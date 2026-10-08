"""Reproduce the mechanics/statistical-physics note checks.

Requires NumPy. Writes only ../foundation-checks.json. These finite examples
verify implementations and arithmetic, not the general theorems or new physics.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, label, atol=1e-10, rtol=1e-8):
    require(np.allclose(actual, expected, atol=atol, rtol=rtol), label)


def entropy(p):
    p = np.asarray(p)
    positive = p[p > 0]
    return float(-np.sum(positive * np.log(positive)))


def check_stationary_action():
    duration, epsilon = 4.0, 0.07
    t = np.linspace(0, duration, 20001)
    changes = []
    for mode in (1, 2):
        rate = mode * np.pi / duration
        q = epsilon * np.sin(rate * t)
        velocity = epsilon * rate * np.cos(rate * t)
        numerical = np.trapezoid(0.5 * (velocity**2 - q**2), t)
        exact = epsilon**2 * duration / 4 * (rate**2 - 1)
        close(numerical, exact, "stationary-action quadratic variation")
        changes.append(float(numerical))
    require(changes[0] < 0 < changes[1], "saddle needs both signs")
    return {"action_changes": changes, "pendulum_period_s": float(2*np.pi*np.sqrt(0.75/9.81))}


def check_legendre_oscillator():
    m, k, q0, p0 = 2.0, 18.0, 0.1, 0.6
    omega = np.sqrt(k/m)
    t = np.linspace(0, 20, 1001)
    q = q0*np.cos(omega*t)+p0/(m*omega)*np.sin(omega*t)
    p = p0*np.cos(omega*t)-m*omega*q0*np.sin(omega*t)
    H = p*p/(2*m)+k*q*q/2
    close(H, 0.18, "oscillator energy")
    velocity = p/m
    L = m*velocity**2/2-k*q*q/2
    close(p*velocity-L, H, "Legendre transform")
    return {"energy_J": float(H[0]), "max_energy_error_J": float(np.max(abs(H-0.18)))}


def check_noether():
    m, q0, velocity = 2.3, -0.4, 0.7
    t = np.linspace(0, 7, 501)
    charge = m*velocity*t-m*(q0+velocity*t)
    close(charge, -m*q0, "boost boundary-term charge")
    x, y, kx, ky = 0.2, -0.1, 4.0, 9.0
    px, py, mass = 0.3, -0.2, 1.7
    derivative = (px/mass)*py + x*(-ky*y) - (py/mass)*px - y*(-kx*x)
    close(derivative, (kx-ky)*x*y, "broken rotation balance")
    close(derivative, 0.1, "torque sign and units")
    return {"boost_charge_kg_m": float(charge[0]), "broken_rotation_torque_Nm": derivative}


def check_phase_volume():
    h, steps = 0.1, 100
    explicit = np.array([[1., h], [-h, 1.]])
    symplectic = np.array([[1-h*h, h], [-h, 1.]])
    J = np.array([[0., 1.], [-1., 0.]])
    close(symplectic.T@J@symplectic, J, "symplectic two-form")
    close(np.linalg.det(symplectic), 1, "symplectic volume")
    close(np.linalg.det(explicit), 1+h*h, "Euler volume expansion")
    actual = np.linalg.det(np.linalg.matrix_power(explicit, steps))
    close(actual, (1+h*h)**steps, "accumulated Euler area")
    require(np.linalg.norm(explicit.T@J@explicit-J) > 1e-3, "negative control must fail")
    return {"explicit_area_factor_100_steps": float(actual),
            "symplectic_area_factor_100_steps": float(np.linalg.det(np.linalg.matrix_power(symplectic, steps)))}


def check_partition():
    x, h = 2.0, 1e-4
    logz = lambda y: np.logaddexp(0., -y)
    excited = 1/(1+np.exp(x))
    first = (logz(x+h)-logz(x-h))/(2*h)
    second = (logz(x+h)-2*logz(x)+logz(x-h))/h**2
    close(-first, excited, "partition first derivative", rtol=1e-7)
    close(second, excited*(1-excited), "partition variance", rtol=1e-6)
    levels_K, temperature = np.array([0., 120.]), 60.
    weights = np.exp(-levels_K/temperature)
    probabilities = weights/weights.sum()
    U_K = float(probabilities@levels_K)
    S = entropy(probabilities)
    C = x*x*excited*(1-excited)
    delta_T = 0.005
    mean = lambda T: 120/(1+np.exp(120/T))
    close((mean(temperature+delta_T)-mean(temperature-delta_T))/(2*delta_T),
          C, "heat-capacity temperature derivative", rtol=1e-7)
    shifted = np.exp(-(levels_K+37)/temperature)
    shifted /= shifted.sum()
    close(shifted, probabilities, "energy-zero invariance")
    close(S, float(logz(x)+U_K/temperature), "canonical entropy identity")
    return {"excited_probability": float(excited), "U_over_kB_K": U_K,
            "S_over_kB": S, "C_over_kB": float(C)}


def check_coarse_graining():
    p = np.array([0.4, 0.1, 0.2, 0.3])
    labels = np.array([p[:2].sum(), p[2:].sum()])
    reconstructed = np.repeat(labels/2, 2)
    increase = entropy(reconstructed)-entropy(p)
    divergence = np.sum(p*np.log(p/reconstructed))
    close(increase, divergence, "cell reconstruction KL identity")
    close(entropy(labels), np.log(2), "coarse label entropy")
    require(increase > 0, "coarse reconstructed entropy should increase")
    return {"fine_S_over_kB": entropy(p), "reconstructed_S_over_kB": entropy(reconstructed),
            "label_S_over_kB": entropy(labels), "increase_over_kB": float(increase)}


def check_free_energy():
    E_K, T = np.array([0., 120.]), 60.
    p = np.array([0.3, 0.7])
    z = np.exp(-E_K/T).sum()
    pi = np.exp(-E_K/T)/z
    excess = float(p@E_K-T*entropy(p)+T*np.log(z))
    divergence = float(np.sum(p*np.log(p/pi)))
    close(excess, T*divergence, "free-energy KL identity")
    require(excess > 0, "Gibbs state must minimize free energy here")
    return {"free_energy_excess_over_kB_K": excess, "relative_entropy_nats": divergence}


def check_quantum_entropy():
    rng = np.random.default_rng(20260904)
    A = rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
    H = (A+A.conj().T)/2
    energies, V = np.linalg.eigh(H)
    U = (V*np.exp(-1j*0.73*energies))@V.conj().T
    rho = np.diag([0.4, 0.3, 0.2, 0.1])
    final = U@rho@U.conj().T
    close(U.conj().T@U, np.eye(4), "unitarity")
    final_eigenvalues = np.linalg.eigvalsh(final)
    close(final_eigenvalues, [0.1,0.2,0.3,0.4], "unitary spectrum")
    change = entropy(final_eigenvalues)-entropy(np.diag(rho))
    close(change, 0, "global von Neumann entropy")
    return {"entropy_change_over_kB": change, "seed": 20260904}


def main():
    tests = [check_stationary_action, check_legendre_oscillator, check_noether,
             check_phase_volume, check_partition, check_coarse_graining,
             check_free_energy, check_quantum_entropy]
    outcomes = []
    for test in tests:
        try:
            data = test()
            outcomes.append({"check": test.__name__, "status": "PASS", "values": data})
        except Exception as exc:
            outcomes.append({"check": test.__name__, "status": "FAIL", "error": str(exc)})
    report = {"generated_utc": datetime.now(timezone.utc).isoformat(),
              "numpy_version": np.__version__, "checks": outcomes,
              "scope": "Finite worked-example checks; not general theorem proofs or new-physics tests"}
    target = Path(__file__).resolve().parents[1] / "foundation-checks.json"
    target.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    require(all(row["status"] == "PASS" for row in outcomes), "foundation check failed")


if __name__ == "__main__":
    main()
