"""Synthetic positive and negative controls for lab 35's frozen gain-free decision rules; no novelty claim.

Lab 35 was frozen without a self-test. This script asks, before its real-data
run, whether the frozen rules are calibrated and have power when the truth is
known. Stationary Gaussian positions are synthesised exactly in frequency from
the classical fluctuation-dissipation spectrum S_x = (2kT/w) Im chi(w), at
1/N_SUB of the 750 ns bin, then box-averaged to bins, so the bin-and-stencil
operator is exercised rather than assumed. Detector noise (white plus a smooth
low-frequency component) is added independently to particle and empty-trap
records. Lab 35's own functions (estimate_R, fit, operator_R, gls) are reused
unmodified; only the data source differs. No real data is read.

    python 38_gain_free_selftest.py            # full control set
    python 38_gain_free_selftest.py --quick    # one seed per truth, fewer refits
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from datetime import datetime, timezone
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.stats import chi2 as chi2_dist

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "gain_free_selftest"
spec = importlib.util.spec_from_file_location("lab35", HERE / "35_gain_free_hydrodynamic_memory.py")
lab35 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab35)
lab34 = lab35.lab34

N_TRACES = 6
N_BINS = 111848          # per trace, as in the Dryad files
N_SUB = 30               # fine samples per 750 ns bin (25 ns)
NOISE_FRACTION_W = 0.06  # empty-trap Var(W) / particle Var(W) is 0.0603 in Benchmark 014's saved results
WHITE_SHARE_W = 0.6      # share of the noise Var(W) that is white at bin level
SMOOTH_NOISE = (2.0e4, 4.0e8)   # (g, k) of a memoryless oscillator used only as a smooth drift-noise shape


def spectrum(w, g, a, k):
    """Two-sided position PSD per kT/m for P(s) = s^2 + a s^{3/2} + g s + k at s = -i w."""
    s = -1j*w
    chi = 1/(s*s + a*s*np.sqrt(s) + g*s + k)
    return 2*np.imag(chi)/w


def synth_binned(rng, n_traces, n_bins, dt, g, a, k):
    """Stationary Gaussian positions, continuum-averaged over bins of width dt (fine-grid box average)."""
    delta = dt/N_SUB
    n = 2*(n_bins*N_SUB)     # double length, keep the first half: removes periodic wrap
    w = 2*np.pi*np.fft.rfftfreq(n, delta)
    S = np.zeros_like(w)
    S[1:] = spectrum(w[1:], g, a, k)
    scale = np.sqrt(n*S/delta/2)
    out = []
    for _ in range(n_traces):
        c = scale*(rng.normal(size=w.size) + 1j*rng.normal(size=w.size))
        c[0] = 0
        c[-1] = c[-1].real*np.sqrt(2)
        x = np.fft.irfft(c, n)[: n_bins*N_SUB]
        out.append(x.reshape(n_bins, N_SUB).mean(axis=1))
    return out


def make_records(rng, truth, dt):
    """Particle (signal + noise) and empty-trap (noise only) records, positions and stencil velocities."""
    g, a, k = truth
    pad = N_BINS + 8
    sig = synth_binned(rng, N_TRACES, pad, dt, g, a, k)
    # noise amplitudes from the model's own operator Var(W), so the noise share is set, not fitted
    s_signal = np.mean([np.var(np.convolve(y, lab34.STENCIL8[::-1], mode="valid")/dt) for y in sig])
    s_noise = NOISE_FRACTION_W*s_signal
    sigma_white = np.sqrt(WHITE_SHARE_W*s_noise*dt**2/np.sum(lab34.STENCIL8**2))

    def noise():
        smooth = synth_binned(rng, N_TRACES, pad, dt, SMOOTH_NOISE[0], 0.0, SMOOTH_NOISE[1])
        s_sm = np.mean([np.var(np.convolve(y, lab34.STENCIL8[::-1], mode="valid")/dt) for y in smooth])
        f = np.sqrt((1 - WHITE_SHARE_W)*s_noise/s_sm)
        return [f*y + sigma_white*rng.normal(size=pad) for y in smooth]

    def split(ys):
        W = [np.convolve(y, lab34.STENCIL8[::-1], mode="valid")/dt for y in ys]
        return [y[4:-4] for y in ys], W

    Yp, Wp = split([s + n for s, n in zip(sig, noise())])
    Ye, We = split(noise())
    return Yp, Wp, Ye, We


_REFIT = {}


def jsonable(obj):
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    return lab34.to_jsonable(obj)


def _refit(i):
    s = _REFIT
    return {m: lab35.fit(m, s["reps"][i], s["Cinv"], s["lags"], s["dt"], s["start"][m])[0] for m in s["start"]}


def analyse(Yp, Wp, Ye, We, P, n_refits, seed_offset):
    """Lab 35's main sequence on supplied records, with its frozen seeds, models, and decision rules."""
    lags = P["observable"]["lags_samples"]
    dt = P["observable"]["sample_time_s"]
    halves, empty = lab35.gather(Yp, Wp, lags), lab35.gather(Ye, We, lags)
    R = lab35.estimate_R(halves, empty)
    rng = np.random.default_rng(2026100611 + seed_offset)
    reps = np.array([lab35.estimate_R(halves, empty, rng, 2000) for _ in range(400)])
    cov = np.cov(reps.T)
    Cinv = np.linalg.inv(cov)
    se = np.sqrt(np.diag(cov))
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    kE = lab35.Kernel(g0, a0, k0)
    t = np.array(lags)*dt
    R_E = lab35.operator_R(kE, lags, dt)
    R_V = R_E*(1 + a0*kE.mpsi(t)/kE.mchi(t))
    fits = {}
    for model, start in (("B2", [lab35.PUB["r"], lab35.PUB["K"]]), ("B3", [g0, a0, k0]), ("L", [g0, k0])):
        p, c2, pred = lab35.fit(model, R, Cinv, lags, dt, start)
        fits[model] = {"params": p, "chi2": c2}
    boot = {m: [] for m in fits}
    _REFIT.update(reps=reps, Cinv=Cinv, lags=lags, dt=dt, start={m: fits[m]["params"] for m in fits})
    with Pool(min(16, os.cpu_count() or 1)) as pool:
        for res in pool.imap(_refit, np.random.default_rng(2026100612 + seed_offset).choice(len(reps), n_refits, replace=False)):
            for m in fits:
                boot[m].append(res[m])
    n = len(lags)
    chi = {"E_published": lab35.gls(R_E, R, Cinv), "V_initial_value_variant": lab35.gls(R_V, R, Cinv),
           "B2_fit": fits["B2"]["chi2"], "B3_fit": fits["B3"]["chi2"], "L_fit": fits["L"]["chi2"]}
    npar = {"E_published": 0, "V_initial_value_variant": 0, "B2_fit": 2, "B3_fit": 3, "L_fit": 2}
    table = {m: {"chi2": c, "dof": n - npar[m], "p": float(chi2_dist.sf(c, n - npar[m])),
                 "p_se_corrected": float(chi2_dist.sf(c/1.44, n - npar[m]))} for m, c in chi.items()}
    zB3 = np.array(boot["B3"])[:, 1]
    interval = [float(np.percentile(zB3, 16)), float(np.percentile(zB3, 84))]
    dec = {"E_published_consistent": table["E_published"]["p"] > 0.01,
           "V_rejected_vs_E": chi["V_initial_value_variant"] - chi["E_published"] > 25,
           "memory_supported_L_minus_B2": chi["L_fit"] - chi["B2_fit"],
           "memory_supported": chi["L_fit"] - chi["B2_fit"] > 25,
           "z_over_m_B3": [float(fits["B3"]["params"][1]), interval],
           "z_interval_contains_stokes_basset": bool(interval[0] <= a0 <= interval[1])}
    return {"models": table, "decision": dec, "R_s": R.tolist(), "R_se_s": se.tolist(), "relative_se": (se/np.abs(R)).tolist(),
            "R_E_s": R_E.tolist(), "fits": {m: np.asarray(v["params"]).tolist() for m, v in fits.items()},
            "noise_fraction_of_varW": float(lab35.moments(empty)[1]/lab35.moments(halves)[1])}


def check_synthesis(dt):
    """The synthesiser reproduces the FDT increment variances the operator uses (independent spectral route).

    Compares Var(Y_{j+n} - Y_j) = 2(G(0) - G(n)) from the operator's time-domain root formula with the
    synthetic bin-averaged records; increments avoid the sample-mean bias of the slow trap mode.
    """
    g, a, k = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    rng = np.random.default_rng(2026100830)
    ys = synth_binned(rng, 24, 20000, dt, g, a, k)
    ker = lab35.Kernel(g, a, k)
    lags = [1, 2, 4, 16, 64, 256]
    x, wq = np.polynomial.legendre.leggauss(24)
    u = 0.5*dt*(x + 1)
    wu = 0.5*dt*wq*(1 - u/dt)/dt
    Cx = lambda tt: -ker.int_mchi_minus_limit(np.abs(tt))
    G = lambda n: (Cx(n*dt + u) + Cx(n*dt - u)) @ wu
    theory = np.array([2*(G(0) - G(n)) for n in lags])
    emp = np.array([np.mean([np.mean((y[n:] - y[:-n])**2) for y in ys]) for n in lags])
    # Exact expectation of the synthesiser itself: discrete spectrum, fine-grid box filter, no sampling noise.
    delta = dt/N_SUB
    nfine = 2*N_BINS*N_SUB
    w = 2*np.pi*np.fft.rfftfreq(nfine, delta)[1:-1]
    S = spectrum(w, g, a, k)
    H2 = np.abs(np.exp(1j*np.outer(w, np.arange(N_SUB)*delta)).mean(axis=1))**2
    exact = np.array([2/(nfine*delta)*np.sum(S*H2*2*(1 - np.cos(w*n*dt))) for n in lags])
    return {"lags": lags, "operator_increment_var": theory.tolist(),
            "synthesiser_expected_increment_var": exact.tolist(), "expected_relative_difference": (exact/theory - 1).tolist(),
            "monte_carlo_increment_var": emp.tolist(), "monte_carlo_relative_difference": (emp/theory - 1).tolist()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    P = json.loads(lab35.PROTOCOL.read_text(encoding="utf-8"))
    dt = P["observable"]["sample_time_s"]
    g0, a0, k0 = lab35.physical_to_scaled(lab35.PUB["r"], lab35.PUB["K"])
    truths = {"basset_published": (g0, a0, k0), "langevin_same_gamma_K": (g0, 0.0, k0)}
    seeds = [2026100841] if args.quick else [2026100841, 2026100842, 2026100843]
    n_refits = 20 if args.quick else 40
    synthesis = check_synthesis(dt)
    print("synthesis check, expected vs operator:", np.round(synthesis["expected_relative_difference"], 6),
          "monte carlo:", np.round(synthesis["monte_carlo_relative_difference"], 4), flush=True)
    runs = []
    for name, truth in truths.items():
        for i, seed in enumerate(seeds):
            rng = np.random.default_rng(seed + (100 if name.startswith("langevin") else 0))
            res = analyse(*make_records(rng, truth, dt), P, n_refits, seed_offset=i + 1)
            res.update(truth=name, seed=seed)
            runs.append(jsonable(res))
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / "partial.json").write_text(json.dumps(runs, indent=2), encoding="utf-8")
            d = res["decision"]
            print(f"{name:>22} seed {seed}: " + "  ".join(f"{m}={v['chi2']:.1f}(p={v['p']:.2g})" for m, v in res["models"].items()), flush=True)
            print(f"{'':>22}   E ok={d['E_published_consistent']} V rejected={d['V_rejected_vs_E']} "
                  f"memory={d['memory_supported']} (dchi2={d['memory_supported_L_minus_B2']:.1f}) "
                  f"z/m={d['z_over_m_B3'][0]:.1f} [{d['z_over_m_B3'][1][0]:.1f}, {d['z_over_m_B3'][1][1]:.1f}] "
                  f"median rel SE={np.median(res['relative_se']):.4f}", flush=True)
    out = {"meta": {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "lab35_script_sha256": hashlib.sha256((HERE / "35_gain_free_hydrodynamic_memory.py").read_bytes()).hexdigest(),
                    "lab35_protocol_sha256": hashlib.sha256(lab35.PROTOCOL.read_bytes()).hexdigest(),
                    "quick": args.quick, "n_refits": n_refits, "n_sub": N_SUB, "noise_fraction_W": NOISE_FRACTION_W,
                    "white_share_W": WHITE_SHARE_W, "smooth_noise_g_k": SMOOTH_NOISE,
                    "status": "synthetic controls only; no real data read"},
           "published_scaled": {"gamma_over_m": g0, "z_over_m": a0, "K_over_m": k0},
           "synthesis_check": synthesis, "runs": runs}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ("results_quick.json" if args.quick else "results.json")).write_text(json.dumps(jsonable(out), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
