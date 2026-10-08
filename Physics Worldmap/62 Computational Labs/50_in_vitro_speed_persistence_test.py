"""Speed-persistence coupling vs localization noise in IN VITRO T-cell tracks. Frozen test; no novelty claim.

Frozen 2026-10-08 before any speed or persistence statistic of these tracks was computed. Only the
file structure was inspected: 10 movies, 21 frames, columns ID/X/Y/T, coordinates in calibrated um
(X max 865 ~ 1344 px x 0.645 um; Y max 658 ~ 1024 px x 0.645 um).

Data: Zenodo 10.5281/zenodo.8420011 (CC-BY 4.0), "T cell dataset for CellTracksColab - 2". These are
T cells migrating on ICAM-1 or VCAM-1, imaged by 10x phase contrast every 30 s for 10 min, segmented
with StarDist and tracked with TrackMate. Pixel 645 nm (source record 10.5281/zenodo.4034929).
File MD5 acb5ce2b9792b5b18d8b5147efe4eee6 was verified.

Method: lab 49's final protocol unchanged (per-cell lag-1 step correlation, closed-form noise
correction, persistence gap between fastest and slowest thirds, sensitivity curve f_noise(sigma)
for sigma = 0..2 um, bootstrap over cells), with dt = 30 s. Tracks are those with >= 6 positions
and no missing frames between first and last; gapped tracks are excluded and counted.
Groups: ICAM (5 movies pooled), VCAM (5 movies pooled), ALL.
Self-tests rerun at dt = 30 s with lab 49's synthetic S1/S2 generators; they must pass.

Physical anchors: sigma_q = 0.645/sqrt(12) = 0.186 um (pure pixel quantisation, a floor) and
sigma_px = 0.645 um (one pixel).

Decision (fixed) per group, requiring G_raw > 0.05:
  NOT ROBUST TO LOCALIZATION NOISE  if sigma_half <= 0.645 um (one pixel or less explains half);
  ROBUST                            if sigma_half > 1.29 um (more than two pixels needed) or never reached;
  INTERMEDIATE                      otherwise.
f_noise at sigma_q and sigma_px is reported. If G_raw <= 0.05: NO COUPLING IN NOISE-CORRECTABLE MEASURE.

    python 50_in_vitro_speed_persistence_test.py --selftest
    python 50_in_vitro_speed_persistence_test.py --data <dir containing Tracks/ICAM/... and Tracks/VCAM/...>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "in_vitro_speed_persistence"
spec = importlib.util.spec_from_file_location("lab49", HERE / "49_speed_persistence_noise_test.py")
lab49 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab49)
lab49.DT = 30.0
SIG_Q, SIG_PX = 0.645/np.sqrt(12), 0.645


def load_group(root, cond):
    import csv
    tracks, gapped = [], 0
    files = sorted((root / "Tracks" / cond).glob("*/*.csv"))
    for f in files:
        per = {}
        with open(f, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                per.setdefault(row["ID"], []).append((int(float(row["T"])), float(row["X"]), float(row["Y"])))
        for rows in per.values():
            a = np.array(sorted(rows))
            if len(a) < lab49.MIN_POS:
                continue
            if np.any(np.diff(a[:, 0]) != 1):
                gapped += 1
                continue
            tracks.append(a[:, 1:3])
    return tracks, gapped, [str(p.relative_to(root)) for p in files]


def verdict(r):
    if not (r["G_raw"] > 0.05):
        return "NO COUPLING IN NOISE-CORRECTABLE MEASURE"
    sh = r["sigma_half"]
    if sh is not None and sh <= SIG_PX + 1e-9:
        return "NOT ROBUST TO LOCALIZATION NOISE"
    if sh is None or sh > 2*SIG_PX:
        return "ROBUST"
    return "INTERMEDIATE"


def f_at(r, s):
    g = np.array(r["sigma_grid"])
    return float(np.interp(s, g, np.nan_to_num(np.array(r["f_noise_curve"], float), nan=np.inf)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--selftest", action="store_true")
    g.add_argument("--data", type=Path)
    args = ap.parse_args()
    meta = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "dt_s": lab49.DT}
    runs = []
    if args.selftest:
        t1, _ = lab49.synthetic(False, 2026100896)
        r1 = lab49.analyse(t1, "S1_no_coupling_sigma1_dt30")
        t2, _ = lab49.synthetic(True, 2026100897)
        r2 = lab49.analyse(t2, "S2_true_coupling_sigma0.2_dt30")
        ok1, ok2 = r1["f_noise_curve"][10] >= 0.8, r2["f_noise_curve"][2] < 0.25
        meta.update(self_tests_pass=bool(ok1 and ok2), S1_pass=bool(ok1), S2_pass=bool(ok2))
        runs = [r1, r2]
        out_dir = OUT / "selftest"
        print("self-tests pass:", meta["self_tests_pass"])
    else:
        st = json.loads((OUT / "selftest" / "results.json").read_text(encoding="utf-8"))
        meta["self_tests_pass"] = st["meta"]["self_tests_pass"]
        groups = {}
        for cond in ("ICAM", "VCAM"):
            tr, gapped, files = load_group(args.data, cond)
            groups[cond] = (tr, gapped, files)
        groups["ALL"] = (groups["ICAM"][0] + groups["VCAM"][0], groups["ICAM"][1] + groups["VCAM"][1],
                         groups["ICAM"][2] + groups["VCAM"][2])
        for name, (tr, gapped, files) in groups.items():
            r = lab49.analyse(tr, name)
            r.update(gapped_tracks_excluded=gapped, files=files,
                     f_noise_at_sigma_quantisation=f_at(r, SIG_Q), f_noise_at_one_pixel=f_at(r, SIG_PX),
                     verdict=verdict(r) if meta["self_tests_pass"] else "NOT INTERPRETABLE (self-test failed)")
            print(f"   {name}: gapped excluded {gapped}; f_noise at 0.19 um {r['f_noise_at_sigma_quantisation']:.2f}, "
                  f"at 0.645 um {r['f_noise_at_one_pixel']:.2f} -> {r['verdict']}", flush=True)
            runs.append(r)
        out_dir = OUT / "zenodo_8420011"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps({"meta": meta, "runs": runs}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
