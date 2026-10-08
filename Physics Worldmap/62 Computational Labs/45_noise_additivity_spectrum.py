"""Is detector noise additive and particle-independent? A spectral check; descriptive, no novelty claim.

Benchmarks 015 and 017 subtract or add empty-trap noise moments, assuming the particle-run
noise equals the empty-trap noise. Here the one-sided power spectral density of the supplied
750 ns positions is compared for particle and empty-trap traces against the published-Basset
particle spectrum (published gain), including the 750 ns box average and aliasing:

    S_Y(f) = sum_m S_x(f + m f_s) sinc^2((f + m f_s)/f_s),   f_s = 1/(750 ns).

Additivity predicts S_particle - S_empty = G^2 S_Y. The ratio (S_particle - S_empty)/(G^2 S_Y)
is reported in frequency bands; values near 1 support additivity, systematic departures at
high frequency (where the particle term is small) indicate particle-dependent noise.
Descriptive diagnostic only; no decision rule, so nothing here is a test verdict.

    python 45_noise_additivity_spectrum.py --data <dir with Dryad files>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "noise_additivity"
spec = importlib.util.spec_from_file_location("lab35", HERE / "35_gain_free_hydrodynamic_memory.py")
lab35 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab35)
lab34 = lab35.lab34
DT = 7.5e-7
GAIN2 = 861966767682287.1


def model_psd_one_sided(f, M=200):
    """One-sided PSD (V^2/Hz) of 750 ns box-averaged, sampled positions under published Basset."""
    r = lab35.PUB["r"]
    mass = 4/3*np.pi*r**3*lab35.PUB["rho_p"] + 2/3*np.pi*r**3*lab35.PUB["rho_f"]
    kTm = lab35.KB*lab35.PUB["T"]/mass
    g, a, k = lab35.physical_to_scaled(r, lab35.PUB["K"])
    fs = 1/DT
    tot = np.zeros_like(f)
    for m in range(-M, M + 1):
        ff = np.abs(f + m*fs)
        ff = np.where(ff == 0, 1e-12, ff)
        w = 2*np.pi*ff
        s = -1j*w
        chi = 1/(s*s + a*s*np.sqrt(s) + g*s + k)
        Sx = 2*np.imag(chi)/w*kTm            # two-sided, m^2 per (rad/s) normalisation: S(w) with C = (1/2pi) int S dw
        tot += Sx*np.sinc(ff*DT)**2
    return 2*tot*GAIN2                       # two-sided per Hz is S(w) (since dw/2pi = df); one-sided doubles


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, required=True)
    args = ap.parse_args()
    P34 = json.loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
    for name, expected in P34["target"]["files_sha256"].items():
        if lab35.sha256(args.data / name) != expected:
            raise lab34.GateFailure(f"{name}: digest mismatch")
    Yp, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_position.csv")
    Ye, _ = lab34.load_traces(args.data / "noise_position.csv")
    nper = 8192
    f, Sp = welch(np.array(Yp), fs=1/DT, nperseg=nper, axis=-1)
    _, Se = welch(np.array(Ye), fs=1/DT, nperseg=nper, axis=-1)
    Sp, Se = Sp.mean(0), Se.mean(0)
    Sm = model_psd_one_sided(f)
    bands = [(2e3, 1e4), (1e4, 3e4), (3e4, 1e5), (1e5, 2e5), (2e5, 4e5), (4e5, 6e5), (6e5, 6.6e5)]
    rows = []
    for lo, hi in bands:
        sel = (f >= lo) & (f < hi)
        rows.append({"band_hz": [lo, hi], "ratio_excess_over_model": float(np.mean((Sp[sel] - Se[sel])/Sm[sel])),
                     "empty_over_model": float(np.mean(Se[sel]/Sm[sel])), "particle_over_empty": float(np.mean(Sp[sel]/Se[sel]))})
        print(f"{lo/1e3:6.0f}-{hi/1e3:4.0f} kHz: (S_p - S_e)/model = {rows[-1]['ratio_excess_over_model']:.3f}  "
              f"S_e/model = {rows[-1]['empty_over_model']:.3f}  S_p/S_e = {rows[-1]['particle_over_empty']:.3f}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps({"bands": rows, "nperseg": nper,
                                                   "status": "descriptive diagnostic; no decision rule"}, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(f[1:], Sp[1:], label="particle traces", lw=1)
    ax.loglog(f[1:], Se[1:], label="empty-trap traces", lw=1)
    ax.loglog(f[1:], Sm[1:], "k--", label="published Basset (gain$^2$), binned + aliased", lw=1)
    ax.loglog(f[1:], Sm[1:] + Se[1:], "k:", label="model + empty-trap noise", lw=1)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("one-sided PSD (V$^2$/Hz)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "noise_additivity_psd.png", dpi=150)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
