"""Post-hoc exact covariance ambiguity for finite independent-pair experiments."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("family_reference", HERE/"20_family_rejection.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
OUT = HERE/"results"/"sensor_calibration"


def main():
    p = {"temperature": 1., "stiffness": 1., "force_frequency": 2*np.pi}
    changed, nominal = {"alias": 1., "decay": .13}, {"alias": 1., "decay": .2}
    noise_variance = .35**2
    lags = [.6, .85, 1.]
    checks, rows = {}, []
    def check(name, error, tolerance=1e-10):
        checks[name] = {"error": float(error), "tolerance": tolerance, "passed": bool(error < tolerance)}
    for t in lags:
        c1, c0 = ref.covariance(p, changed, t), ref.covariance(p, nominal, t)
        delta = c1-c0
        colored_noise = np.array([[noise_variance, delta], [delta, noise_variance]])
        observed_changed = np.array([[1+noise_variance, c1], [c1, 1+noise_variance]])
        observed_nominal = np.array([[1., c0], [c0, 1.]])+colored_noise
        check("same_observed_covariance_"+str(t), np.max(abs(observed_changed-observed_nominal)))
        check("positive_noise_covariance_"+str(t), 0. if np.min(np.linalg.eigvalsh(colored_noise)) > 0 else 1.)
        check("unchanged_noise_variance_"+str(t), np.max(abs(np.diag(colored_noise)-noise_variance)))
        point = np.array([.3, -.7])
        def log_density(s):
            return -np.log(2*np.pi)-.5*np.linalg.slogdet(s)[1]-.5*point@np.linalg.solve(s, point)
        check("same_gaussian_log_density_"+str(t), abs(log_density(observed_changed)-log_density(observed_nominal)))
        rows.append({"lag": t, "nominal_signal_covariance": c0, "changed_signal_covariance": c1,
                     "required_sensor_cross_covariance": delta,
                     "required_sensor_correlation": delta/noise_variance,
                     "sensor_covariance_eigenvalues": np.linalg.eigvalsh(colored_noise).tolist(),
                     "observed_covariance": observed_changed.tolist()})
    chi0, chi1 = ref.response(p, nominal), ref.response(p, changed)
    error = float(abs(chi0-chi1)/abs(chi1))
    report = {
        "analysis_type": "post-hoc constructive identifiability example; not part of frozen benchmark outcomes",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_sha256": hashlib.sha256((HERE/"20_family_rejection.py").read_bytes()).hexdigest(),
        "models": {
            "A": "Changed physical damping 0.13, independent sensor noise variance 0.1225.",
            "B": "Nominal physical damping 0.20, same marginal sensor variance, specified correlated errors within each dynamic pair."},
        "calibration": "Each calibration trial is one isolated noise-only reading N(0,0.1225), independent of all other trials in both models.",
        "sampling": "Each dynamic pair is a freshly prepared independent trial; sensor errors are independent of signal and other trials. The within-pair error correlation may depend on the scheduled lag.",
        "scope": "This defines valid finite independent-pair experiment laws. No single stationary colored-noise process across an uninterrupted trajectory is constructed or claimed.",
        "identifiability": "All measured Gaussian pair laws and isolated calibration laws coincide. Their arbitrary independent products coincide. No test on these observations can distinguish A from B with power greater than its size under B.",
        "remedy": "Noise-only calibration PAIRS at the same lags would have cross covariance zero in A and delta in B, provided their noise law transfers to dynamic measurement.",
        "relative_response_error_using_B_when_A_true": error,
        "half_response_distance_absolute": float(abs(chi0-chi1)/2),
        "response_A": [float(chi1.real), float(chi1.imag)],
        "response_B": [float(chi0.real), float(chi0.imag)],
        "checks": checks, "all_checks_passed": all(v["passed"] for v in checks.values()), "lags": rows}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"correlated_sensor_counterexample.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    assert report["all_checks_passed"]


if __name__ == "__main__":
    main()
