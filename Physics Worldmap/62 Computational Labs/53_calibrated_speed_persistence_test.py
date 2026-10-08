"""Speed-persistence coupling with a data-internal localization-noise calibration. Frozen test; no novelty claim.

Frozen 2026-10-08 before any speed, persistence or noise statistic of these tracks was computed. Only
the file structure, the track counts, the position counts and the frame intervals had been inspected.
The authors' own simulation script (simulate_prw_artifact_check4.py) was read. It shows that they
checked one assumed noise level, sigma_noise = 2/sqrt(20) in simulation units (about 0.45 um),
for a PRW with constant P.

Data: Jerison & Quake, eLife 9:e53933 (2020), github.com/erjerison/TCellMigration,
trajectory_analysis/master_trajectory_file_all_experiments.txt. These are 2D tracks in um.
  fish_T control (712 tracks, dt 45 s), fish_T rockout (236, 45 s), fish_T highfreq_control (29, 12 s,
  ~830 positions each), Gerard_mouse_T control/Myo1g_KO (42/123, 30 s),
  Gautreau_dicty WT/Arp_KO/Arp_rescue (42/38/42, 5 s).

Tracks: per track, the longest gap-free segment (consecutive time differences equal to the group's
frame interval); segments with >= 6 positions are kept.

Part A, noise calibration (the new element). For each track with >= 100 positions, the
per-coordinate MSD m_k (k = 1..10, both coordinates pooled) is fitted by the OU persistent-walk form
with white localization error,
    m_k = 2 a (k x - 1 + exp(-k x)) + 2 s2,   a = v^2 P^2 >= 0, x = dt/P > 0, s2 = sigma^2 >= 0,
by least squares with relative weights 1/m_k. The group sigma_cal is the median over tracks of
sqrt(s2), with a 1000-replicate bootstrap over tracks (16-84%).
Secondary: quadratic intercept, m_k = c0 + c1 k + c2 k^2 on k = 1..4, sigma^2 = c0/2.
Self-test A (it must pass for sigma_cal to be used): synthetic tracks with the group's real segment
lengths. Each synthetic cell's velocity scale is chosen so that its noise-free step variance equals
the matching real track's measured per-coordinate step variance, minus 2 sigma_true^2 (floored at
10%). This is the only real-data statistic the self-test uses. P is lognormal (median 120 s, log-sd
0.5); within each track P switches between P and P/5 at random 10-frame epochs, a stand-in for
run/pause heterogeneity. sigma_true is 0.3 and 1.0 um. PASS if the median estimate lies within 25% of
sigma_true for both values. A group whose self-test fails gets "SIGMA UNIDENTIFIED", and only its
curve is reported.

Part B, coupling: lab 49's final protocol unchanged (lag-1 step correlation r, per-cell correction,
persistence gap G between speed terciles, f_noise(sigma) for sigma = 0..2 um, 300-replicate
bootstrap), with each group's own dt. Also run: highfreq_control coarsened x4 (48 s, comparable to the
45 s control set), using the highfreq sigma_cal.

Decision (fixed), for each group with G_raw > 0.05 and an identified sigma_cal:
  f_cal = f_noise(sigma_cal) (interpolated); range from f_noise at the sigma_cal 16-84% ends.
  NOISE MINOR if f_cal < 0.2; NOISE SUBSTANTIAL if 0.2 <= f_cal < 0.5; NOISE MAJOR if f_cal >= 0.5.
  For fish_T control and rockout (45 s; no long tracks), the highfreq_control sigma_cal from the
  same fish imaging setup is applied, and is flagged "TRANSFERRED CALIBRATION". If those groups'
  own sigma_cal is identified, it is reported as well.
  G_raw <= 0.05: NO COUPLING IN NOISE-CORRECTABLE MEASURE.
Amendment 1 (2026-10-08, code fix after the first self-test, before any real-data statistic). msd()
divided the per-coordinate MSD by 2 a second time, so every estimate came out as sigma/sqrt(2)
(self-test medians 0.70-0.73 for a true 1.0). The extra /2 is removed. Nothing else changes.

Caveats fixed in advance: frames are 2D projections of z-stacks. Motion blur during acquisition is
ignored. The highfreq imaging settings may differ from those of the 45 s movies.

    python 53_calibrated_speed_persistence_test.py --selftest --data <master_trajectory_file>
    python 53_calibrated_speed_persistence_test.py --run --data <master_trajectory_file>
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "calibrated_speed_persistence"
spec = importlib.util.spec_from_file_location("lab49", HERE / "49_speed_persistence_noise_test.py")
lab49 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab49)
KMAX, MIN_CAL = 10, 100


def load(path):
    raw = {}
    with open(path, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            e, t, s, idx, tr = line.rstrip("\n").split("\t")
            pts = np.array([[float(v) for v in p.split(",")] for p in tr.split(";") if p])
            raw.setdefault(f"{e}/{t}", []).append(pts)
    groups = {}
    for g, trs in raw.items():
        dts = Counter(np.round(np.diff(p[:, 0]), 6)[0] for p in trs if len(p) > 1)
        dt = dts.most_common(1)[0][0]
        segs = []
        for p in trs:
            ok = np.isclose(np.diff(p[:, 0]), dt, rtol=1e-6, atol=1e-6)
            best, start = (0, 0), 0
            for i in range(len(ok) + 1):
                if i == len(ok) or not ok[i]:
                    if i + 1 - start > best[1] - best[0]:
                        best = (start, i + 1)
                    start = i + 1
            seg = p[best[0]:best[1], 1:3]
            if len(seg) >= lab49.MIN_POS:
                segs.append(seg)
        groups[g] = {"dt": float(dt), "tracks": segs, "n_raw": len(trs)}
    return groups


def msd(r, kmax=KMAX):
    return np.array([np.mean((r[k:] - r[:-k])**2) for k in range(1, kmax + 1)])   # mean over both coords = per-coordinate MSD


def sigma_ou(r):
    m = msd(r)
    k = np.arange(1, KMAX + 1)
    def res(p):
        a, x, s2 = np.exp(p)
        return (2*a*(k*x - 1 + np.exp(-k*x)) + 2*s2 - m)/m
    best = None
    for x0 in (0.05, 0.3, 1.5):
        a0 = max(m[-1] - m[0], 1e-6)/(2*max(KMAX*x0 - 1 + np.exp(-KMAX*x0), 1e-6))
        for s0 in (0.05, 0.5):
            f = least_squares(res, np.log([a0, x0, max(s0*m[0], 1e-8)]), method="lm")
            if best is None or f.cost < best.cost:
                best = f
    return float(np.sqrt(np.exp(best.x[2])))


def sigma_quad(r):
    m = msd(r, 4)
    c = np.polyfit(np.arange(1, 5), m, 2)
    return float(np.sqrt(max(c[-1], 0)/2))


def calibrate(tracks, rng):
    long = [r for r in tracks if len(r) >= MIN_CAL]
    if len(long) < 5:
        return None
    s = np.array([sigma_ou(r) for r in long])
    q = np.array([sigma_quad(r) for r in long])
    bs = [np.median(s[rng.integers(0, len(s), len(s))]) for _ in range(1000)]
    return {"tracks_used": len(long), "sigma_cal": float(np.median(s)), "sigma_cal_16_84": np.percentile(bs, [16, 84]).tolist(),
            "sigma_quad_median": float(np.median(q)), "per_track_sigma": s.tolist()}


def synth_like(tracks, dt, sigma, rng):
    out = []
    for r in tracks:
        n = len(r)
        Vhat = np.mean(np.diff(r, axis=0)**2)
        Vtrue = max(Vhat - 2*sigma**2, 0.1*Vhat)
        P0 = rng.lognormal(np.log(120.0), 0.5)
        x = dt/P0
        vsd = np.sqrt(Vtrue/(2*P0**2*(x - 1 + np.exp(-x))))
        v = rng.normal(0, vsd, 2); pos = np.zeros((n, 2)); P = P0; h = dt/10
        for i in range(1, n):
            if i % 10 == 0:
                P = P0 if rng.random() < 0.5 else P0/5
            a = np.exp(-h/P)
            step = np.zeros(2)
            for _ in range(10):          # exact OU velocity on substeps, position by midpoint rule
                vn = a*v + np.sqrt(1 - a*a)*vsd*rng.normal(size=2)
                step += 0.5*(v + vn)*h
                v = vn
            pos[i] = pos[i-1] + step
        out.append(pos + rng.normal(0, sigma, (n, 2)))
    return out


def selftest(groups, rng):
    res = {}
    for g, d in groups.items():
        long = [r for r in d["tracks"] if len(r) >= MIN_CAL]
        if len(long) < 5:
            res[g] = {"pass": False, "reason": "fewer than 5 tracks with >= 100 positions"}
            continue
        row = {}
        for st in (0.3, 1.0):
            syn = synth_like(long, d["dt"], st, rng)
            est = float(np.median([sigma_ou(r) for r in syn]))
            row[str(st)] = {"median_est": est, "quad_median": float(np.median([sigma_quad(r) for r in syn])),
                            "ok": bool(abs(est/st - 1) <= 0.25)}
        row["pass"] = bool(all(v["ok"] for k, v in row.items() if k != "pass"))
        res[g] = row
        print(g, row, flush=True)
    return res


def decide(f):
    if f is None or not np.isfinite(f):
        return "UNDEFINED"
    return "NOISE MINOR" if f < 0.2 else ("NOISE SUBSTANTIAL" if f < 0.5 else "NOISE MAJOR")


def f_at(r, s):
    g = np.array(r["sigma_grid"]); c = np.nan_to_num(np.array(r["f_noise_curve"], float), nan=np.inf)
    return float(np.interp(s, g, c))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument("--selftest", action="store_true")
    m.add_argument("--run", action="store_true")
    ap.add_argument("--data", type=Path, required=True)
    a = ap.parse_args()
    groups = load(a.data)
    meta = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "data_sha256": hashlib.sha256(a.data.read_bytes()).hexdigest(),
            "groups": {g: {"dt": d["dt"], "n_raw": d["n_raw"], "n_kept": len(d["tracks"]),
                           "median_len": int(np.median([len(r) for r in d["tracks"]]))} for g, d in groups.items()}}
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(2026100853)
    if a.selftest:
        meta["selftest"] = selftest(groups, rng)
        (OUT / "selftest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return
    st = json.loads((OUT / "selftest.json").read_text(encoding="utf-8"))["selftest"]
    hf = "fish_T/highfreq_control"
    groups[hf + "_x4"] = {"dt": groups[hf]["dt"]*4, "tracks": [r[::4] for r in groups[hf]["tracks"] if len(r[::4]) >= lab49.MIN_POS]}
    cal = {}
    for g, d in groups.items():
        if g.endswith("_x4"):
            continue
        c = calibrate(d["tracks"], rng)
        if c is not None:
            c["identified"] = bool(st.get(g, {}).get("pass", False))
        cal[g] = c
        if c:
            print(f"{g}: sigma_cal {c['sigma_cal']:.3f} [{c['sigma_cal_16_84'][0]:.3f}, {c['sigma_cal_16_84'][1]:.3f}] "
                  f"(quad {c['sigma_quad_median']:.3f}), identified {c['identified']}", flush=True)
    runs = []
    for g, d in groups.items():
        lab49.DT = d["dt"]
        r = lab49.analyse(d["tracks"], g)
        src = g[:-3] if g.endswith("_x4") else g
        c = cal.get(src)
        flag = "OWN CALIBRATION"
        if (c is None or not c["identified"]) and g in ("fish_T/control", "fish_T/rockout"):
            c, flag = cal.get(hf), "TRANSFERRED CALIBRATION (fish highfreq)"
        if g.endswith("_x4"):
            flag = "highfreq calibration, coarsened x4"
        if not (r["G_raw"] > 0.05):
            r["verdict"] = "NO COUPLING IN NOISE-CORRECTABLE MEASURE"
        elif c is None or not c["identified"]:
            r["verdict"] = "SIGMA UNIDENTIFIED (curve only)"
        else:
            fc = f_at(r, c["sigma_cal"]); lo, hi = (f_at(r, s) for s in c["sigma_cal_16_84"])
            r.update(f_cal=fc, f_cal_range=[lo, hi], sigma_used=c["sigma_cal"], calibration=flag, verdict=decide(fc))
        print(f"   -> {g}: G_raw {r['G_raw']:.3f}; {r['verdict']}"
              + (f"; f_cal {r['f_cal']:.2f} [{r['f_cal_range'][0]:.2f}, {r['f_cal_range'][1]:.2f}] ({r['calibration']})" if "f_cal" in r else ""),
              flush=True)
        runs.append(r)
    meta["calibration"] = {g: ({k: v for k, v in c.items()} if c else None) for g, c in cal.items()}
    (OUT / "results.json").write_text(json.dumps({"meta": meta, "runs": runs}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
