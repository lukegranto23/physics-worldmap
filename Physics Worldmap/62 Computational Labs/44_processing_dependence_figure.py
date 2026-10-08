"""Figure for Benchmark 017: conditioned MSD under three processing choices; descriptive, no new test.

Zero-speed (|W| <= 0.01 sd) conditioned MSD in m^2 (published gain), for velocity processing
(order 8, 750 ns), (order 8, 3 us) and (order 2, 3 us), against the published continuum curve
and the forward model (Basset through each operator, plus measured empty-trap noise).
Uses lab 41's functions unchanged.

    python 44_processing_dependence_figure.py --data <dir with Dryad files>
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "processing_dependence"
spec = importlib.util.spec_from_file_location("lab41", HERE / "41_processing_dependence_test.py")
lab41 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab41)
lab35, lab34 = lab41.lab35, lab41.lab34


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, required=True)
    args = ap.parse_args()
    P34 = __import__("json").loads(lab34.PROTOCOL.read_text(encoding="utf-8"))
    for name, expected in P34["target"]["files_sha256"].items():
        if lab35.sha256(args.data / name) != expected:
            raise lab34.GateFailure(f"{name}: digest mismatch")
    Yp, _ = lab34.load_traces(args.data / "barium_titanate_in_acetone_position.csv")
    Ye, _ = lab34.load_traces(args.data / "noise_position.csv")
    times_us = [0.75, 1.5, 2.25, 3, 4.5, 6, 9, 12, 18, 24, 36, 48]
    lab41.TIMES_US = times_us
    G2 = lab41.GAIN2_PUB
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    ker = lab35.Kernel(g0, a0, k0)
    r_ = lab35.PUB["r"]
    mass = 4/3*np.pi*r_**3*lab35.PUB["rho_p"] + 2/3*np.pi*r_**3*lab35.PUB["rho_f"]
    kTm = lab35.KB*lab35.PUB["T"]/mass
    tt = np.logspace(np.log10(0.5e-6), np.log10(60e-6), 200)
    cont = kTm*(2*(ker.int_mchi_minus_limit(tt) + 1/k0) - ker.mchi(tt)**2)

    fig, ax = plt.subplots(figsize=(7, 5.2))
    ax.plot(tt*1e6, cont, "k-", lw=2, label="published continuum theory")
    ax.plot(tt*1e6, cont[100]*(tt/tt[100])**2.5, "k:", lw=1, label=r"$t^{5/2}$ guide")
    colors = {(8, 1): "C0", (8, 4): "C1", (2, 4): "C2"}
    labels = {(8, 1): "order 8, 750 ns (published)", (8, 4): "order 8, 3 µs", (2, 4): "order 2, 3 µs"}
    for v, col in colors.items():
        c = v[1]
        valid = [T for T in times_us if abs(T*1e-6/(c*lab41.DT) - round(T*1e-6/(c*lab41.DT))) < 1e-9 and round(T*1e-6/(c*lab41.DT)) >= 1]
        lab41.TIMES_US = valid
        lags, _, num, cnt = lab41.block_table(Yp, *v)
        obs, _ = lab41.ratio_obs(num, cnt, num.keys())
        _, ne, _, _ = lab41.block_table(Ye, *v)
        u, r, s = lab41.theory_moments(v[0], v[1], lags)
        st = G2*s + ne["s"]
        fwd = lab41.cond(G2*u + ne["u"], G2*r + ne["r"], st, 0.01*np.sqrt(st))
        T = np.array(valid)
        ax.plot(T, obs/G2, "o", color=col, ms=6, label=f"data: {labels[v]}")
        ax.plot(T, fwd/G2, "--", color=col, lw=1.5, label=f"forward model: {labels[v]}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("time after selection (µs)")
    ax.set_ylabel(r"conditioned MSD, $|W|\leq 0.01\,\sigma$ (m$^2$)")
    ax.set_title("Same particle, same positions: the conditioned MSD depends on velocity processing", fontsize=10)
    ax.legend(fontsize=7.5, loc="upper left")
    fig.tight_layout()
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "processing_dependence_figure.png", dpi=160)
    print("wrote", OUT / "processing_dependence_figure.png")


if __name__ == "__main__":
    main()
