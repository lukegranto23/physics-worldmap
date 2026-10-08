"""Audited stress test of a restricted correlation-to-memory implementation.

Wishart inputs represent independent Gaussian trajectory ensembles, not the
paper's molecular dynamics data. Spectral repair is deliberately not implemented.
"""
from __future__ import annotations
import csv
import hashlib
import importlib.util
import json
import platform
import warnings
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.linalg import expm, logm, solve_continuous_are, toeplitz
from scipy.stats import norm, wishart

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "noisy_memory_stress_protocol.json"
OUT = HERE / "results" / "noisy_memory_stress"
spec = importlib.util.spec_from_file_location("thermal_memory_reference",
                                              HERE / "27_thermal_memory_reproduction.py")
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def wilson(count, total):
    if total == 0:
        return None
    z = norm.ppf(0.975)
    p = count / total
    denominator = 1 + z*z/total
    center = (p + z*z/(2*total)) / denominator
    half = z*np.sqrt(p*(1-p)/total + z*z/(4*total**2)) / denominator
    return [float(max(0, center-half)), float(min(1, center+half))]


def real_finite(value, label):
    array = np.asarray(value)
    if not np.all(np.isfinite(array)):
        raise ValueError("nonfinite:" + label)
    if np.iscomplexobj(array) and np.max(abs(array.imag)) > 1e-8:
        raise ValueError("nonreal:" + label)
    return array.real


def exponential_bilinear(matrix, left, right, times):
    """Direct matrix exponentials also handle repeated or defective eigenvalues."""
    values = np.array([left @ expm(t*matrix) @ right for t in times])
    return real_finite(values, "matrix-exponential")


def fit_restricted(moments, n, p):
    """Same Newton update as lab 27, with explicit diagnostics and no spectral repair."""
    y = real_finite(moments[:2*n].copy(), "input")
    for iteration in range(p["newton_max_iterations"]):
        jacobi, derivative = reference.jacobi_and_derivative(y)
        real_finite(jacobi, "jacobi")
        real_finite(derivative, "jacobi-derivative")
        system, dsystem = reference.system_and_frechet(jacobi, derivative, p["tau"])
        residual, slope = float(system[0, 0].real), float(dsystem[0, 0].real)
        real_finite([residual, slope], "newton")
        if abs(residual) <= p["newton_tolerance"]:
            break
        if slope == 0:
            raise ValueError("newton_zero_derivative")
        y[1] -= residual/slope
    else:
        raise ValueError("newton_nonconvergence")
    poles = np.linalg.eigvals(jacobi)
    if np.max(abs(poles)) >= p["acceptance"]["maximum_discrete_pole_modulus"]:
        raise ValueError("spectral_repair_required_unstable_pole")
    if np.any((abs(poles.imag) < 1e-10) & (poles.real < 0)):
        raise ValueError("spectral_repair_required_negative_pole")
    system = real_finite(logm(jacobi)/p["tau"], "matrix-logarithm")
    if abs(system[0, 0]) > p["newton_tolerance"]:
        raise ValueError("recomputed_derivative_constraint")
    return y, system, iteration+1


def attempt(noisy, n, p, omega, tv, cv, tk, kernel):
    a = p["acceptance"]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            y, system, iterations = fit_restricted(noisy, n, p)
        if np.max(np.linalg.eigvals(system).real) >= a["maximum_real_system_eigenvalue"]:
            return None, "unstable_system"
        b, c, a0 = system[0, 1:], -system[1:, 0], system[1:, 1:]
        if np.max(np.linalg.eigvals(a0).real) >= a["maximum_real_auxiliary_eigenvalue"]:
            return None, "unstable_auxiliary_block"
        kappa = np.array([b @ np.linalg.solve(1j*w*np.eye(n-1)-a0, c) for w in omega])
        if not np.all(np.isfinite(kappa)):
            return None, "nonfinite_transfer"
        positive_min = float(min(kappa.real))
        if positive_min < a["sampled_positive_real_minimum"]:
            return None, "sampled_non_positive_real"
        delta = p["regularization_delta"]
        ric_b = 2*delta*a0 - np.outer(c, b)
        try:
            sigma0 = solve_continuous_are(ric_b.T, b[:, None], np.outer(c, c), [[-1.]])
        except (ValueError, np.linalg.LinAlgError):
            return None, "riccati_solver"
        sigma0 = real_finite((sigma0+sigma0.T)/2, "covariance")
        ric = float(np.linalg.norm(ric_b@sigma0 + sigma0@ric_b.T
                                   + sigma0@np.outer(b,b)@sigma0 + np.outer(c,c)))
        real_finite(ric, "riccati-residual")
        if ric > a["riccati_residual_frobenius"]:
            return None, "riccati_residual"
        if np.min(np.linalg.eigvalsh(sigma0)) < a["covariance_minimum_eigenvalue"]:
            return None, "nonpositive_covariance"
        regularized = system.copy()
        regularized[0,0] = -delta
        if np.max(np.linalg.eigvals(regularized).real) >= a["maximum_real_system_eigenvalue"]:
            return None, "unstable_regularized_system"
        covariance = np.zeros_like(system)
        covariance[0,0] = 1.
        covariance[1:,1:] = sigma0
        noise = np.r_[2*delta, c-sigma0@b]/np.sqrt(2*delta)
        lyap = float(np.linalg.norm(regularized@covariance + covariance@regularized.T
                                   + np.outer(noise,noise)))
        real_finite(lyap, "lyapunov-residual")
        if lyap > a["lyapunov_residual_frobenius"]:
            return None, "lyapunov_residual"
        e1 = np.eye(n)[0]
        sample_fit = exponential_bilinear(system, e1, e1, np.arange(2*n)*p["tau"])
        interp = float(max(abs(sample_fit-y)))
        if interp > a["adjusted_sample_interpolation_max_abs_error"]:
            return None, "interpolation_residual"
        vacf_fit = exponential_bilinear(regularized, e1, e1, tv)
        kernel_fit = exponential_bilinear(a0, b, c, tk)
        nonpositive = bool(np.any(kernel_fit <= 0))
        # The extended loss is +infinity on a sign mismatch. JSON uses null
        # with an explicit status; it never contains NaN or Infinity tokens.
        log_error = None if nonpositive else float(np.sqrt(np.mean(np.log(kernel_fit/kernel)**2)))
        accepted = {
            "n": n, "vacf_rmse": float(np.sqrt(np.mean((vacf_fit-cv)**2))),
            "kernel_log_rmse": log_error, "kernel_nonpositive": int(nonpositive),
            "kernel_relative_rmse": float(np.sqrt(np.mean(((kernel_fit-kernel)/kernel)**2))),
            "y1_adjustment": float(y[1]-noisy[1]),
            "positive_real_min": positive_min, "riccati_residual": ric,
            "lyapunov_residual": lyap, "interpolation_error": interp,
            "original_sample_rmse": float(np.sqrt(np.mean((sample_fit-noisy[:2*n])**2))),
            "newton_evaluations": iterations,
            "regularized_max_real_eigenvalue": float(max(np.linalg.eigvals(regularized).real)),
            "system": regularized, "kernel_curve": kernel_fit, "vacf_curve": vacf_fit,
        }
        return accepted, "accepted"
    except (ValueError, np.linalg.LinAlgError, FloatingPointError, OverflowError) as exc:
        return None, str(exc)[:180]


def kernel_median(rows):
    if not rows:
        return None, "no_accepted_fits"
    values = [float("inf") if r["kernel_nonpositive"] else r["kernel_log_rmse"] for r in rows]
    value = float(np.median(values))
    return (value, "finite") if np.isfinite(value) else (None, "infinite_due_to_sign_mismatch")


def main():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    tau, nmax = p["tau"], p["starting_n"]
    truth = np.array([reference.mittag_leffler_3_2(k*tau) for k in range(2*nmax)])
    target = toeplitz(truth)
    evaluation = p["evaluation"]
    tv = np.linspace(*evaluation["vacf_interval"], evaluation["vacf_points"])
    tk = np.geomspace(*evaluation["kernel_interval"], evaluation["kernel_points"])
    cv = np.array([reference.mittag_leffler_3_2(float(t)) for t in tv])
    kernel = 1/np.sqrt(np.pi*tk)
    fg = p["frequency_grid"]
    omega = np.geomspace(fg["minimum"], fg["maximum"], fg["points"])
    checks = []

    def check(name, condition, value):
        checks.append({"name": name, "passed": bool(condition), "value": value})
        if not condition:
            raise AssertionError(name + ": " + str(value))

    check("analytic trajectory covariance positive definite",
          np.min(np.linalg.eigvalsh(target)) > 1e-10, float(np.min(np.linalg.eigvalsh(target))))
    for bad in [np.array([np.nan]), np.array([np.inf]), np.array([1+0.1j])]:
        try:
            real_finite(bad, "guard-test")
            rejected = False
        except ValueError:
            rejected = True
        check("nonfinite or nonreal guard", rejected, str(bad))
    # Independent generator validation using explicit Gaussian trajectories.
    # Ratio-estimator covariance is (K_rest-c c^T)/(M-2), not independent lag noise.
    validation_rng = np.random.default_rng(12345)
    small_target = target[:4,:4]
    paths = validation_rng.standard_normal((6000,64,4)) @ np.linalg.cholesky(small_target).T
    estimates_direct = np.einsum("bi,bij->bj", paths[:,:,0], paths) / np.sum(paths[:,:,0]**2, axis=1)[:,None]
    expected_cov = (small_target[1:,1:]-np.outer(truth[1:4],truth[1:4]))/62
    check("explicit-trajectory estimator mean", np.max(abs(estimates_direct[:,1:].mean(0)-truth[1:4])) < .008,
          float(np.max(abs(estimates_direct[:,1:].mean(0)-truth[1:4]))))
    rel_cov = float(np.linalg.norm(np.cov(estimates_direct[:,1:],rowvar=False)-expected_cov)/np.linalg.norm(expected_cov))
    check("explicit-trajectory estimator covariance", rel_cov < .08, rel_cov)
    clean, why = attempt(truth,nmax,p,omega,tv,cv,tk,kernel)
    check("clean-case regression", clean is not None, why)
    if clean is not None:
        check("clean VACF error", clean["vacf_rmse"] < .002, clean["vacf_rmse"])
        check("clean kernel error", clean["kernel_log_rmse"] < .2, clean["kernel_log_rmse"])

    rng = np.random.default_rng(p["seed"])
    rows, attempts, input_blocks = [], [], []
    states, ids = [], []
    all_covariances = []
    with (OUT/"attempts.jsonl").open("w",encoding="utf-8") as log:
        for M in p["ensemble_sizes"]:
            scatters = wishart.rvs(df=M,scale=target,size=p["replicates_per_size"],random_state=rng)
            estimates = scatters[:,0,:]/scatters[:,0,0,None]
            estimates[:,0] = 1.
            input_blocks.append(estimates)
            all_covariances.append(scatters/M)
            for rep,noisy in enumerate(estimates):
                fit = None
                first = None
                for n in range(nmax,p["minimum_n"]-1,-1):
                    fit, why = attempt(noisy,n,p,omega,tv,cv,tk,kernel)
                    entry = {"ensemble_size": M, "replicate": rep, "n": n, "reason": why}
                    attempts.append(entry)
                    log.write(json.dumps(entry,allow_nan=False)+"\n")
                    if first is None:
                        first = why
                    if fit is not None:
                        break
                row = {"ensemble_size":M,"replicate":rep,"accepted":int(fit is not None),
                       "full_order":int(fit is not None and n==nmax),
                       "accepted_n":n if fit else None,
                       "fitted_window_end":(2*n-1)*tau if fit else None,
                       "first_attempt_reason":first,"final_reason":why}
                keys = ["vacf_rmse","kernel_log_rmse","kernel_nonpositive","kernel_relative_rmse",
                        "y1_adjustment","positive_real_min","riccati_residual","lyapunov_residual",
                        "interpolation_error","original_sample_rmse","newton_evaluations",
                        "regularized_max_real_eigenvalue"]
                row.update({k:fit[k] if fit else None for k in keys})
                if fit:
                    row["good_vacf_bad_kernel"] = int(
                        fit["vacf_rmse"] <= evaluation["good_vacf_rmse_threshold"]
                        and (fit["kernel_nonpositive"] or
                             fit["kernel_log_rmse"] > evaluation["bad_kernel_log_rmse_threshold"]))
                    row["y1_adjustment_over_sampling_sd"] = abs(fit["y1_adjustment"])/np.sqrt((1-truth[1]**2)/(M-2))
                    padded = np.zeros((nmax,nmax))
                    padded[:n,:n] = fit["system"]
                    states.append(padded)
                    ids.append([M,rep,n])
                else:
                    row["good_vacf_bad_kernel"] = 0
                    row["y1_adjustment_over_sampling_sd"] = None
                rows.append(row)
            log.flush()
            print(f"M={M}: {sum(r['accepted'] for r in rows if r['ensemble_size']==M)}/{p['replicates_per_size']} accepted",flush=True)

    summary = []
    for M in p["ensemble_sizes"]:
        subset = [r for r in rows if r["ensemble_size"]==M]
        good = [r for r in subset if r["accepted"]]
        full = sum(r["full_order"] for r in subset)
        sign = sum(r["kernel_nonpositive"] for r in good)
        mismatch = sum(r["good_vacf_bad_kernel"] for r in good)
        med, med_status = kernel_median(good)
        summary.append({
            "ensemble_size":M,"trials":len(subset),
            "full_order_accepted":full,"full_order_rate":full/len(subset),
            "full_order_wilson95":wilson(full,len(subset)),
            "fallback_accepted":len(good),"fallback_acceptance_rate":len(good)/len(subset),
            "fallback_wilson95":wilson(len(good),len(subset)),
            "accepted_order_counts":dict(sorted(Counter(r["accepted_n"] for r in good).items())),
            "median_vacf_rmse":float(np.median([r["vacf_rmse"] for r in good])) if good else None,
            "median_kernel_log_rmse":med,"median_kernel_log_rmse_status":med_status,
            "kernel_nonpositive_count":sign,"kernel_nonpositive_wilson95":wilson(sign,len(good)),
            "good_vacf_bad_kernel":mismatch,"good_vacf_bad_kernel_wilson95":wilson(mismatch,len(good)),
            "good_vacf_bad_kernel_rate_among_accepted":mismatch/len(good) if good else None,
            "median_y1_adjustment_over_sampling_sd":float(np.median([r["y1_adjustment_over_sampling_sd"] for r in good])) if good else None,
        })
    check("all trials accounted for",len(rows)==len(p["ensemble_sizes"])*p["replicates_per_size"],len(rows))
    check("accepted-state inventory",len(states)==sum(r["accepted"] for r in rows),len(states))
    check("every attempt has explicit reason",all(x["reason"] for x in attempts),len(attempts))
    check("kernel sign-status accounting",
          all((r["kernel_log_rmse"] is None)==bool(r["kernel_nonpositive"])
              for r in rows if r["accepted"]),sum(r["kernel_nonpositive"] or 0 for r in rows))
    # CSV is a plain machine-readable results table; null is an empty cell.
    with (OUT/"trials.csv").open("w",newline="",encoding="utf-8") as stream:
        writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    np.savez_compressed(OUT/"inputs_and_models.npz",noisy_moments=np.array(input_blocks),
                        empirical_covariances=np.array(all_covariances),
                        true_covariance=target,ensemble_sizes=p["ensemble_sizes"],
                        accepted_ids=np.array(ids,dtype=int),systems=np.array(states),
                        t_vacf=tv,vacf_true=cv,t_kernel=tk,kernel_true=kernel)
    fig,axes = plt.subplots(2,2,figsize=(12,8.2))
    sizes = np.array(p["ensemble_sizes"])
    ax=axes[0,0]
    for prefix,label,style in [("full_order","n=10 only","o-"),("fallback","order + window fallback","s--")]:
        counts=np.array([s["full_order_accepted" if prefix=="full_order" else "fallback_accepted"] for s in summary])
        rates=counts/p["replicates_per_size"]
        cis=np.array([wilson(int(c),p["replicates_per_size"]) for c in counts])
        ax.errorbar(sizes,rates,yerr=np.maximum(0,np.array([rates-cis[:,0],cis[:,1]-rates])),
                    fmt=style,capsize=3,label=label)
    ax.set(xscale="log",xlabel="independent trajectory vectors",ylabel="acceptance fraction",
           ylim=(-.03,1.03),title="Restricted implementation: acceptance")
    ax.legend(frameon=False,fontsize=8)
    ax=axes[0,1]
    order_counts=np.array([[s["accepted_order_counts"].get(n,0) for s in summary]
                          for n in range(p["minimum_n"],nmax+1)])
    bottom=np.zeros(len(sizes))
    for n,counts in zip(range(p["minimum_n"],nmax+1),order_counts):
        if np.any(counts):
            ax.bar(np.arange(len(sizes)),counts,bottom=bottom,label=f"n={n}")
            bottom+=counts
    ax.set(xticks=np.arange(len(sizes)),xticklabels=sizes,xlabel="ensemble size",
           ylabel="accepted fits",title="Order selection also truncates the window")
    ax.legend(frameon=False,fontsize=8)
    ax=axes[1,0]
    signs=np.array([s["kernel_nonpositive_count"] for s in summary])
    accepted=np.array([s["fallback_accepted"] for s in summary])
    ax.bar(np.arange(len(sizes)),signs,color="#D55E00",label="kernel crosses/below zero")
    ax.bar(np.arange(len(sizes)),accepted-signs,bottom=signs,color="#009E73",label="positive throughout grid")
    ax.set(xticks=np.arange(len(sizes)),xticklabels=sizes,xlabel="ensemble size",
           ylabel="accepted fits",title="Sign mismatches remain in the accounting")
    ax.legend(frameon=False,fontsize=8)
    ax=axes[1,1]
    finite=[r for r in rows if r["accepted"] and not r["kernel_nonpositive"]]
    for M in sizes:
        chosen=[r for r in finite if r["ensemble_size"]==M]
        ax.scatter([r["vacf_rmse"] for r in chosen],[r["kernel_log_rmse"] for r in chosen],
                   s=18,alpha=.65,label=str(M))
    ax.axvline(evaluation["good_vacf_rmse_threshold"],color="black",ls=":",lw=.8)
    ax.axhline(evaluation["bad_kernel_log_rmse_threshold"],color="black",ls=":",lw=.8)
    ax.set(xscale="log",yscale="log",xlabel="regularized VACF RMSE",ylabel="kernel log-RMSE",
           title=f"Positive kernels only ({len(finite)}); sign cases at left")
    ax.legend(title="ensemble",frameon=False,fontsize=8)
    fig.suptitle("Noisy subdiffusion reconstruction — audited restricted method",fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT/"noisy_memory_stress.png",dpi=180)
    plt.close(fig)
    clean_public={k:v for k,v in clean.items() if not isinstance(v,np.ndarray)}
    result={
        "study":p["title"],"protocol_version":p["version"],
        "protocol_sha256":sha256(PROTOCOL),"script_sha256":sha256(__file__),
        "reference_script_sha256":sha256(HERE/"27_thermal_memory_reproduction.py"),
        "environment":{"python":platform.python_version(),"numpy":np.__version__,
                       "scipy":scipy.__version__,"matplotlib":matplotlib.__version__},
        "clean_reference":clean_public,"total_trials":len(rows),"total_attempts":len(attempts),
        "summary":summary,
        "terminal_failure_counts":dict(Counter(r["final_reason"] for r in rows if not r["accepted"])),
        "all_attempt_reason_counts":dict(Counter(r["reason"] for r in attempts)),
        "checks":checks,"passed_checks":len(checks),"scope":p["interpretation_limits"],
    }
    (OUT/"results.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
