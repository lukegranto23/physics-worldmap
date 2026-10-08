"""Reproduce a limited set of SI electromagnetism worked examples.

Requires NumPy and SciPy; writes only ../electromagnetism-checks.json. Numerical
quadratures, numerical field derivatives, balances, and deliberate sign-error
controls check selected examples, not all of electromagnetism or new physics.
The ideal capacitor and solenoid omit fringing; the resistor is quasistatic.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy import constants
from scipy.integrate import quad


EPS0, MU0, C = constants.epsilon_0, constants.mu_0, constants.c
H = 1e-25


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def close(actual, expected, label, *, rtol=2e-9, atol=0.0):
    require(np.allclose(actual, expected, rtol=rtol, atol=atol),
            f"{label}: actual={actual!r}; expected={expected!r}")


def derivative(function, point, axis):
    """Complex-step first derivative; only analytic functions are passed here."""
    shifted = np.array(point, dtype=complex)
    shifted[axis] += 1j * H
    return np.imag(function(shifted)) / H


def curl(function, point):
    dx, dy, dz = [derivative(function, point, axis) for axis in range(3)]
    return np.array([dy[2] - dz[1], dz[0] - dx[2], dx[1] - dy[0]])


def divergence(function, point):
    return sum(derivative(function, point, axis)[axis] for axis in range(3))


def check_si_dimensions():
    # Exponent order: mass, length, time, electric current. Temperature unused.
    E = np.array([1, 1, -3, -1])
    B = np.array([1, 0, -2, -1])
    epsilon = np.array([-1, -3, 4, 2])
    mu = np.array([1, 1, -2, -2])
    length, time = np.array([0, 1, 0, 0]), np.array([0, 0, 1, 0])
    rho, current_density = np.array([0, -3, 1, 1]), np.array([0, -2, 0, 1])
    energy_density, power_flux = np.array([1, -1, -2, 0]), np.array([1, 0, -3, 0])
    relations = {
        "electric Gauss": (E - length, rho - epsilon),
        "Faraday": (E - length, B - time),
        "Ampere conduction": (B - length, mu + current_density),
        "Ampere displacement": (B - length, mu + epsilon + E - time),
        "electric energy density": (epsilon + 2 * E, energy_density),
        "magnetic energy density": (2 * B - mu, energy_density),
        "Poynting flux": (E + B - mu, power_flux),
        "local Joule power": (current_density + E, energy_density - time),
    }
    for name, (left, right) in relations.items():
        require(np.array_equal(left, right), name)
    # SciPy's separately tabulated decimal values have rounding, even though
    # the defining relation is exact. Do not demand tighter than tabulation.
    close(EPS0 * MU0 * C**2, 1.0, "vacuum SI constant consistency", rtol=2e-11)
    return {"relations": list(relations), "dimension_exponents": "M,L,T,I",
            "epsilon0_mu0_c_squared": EPS0 * MU0 * C**2,
            "scope": "Dimensional consistency does not establish field equations."}


def check_uniform_charged_sphere():
    charge, radius = 5e-9, 0.1
    density = charge / (4 * np.pi * radius**3 / 3)
    rows = []
    for r in (0.05, 0.20):
        # Direct axial Coulomb volume integral, dimensionless source radius s.
        # Splitting the outer integral at the field point handles the shell jump.
        x = r / radius
        def shell(s):
            angular = quad(lambda u: (x - s*u) / (x*x + s*s - 2*x*s*u)**1.5,
                           -1, 1, epsabs=2e-10, epsrel=2e-10, limit=150)[0]
            return s*s * angular
        bounds = [0, x, 1] if x < 1 else [0, 1]
        integral = sum(quad(shell, lo, hi, epsabs=2e-9, epsrel=2e-9,
                            limit=150)[0] for lo, hi in zip(bounds[:-1], bounds[1:]))
        from_coulomb = density * radius / (2 * EPS0) * integral
        enclosed = charge * min(1.0, x**3)
        from_gauss = enclosed / (4 * np.pi * EPS0 * r*r)
        close(from_coulomb, from_gauss, "Coulomb volume integral versus Gauss", rtol=2e-7)
        rows.append({"r_m": r, "field_Coulomb_V_per_m": from_coulomb,
                     "field_Gauss_V_per_m": from_gauss,
                     "relative_error": abs(from_coulomb / from_gauss - 1),
                     "enclosed_charge_C": enclosed})
    field = lambda p: density * np.array(p[:3]) / (3 * EPS0)
    divE = divergence(field, [0.021, -0.017, 0.009, 0.0])
    close(EPS0 * divE, density, "local volume charge density")
    return {"Q_C": charge, "R_m": radius, "rho_C_per_m3": density,
            "samples": rows, "divergence_inferred_rho_C_per_m3": EPS0 * divE}


def check_gauss_off_center_flux():
    radius, charge = 0.14, 3e-9
    rows = []
    for offset in (0.37 * radius, 1.7 * radius):
        # Direct normal component of a displaced point charge on a sphere.
        integral, error = quad(
            lambda u: (radius - offset*u) /
            (radius*radius + offset*offset - 2*radius*offset*u)**1.5,
            -1, 1, epsabs=1e-10, epsrel=1e-11)
        inferred_charge = charge * radius*radius * integral / 2
        expected = charge if offset < radius else 0.0
        close(inferred_charge, expected, "enclosed versus external charge flux", atol=1e-20)
        rows.append({"offset_m": offset, "epsilon0_flux_C": inferred_charge,
                     "expected_enclosed_C": expected, "quadrature_estimated_error_integral": error})
    return {"radius_m": radius, "source_charge_C": charge, "samples": rows}


def check_local_charge_conservation():
    # An explicitly constructed curl-free E and B=0. Ampere fixes J=-eps0 E_t.
    # Positive divergence current must decrease charge density (minus sign).
    a, b, omega = 120.0, -85.0, 270.0
    def current(p):
        x, y, _, t = p
        return EPS0 * np.array([a*x*omega*np.sin(omega*t),
                                -b*y*omega*np.cos(omega*t), 0.0])
    def rho(p):
        return EPS0 * (a*np.cos(omega*p[3]) + b*np.sin(omega*p[3]))
    point = [0.021, 0.033, -0.01, 0.004]
    rho_dot, divJ = derivative(rho, point, 3), divergence(current, point)
    close(rho_dot, -divJ, "differential continuity")
    edge = 0.06
    # Independent surface integral over the six cube faces (uniform per face).
    outward = 0.0
    for axis in range(3):
        for sign in (-1, 1):
            sample = np.array([0., 0., 0., point[3]])
            sample[axis] = sign*edge/2
            outward += sign * current(sample)[axis] * edge**2
    close(outward, -rho_dot * edge**3, "integrated current versus charge loss")
    require(abs(rho_dot - divJ) > abs(rho_dot), "wrong continuity sign must be detected")
    return {"rho_dot_C_per_m3_s": float(rho_dot), "divJ_A_per_m3": float(divJ),
            "outward_current_A": outward, "charge_loss_rate_A": float(-rho_dot*edge**3),
            "relative_continuity_residual": float(abs(rho_dot+divJ)/abs(rho_dot))}


def check_capacitor_displacement_current():
    plate_radius, gap, current = 0.020, 0.001, 0.010
    area = np.pi * plate_radius**2
    # Derive field rate from time-dependent plate charge before forming B.
    field = lambda t: (7e-9 + current*t) / (EPS0*area)
    dt = 1e-7
    field_rate = (field(dt) - field(-dt)) / (2*dt)
    displacement, quadrature_error = quad(lambda r: EPS0*field_rate*2*np.pi*r,
                                         0, plate_radius, epsabs=1e-15)
    close(displacement, current, "equal conduction and full-gap displacement current")
    samples = []
    for r in (0.010, 0.030):
        effective_radius = min(r, plate_radius)
        enclosed_displacement = quad(lambda s: EPS0*field_rate*2*np.pi*s,
                                     0, effective_radius, epsabs=1e-15)[0]
        B = MU0 * enclosed_displacement / (2*np.pi*r)
        expected = MU0*current/(2*np.pi*r)*min(1, r*r/plate_radius**2)
        close(B, expected, "Ampere surfaces across wire and capacitor gap")
        samples.append({"r_m": r, "B_phi_T": B, "enclosed_current_A": enclosed_displacement})
    return {"plate_radius_m": plate_radius, "gap_m": gap, "wire_current_A": current,
            "field_rate_V_per_m_s": field_rate, "integrated_displacement_current_A": displacement,
            "current_integral_error_A": quadrature_error, "samples": samples,
            "scope": "Ideal uniform circular gap; quasistatic, no fringing or radiation."}


def check_faraday_solenoid():
    radius, Bdot = 0.03, 0.20
    rows = []
    for r in (0.01, 0.06):
        Ephi = -0.5*Bdot*(r if r < radius else radius*radius/r)
        # Positively oriented CCW loop viewed from +z.
        circulation = quad(lambda phi: Ephi*r, 0, 2*np.pi, epsabs=1e-15)[0]
        flux_rate = quad(lambda s: Bdot*2*np.pi*s, 0, min(r, radius), epsabs=1e-15)[0]
        close(circulation, -flux_rate, "Faraday loop orientation")
        h = 1e-6
        def rE(s):
            return -0.5*Bdot*(s*s if s < radius else radius*radius)
        numerical_curl = (rE(r+h) - rE(r-h))/(2*h*r)
        expected_curl = -Bdot if r < radius else 0.0
        close(numerical_curl, expected_curl, "Faraday local curl away from current sheet",
              atol=1e-10, rtol=1e-8)
        require(abs(circulation-flux_rate) > abs(flux_rate), "wrong Faraday sign must fail")
        rows.append({"r_m": r, "E_phi_V_per_m": Ephi, "emf_V": circulation,
                     "minus_flux_rate_V": -flux_rate, "curlE_T_per_s": numerical_curl})
    return {"solenoid_radius_m": radius, "Bdot_T_per_s": Bdot,
            "orientation": "positive circulation CCW as viewed from +z", "samples": rows,
            "scope": "Ideal infinitely long solenoid, uniform internal B, zero external B."}


def check_motional_emf_and_power():
    length, speed, B, resistance = 0.25, 3.0, 0.4, 2.0
    velocity, magnetic = np.array([speed, 0., 0.]), np.array([0., 0., B])
    # Move right, B out of page: v cross B drives current down the moving rod.
    tangent = np.array([0., -1., 0.])
    emf = quad(lambda s: float(np.cross(velocity, magnetic) @ tangent), 0, length)[0]
    current = emf/resistance
    force = current*length*np.cross(tangent, magnetic)
    required_power = -float(force @ velocity)
    joule = current*current*resistance
    close(emf, 0.3, "rod emf independently integrated")
    close(force, [-0.015, 0., 0.], "magnetic drag direction", atol=1e-15)
    close(required_power, joule, "mechanical input and Joule output")
    # Magnetic force is perpendicular to any single instantaneous particle velocity.
    particle_velocity = np.array([speed, -0.017, 0.009])
    magnetic_work = float(np.cross(particle_velocity, magnetic) @ particle_velocity)
    close(magnetic_work, 0.0, "magnetic Lorentz force does no particle work", atol=1e-16)
    return {"emf_V": emf, "current_A": current, "rod_magnetic_force_N": force.tolist(),
            "mechanical_input_W": required_power, "Joule_power_W": joule,
            "particle_magnetic_work_per_unit_charge_W_per_C": magnetic_work}


def check_resistor_poynting_flux():
    radius, length, conductivity, current = 0.00050, 0.12, 2.0e6, 0.80
    area = np.pi*radius**2
    E = current/(conductivity*area)
    # Surface normal rhat=xhat at one point; E along z, B along +y => S=-x.
    Evec, Bvec = np.array([0., 0., E]), np.array([0., MU0*current/(2*np.pi*radius), 0.])
    S = np.cross(Evec, Bvec)/MU0
    inward = -quad(lambda z: S[0]*2*np.pi*radius, 0, length, epsabs=1e-13)[0]
    local_heat = quad(lambda r: conductivity*E*E*2*np.pi*r*length,
                      0, radius, epsabs=1e-13)[0]
    resistance = length/(conductivity*area)
    circuit_heat = current*current*resistance
    close(inward, local_heat, "Poynting surface flux and volume Joule heating")
    close(inward, circuit_heat, "field energy and I squared R")
    require(S[0] < 0, "energy must flow inward through side wall")
    # Local divergence: S_r=-sigma E^2 r/2, hence div S=-sigma E^2.
    h, r = 1e-8, 0.3*radius
    rS = lambda s: -conductivity*E*E*s*s/2
    divS = (rS(r+h)-rS(r-h))/(2*h*r)
    close(divS, -conductivity*E*E, "local steady Poynting balance", rtol=1e-8)
    return {"radius_m": radius, "length_m": length, "sigma_S_per_m": conductivity,
            "current_A": current, "E_z_V_per_m": E, "B_surface_T": float(Bvec[1]),
            "S_radial_W_per_m2": float(S[0]), "resistance_ohm": resistance,
            "inward_field_power_W": inward, "volume_Joule_power_W": local_heat,
            "circuit_power_W": circuit_heat, "local_balance_error_W_per_m3": float(divS+conductivity*E*E)}


def plane_fields(peak, frequency):
    omega, k = 2*np.pi*frequency, 2*np.pi*frequency/C
    def E(p):
        return np.array([peak*np.cos(k*p[2]-omega*p[3]), 0., 0.])
    def B(p):
        return np.array([0., peak/C*np.cos(k*p[2]-omega*p[3]), 0.])
    return E, B


def check_vacuum_plane_wave():
    peak, frequency, detector_area = 12.0, 150e6, 0.0008
    E, B = plane_fields(peak, frequency)
    point = [0.02, 0.03, 0.17*C/frequency, 0.13/frequency]
    Faraday = curl(E, point) + derivative(B, point, 3)
    Ampere = curl(B, point) - EPS0*MU0*derivative(E, point, 3)
    faraday_scale = 2*np.pi*frequency*peak/C
    ampere_scale = 2*np.pi*frequency*peak/C**2
    close(Faraday, [0., 0., 0.], "plane-wave Faraday", atol=1e-12*faraday_scale)
    close(Ampere, [0., 0., 0.], "plane-wave Ampere", atol=1e-12*ampere_scale)
    close(divergence(E, point), 0., "plane-wave electric divergence", atol=1e-20)
    close(divergence(B, point), 0., "plane-wave magnetic divergence", atol=1e-20)
    average = frequency*quad(lambda t: np.cross(E([0,0,0,t]), B([0,0,0,t]))[2]/MU0,
                             0, 1/frequency, epsabs=1e-18, epsrel=1e-12)[0]
    expected = EPS0*C*peak*peak/2
    close(average, expected, "cycle-integrated intensity")
    require(average > 0, "wave energy flux must point in propagation direction")
    wrong_sign = curl(E, point) - derivative(B, point, 3)
    require(np.linalg.norm(wrong_sign) > 0.1*faraday_scale, "reversed B must fail Maxwell")
    return {"frequency_Hz": frequency, "peak_E_V_per_m": peak, "peak_B_T": peak/C,
            "wavelength_m": C/frequency, "average_intensity_W_per_m2": average,
            "detector_area_m2": detector_area, "incident_power_W": average*detector_area,
            "Faraday_relative_residual": float(np.linalg.norm(Faraday)/faraday_scale),
            "Ampere_relative_residual": float(np.linalg.norm(Ampere)/ampere_scale)}


def check_standing_wave_local_energy():
    peak, frequency = 12.0, 150e6
    omega, k, wavelength, period = 2*np.pi*frequency, 2*np.pi*frequency/C, C/frequency, 1/frequency
    def E(p):
        return np.array([2*peak*np.cos(k*p[2])*np.cos(omega*p[3]), 0., 0.])
    def B(p):
        return np.array([0., 2*peak/C*np.sin(k*p[2])*np.sin(omega*p[3]), 0.])
    def energy(p):
        return (EPS0*np.dot(E(p), E(p)) + np.dot(B(p), B(p))/MU0)/2
    def flux(p):
        return np.cross(E(p), B(p))/MU0
    residuals = []
    for zfraction, tfraction in ((.17,.13), (.31,.22), (.09,.43), (.45,.38)):
        point = [0.,0.,zfraction*wavelength,tfraction*period]
        udot = derivative(energy, point, 3)
        divS = divergence(flux, point)
        close(udot, -divS, "standing-wave local Poynting balance", rtol=1e-11)
        residuals.append(float(abs(udot+divS)/(EPS0*peak*peak*omega)))
    stored = [quad(lambda z: energy([0,0,z,t]), 0, wavelength, epsabs=1e-18)[0]
              for t in (0., .13*period, .37*period, .5*period)]
    close(stored, EPS0*peak*peak*wavelength, "energy integrated over a spatial period", rtol=1e-11)
    average_flux = quad(lambda tau: flux([0,0,.17*wavelength,tau*period])[2],
                        0, 1, epsabs=1e-13)[0]
    close(average_flux, 0, "standing wave cycle-averaged flux", atol=1e-12)
    instantaneous = float(flux([0,0,.17*wavelength,.13*period])[2])
    require(abs(instantaneous) > .01, "zero average flux must not erase local energy transport")
    return {"energy_per_transverse_area_J_per_m2": stored,
            "maximum_normalized_local_balance_residual": max(residuals),
            "instantaneous_flux_at_sample_W_per_m2": instantaneous,
            "time_averaged_flux_at_sample_W_per_m2": average_flux,
            "scope": "Equal coherent counterpropagating monochromatic vacuum plane waves."}


def check_uniform_field_gauge():
    field, x, time, charge = 75., 0.024, 0.004, 2e-9
    phi = lambda p: -field*p[0]
    chi = lambda p: -field*p[0]*p[3]
    transformed_phi = lambda p: 0.*p[0]
    transformed_A = lambda p: np.array([-field*p[3], 0., 0.])
    point = [x,0.,0.,time]
    original_E = -np.array([derivative(phi, point, i) for i in range(3)])
    transformed_E = -np.array([derivative(transformed_phi, point, i) for i in range(3)]) - derivative(transformed_A, point, 3)
    close(original_E, transformed_E, "uniform-field potential gauges", atol=1e-14)
    close(curl(transformed_A, point), [0,0,0], "transformed vector potential has no B", atol=1e-14)
    work = quad(lambda location: charge*original_E[0], 0, x, epsabs=1e-20)[0]
    close(work, -charge*(phi(point)-phi([0,0,0,time])), "electric work versus potential difference")
    grad_chi = np.array([derivative(chi, point, i) for i in range(3)])
    mass, velocity = 1e-6, np.array([.2,-.1,.05])
    initial_canonical = mass*velocity
    transformed_canonical = initial_canonical + charge*grad_chi
    close(transformed_canonical-charge*transformed_A(point), mass*velocity,
          "gauge-invariant kinetic momentum")
    return {"original_phi_V": phi(point), "gauge_chi_V_s": chi(point),
            "transformed_A_V_s_per_m": transformed_A(point).tolist(),
            "force_x_N": float(charge*original_E[0]), "work_J": work,
            "canonical_momentum_change_kg_m_per_s": (charge*grad_chi).tolist()}


def check_nontrivial_gauge_and_action():
    # Nonuniform, time-dependent potentials and a nonlinear gauge; SI coefficients.
    length, omega, chi0, chi1, B0, A0, charge = .4, 3.7, .023, -.017, .13, .08, 2e-9
    def phi(p):
        x,y,z,t = p
        return 1.2*x*y + .7*z*np.cos(omega*t)
    def A(p):
        x,y,_,t = p
        return np.array([-B0*y/2, B0*x/2, A0*np.sin(x/length-omega*t)])
    def chi(p):
        x,y,z,t = p
        return chi0*x*x*y/length**3*np.cos(omega*t) + chi1*z/length*np.sin(omega*t)
    def grad_chi(p):
        x,y,_,t = p
        return np.array([2*chi0*x*y/length**3*np.cos(omega*t),
                         chi0*x*x/length**3*np.cos(omega*t),
                         chi1/length*np.sin(omega*t)])
    def chi_t(p):
        x,y,z,t = p
        return -chi0*omega*x*x*y/length**3*np.sin(omega*t) + chi1*omega*z/length*np.cos(omega*t)
    changed_A = lambda p: A(p)+grad_chi(p)
    changed_phi = lambda p: phi(p)-chi_t(p)
    point = [.13,-.17,.23,.19]
    def electric(potential, vector):
        return -np.array([derivative(potential, point, i) for i in range(3)])-derivative(vector,point,3)
    E, Ep = electric(phi,A), electric(changed_phi,changed_A)
    B, Bp = curl(A,point), curl(changed_A,point)
    close(Ep,E,"nonlinear gauge E invariance",atol=1e-13)
    close(Bp,B,"nonlinear gauge B invariance",atol=1e-13)
    def trajectory(t):
        return np.array([.1+.03*np.sin(t), -.2+.05*t*t, .15*np.cos(.7*t), t])
    def velocity(t):
        return np.array([.03*np.cos(t), .10*t, -.105*np.sin(.7*t)])
    def action_difference(t):
        p, v = trajectory(t), velocity(t)
        # Mechanical kinetic term cancels; compute the two interaction terms.
        return charge*((changed_A(p)-A(p))@v-(changed_phi(p)-phi(p)))
    t0,t1 = .03,1.4
    integrated = quad(action_difference,t0,t1,epsabs=1e-21,epsrel=1e-11)[0]
    endpoint = charge*(chi(trajectory(t1))-chi(trajectory(t0)))
    close(integrated,endpoint,"particle Lagrangian gauge term is endpoint-only",rtol=1e-10,atol=1e-21)
    wrong_phi = lambda p: phi(p)+chi_t(p)
    wrong_error = float(np.linalg.norm(electric(wrong_phi,changed_A)-E))
    require(wrong_error > .01,"wrong scalar-potential sign must be detected")
    return {"E_invariance_error_V_per_m": float(np.linalg.norm(Ep-E)),
            "B_invariance_error_T": float(np.linalg.norm(Bp-B)),
            "integrated_action_change_J_s": integrated,"endpoint_action_change_J_s": endpoint,
            "wrong_gauge_sign_E_error_V_per_m": wrong_error}


def check_dielectric_free_and_total_charge():
    # Planar interface, n from medium1 to medium2. Linear isotropic dielectrics.
    epsr1, epsr2, E1n, sigma_free, tangential_E = 2.0, 5.0, 130., 3e-9, 40.
    E2n = (EPS0*epsr1*E1n+sigma_free)/(EPS0*epsr2)
    P1n, P2n = EPS0*(epsr1-1)*E1n, EPS0*(epsr2-1)*E2n
    sigma_bound = P1n-P2n
    from_D = EPS0*(epsr2*E2n-epsr1*E1n)
    from_E = EPS0*(E2n-E1n)
    close(from_D,sigma_free,"D jump equals free sheet charge")
    close(from_E,sigma_free+sigma_bound,"epsilon0 E jump equals total sheet charge",atol=1e-23)
    # A shrinking rectangular electrostatic loop gives E2_t=E1_t; D_t need not agree.
    width,height = .013,1e-7
    loop = tangential_E*width+E2n*height-tangential_E*width-E2n*height
    close(loop,0.,"tangential electrostatic loop",atol=1e-15)
    require(abs(from_E-sigma_free) > .5*abs(sigma_free),"confusing free with total charge must fail")
    return {"relative_permittivities": [epsr1,epsr2],"normal_E1_V_per_m": E1n,
            "normal_E2_V_per_m": E2n,"sigma_free_C_per_m2": sigma_free,
            "sigma_bound_C_per_m2": sigma_bound,"sigma_total_C_per_m2": sigma_free+sigma_bound,
            "normal_D_jump_C_per_m2": from_D,"epsilon0_normal_E_jump_C_per_m2": from_E,
            "tangential_E_both_V_per_m": tangential_E,
            "scope": "Static planar interface; linear, isotropic, nondispersive constitutive relation."}


def check_capacitor_energy_and_force():
    area,gap,voltage = .004,.0012,40.
    capacitance=EPS0*area/gap
    charge=capacitance*voltage
    E=voltage/gap
    field_energy=quad(lambda z: EPS0*E*E*area/2,0,gap,epsabs=1e-20)[0]
    charging_work=quad(lambda q: q/capacitance,0,charge,epsabs=1e-20)[0]
    close(field_energy,charging_work,"field energy equals quasistatic charging work")
    # Fixed charge, unlike fixed voltage: differentiate the appropriate field energy.
    h=gap*1e-5
    fixed_charge_energy=lambda d: charge*charge*d/(2*EPS0*area)
    separation_force=-(fixed_charge_energy(gap+h)-fixed_charge_energy(gap-h))/(2*h)
    pressure=EPS0*E*E/2
    close(separation_force,-pressure*area,"attractive Maxwell pressure and fixed-Q virtual work",rtol=1e-9)
    # A second apparatus is voltage-controlled; include its ideal voltage source.
    # Differentiating field energy alone at fixed V predicts the wrong force.
    area_v,gap_v,voltage_v = .010,.002,100.
    q_v=lambda d: EPS0*area_v*voltage_v/d
    u_v=lambda d: EPS0*area_v*voltage_v**2/(2*d)
    effective=lambda d: u_v(d)-voltage_v*q_v(d)
    h_v=gap_v*1e-5
    correct_v_force=-(effective(gap_v+h_v)-effective(gap_v-h_v))/(2*h_v)
    wrong_v_force=-(u_v(gap_v+h_v)-u_v(gap_v-h_v))/(2*h_v)
    stress_force=lambda d: -EPS0*area_v*(voltage_v/d)**2/2
    close(correct_v_force,stress_force(gap_v),"fixed-V effective energy and attractive stress",rtol=2e-9)
    require(correct_v_force < 0 < wrong_v_force,"omitting fixed-V source must reverse the predicted force")
    final_gap=1.07*gap_v
    source_work=voltage_v*(q_v(final_gap)-q_v(gap_v))
    stored_change=u_v(final_gap)-u_v(gap_v)
    work_by_field=quad(stress_force,gap_v,final_gap,epsabs=1e-20,epsrel=1e-12)[0]
    close(source_work,stored_change+work_by_field,"source work equals stored change plus field mechanical work",rtol=1e-12)
    return {"area_m2": area,"gap_m": gap,"voltage_V": voltage,"charge_C": charge,
            "field_energy_J": field_energy,"charging_work_J": charging_work,
            "pressure_Pa": pressure,"force_in_increasing_gap_direction_N": separation_force,
            "fixed_voltage_example":{"area_m2":area_v,"initial_gap_m":gap_v,
                "final_gap_m":final_gap,"voltage_V":voltage_v,
                "effective_energy_force_N":correct_v_force,
                "Maxwell_stress_force_N":stress_force(gap_v),
                "wrong_field_energy_only_force_N":wrong_v_force,
                "voltage_source_work_J":source_work,"stored_field_energy_change_J":stored_change,
                "mechanical_work_by_field_J":work_by_field,
                "energy_balance_residual_J":source_work-stored_change-work_by_field},
            "scope": "Vacuum parallel plates, no fringing; fixed-charge and ideal-source fixed-voltage force calculations are distinguished."}


def main():
    tests = [check_si_dimensions,check_uniform_charged_sphere,check_gauss_off_center_flux,
             check_local_charge_conservation,check_capacitor_displacement_current,
             check_faraday_solenoid,check_motional_emf_and_power,check_resistor_poynting_flux,
             check_vacuum_plane_wave,check_standing_wave_local_energy,check_uniform_field_gauge,
             check_nontrivial_gauge_and_action,check_dielectric_free_and_total_charge,
             check_capacitor_energy_and_force]
    outcomes=[]
    for test in tests:
        try:
            outcomes.append({"check":test.__name__,"status":"PASS","values":test()})
        except Exception as exc:
            outcomes.append({"check":test.__name__,"status":"FAIL","error":str(exc)})
    source=Path(__file__).resolve()
    vault=source.parents[2]
    concept_dir=vault/"23 Electromagnetism"/"Concepts"
    note_names=["Maxwell Equations.md","Gausss Law.md","Faradays Law.md",
                "Poynting Theorem.md","Gauge Transformations.md","Electromagnetic Waves.md"]
    hashes={str(source.relative_to(vault)).replace("\\","/"):hashlib.sha256(source.read_bytes()).hexdigest()}
    for name in note_names:
        note=concept_dir/name
        if note.exists():
            hashes[str(note.relative_to(vault)).replace("\\","/")]=hashlib.sha256(note.read_bytes()).hexdigest()
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),
            "schema_version":1,"numpy_version":np.__version__,"scipy_version":scipy.__version__,
            "constants":{"epsilon0_F_per_m":EPS0,"mu0_H_per_m":MU0,"c_m_per_s":C,
                         "source":"scipy.constants; epsilon0 and mu0 are measured SI constants, not exactly their pre-2019 values"},
            "scope":"14 finite worked-example and consistency groups. Not a proof, a full note audit, full electromagnetism validation, experimental validation, or new physics.",
            "limitations":["Idealized field geometries and constitutive laws are stated per check.",
                           "Floating-point numerics and reported quadrature errors are not interval-certified proofs.",
                           "Only the specified examples and signs are tested; hashes identify note snapshots but do not validate every claim in them."],
            "source_sha256":hashes,"checks":outcomes,
            "passed_groups":sum(row["status"]=="PASS" for row in outcomes),"total_groups":len(outcomes)}
    target=source.parents[1]/"electromagnetism-checks.json"
    target.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,allow_nan=False))
    require(all(row["status"]=="PASS" for row in outcomes),"electromagnetism example check failed")


if __name__ == "__main__":
    main()
