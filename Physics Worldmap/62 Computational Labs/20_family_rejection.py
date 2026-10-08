"""Fresh-case family rejection: split likelihood and Gaussian concentration.

Established statistical controls, not general missing-physics detection.
"""
from __future__ import annotations
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "family_rejection_protocol.json"
OUT = HERE / "results" / "family_rejection"


def components(scenario):
    return scenario.get("components", [[scenario.get("alias", 1), scenario.get("decay", .2), 1.]])


def covariance(p, scenario, lag):
    value = 0.
    for alias, decay, weight in components(scenario):
        w = 2*np.pi*alias
        value += weight*np.exp(-decay*abs(lag))*(np.cos(w*lag)+decay/w*np.sin(w*abs(lag)))
    return value*p["temperature"]/p["stiffness"]


def response(p, scenario):
    value = 0j
    for alias, decay, weight in components(scenario):
        mass = p["stiffness"]/((2*np.pi*alias)**2+decay**2)
        w = p["force_frequency"]
        value += weight/(p["stiffness"]-mass*w*w+2j*decay*mass*w)
    return value


def ll(a, b, c, n, stats):
    """a,b diagonal covariance; c off-diagonal; stats=(sum x²,sum y²,sum xy)."""
    det = a*b-c*c
    return (-n*np.log(2*np.pi)-n/2*np.log(det)-
            (b*stats[:, 0]+a*stats[:, 1]-2*c*stats[:, 2])/(2*det))


def confidence(loglikes, alpha):
    top = np.max(loglikes, axis=1, keepdims=True)
    mix = top[:, 0]+np.log(np.mean(np.exp(loglikes-top), axis=1))
    return mix[:, None]-loglikes <= np.log(1/alpha)


def wilson(events):
    events = np.asarray(events, dtype=bool)
    n, k = events.size, int(np.sum(events))
    if n == 0:
        return None
    z = 1.959963984540054
    rate = k/n
    den = 1+z*z/n
    center = (rate+z*z/(2*n))/den
    half = z*np.sqrt(rate*(1-rate)/n+z*z/(4*n*n))/den
    return {"estimate": rate, "count": k, "total": n,
            "wilson95": [max(0., center-half), min(1., center+half)]}


def moment_acceptance(variance, crosses, n, stats, lag_count, alpha):
    x = np.log(4*lag_count/alpha)
    lower, upper = max(0., n-2*np.sqrt(n*x)), n+2*np.sqrt(n*x)+2*x
    plus = (stats[:, 0]+stats[:, 1]+2*stats[:, 2])/2
    minus = (stats[:, 0]+stats[:, 1]-2*stats[:, 2])/2
    qp = plus[:, None]/(variance+crosses[None, :])
    qm = minus[:, None]/(variance-crosses[None, :])
    return (qp>=lower)&(qp<=upper)&(qm>=lower)&(qm<=upper)


def main():
    raw = PROTOCOL.read_bytes()
    p = json.loads(raw)
    v = p["temperature"]/p["stiffness"]+p["measurement_noise_sd"]**2
    candidates = [{"alias": a, "decay": p["decay_rate"]} for a in p["candidate_aliases"]]
    responses = np.array([response(p, c) for c in candidates])
    r = p["replicates"]
    checks = {}

    def check(name, error, tol=1e-9):
        checks[name] = {"error": float(error), "tolerance": tol, "passed": bool(error < tol)}

    s = np.array([[2., 3., .4]])
    mat = np.array([[1.2, .2], [.2, .9]])
    direct = -3*np.log(2*np.pi)-1.5*np.linalg.slogdet(mat)[1]-.5*np.trace(
        np.linalg.inv(mat)@np.array([[2., .4], [.4, 3.]]))
    check("likelihood_matrix_formula", abs(ll(1.2,.9,.2,3,s)[0]-direct))
    check("identical_likelihood_all_retained",
          0. if np.all(confidence(np.zeros((2,3)), p["confidence_alpha"])) else 1.)
    sample = np.array([[.1,.7],[-.3,.2],[.4,-.8]])
    sums = np.array([[sum(sample[:,0]**2),sum(sample[:,1]**2),sum(sample[:,0]*sample[:,1])]])
    check("orthogonal_sum_squares",
          abs((sums[0,0]+sums[0,1]+2*sums[0,2])/2-sum(((sample[:,0]+sample[:,1])/np.sqrt(2))**2)))
    check("orthogonal_difference_squares",
          abs((sums[0,0]+sums[0,1]-2*sums[0,2])/2-sum(((sample[:,0]-sample[:,1])/np.sqrt(2))**2)))
    check("hidden_pair_weights_normalized", abs(sum(c[2] for c in components(p["scenarios"][-1]))-1))
    # Normalization and stability of the thermal elementary models.
    for scenario in p["scenarios"]:
        check(scenario["name"]+"_unit_position_variance", abs(covariance(p,scenario,0)-1.))
    rows, arrays = [], {}
    positive_det, nonempty, rejection_dominates = True, True, True
    fit_max_density_bound = 0.
    all_scalar_reference_error = 0.
    for si, scenario in enumerate(p["scenarios"]):
        for n in p["pair_budgets"]:
            rng = np.random.default_rng(np.random.SeedSequence([p["seed"], si, n]))
            normal = rng.standard_normal((r,n,2))
            for design, lags in p["designs"].items():
                lcount = len(lags)
                perlag = n//lcount
                half = perlag//2
                assert 2*half*lcount == n
                full_ll = np.zeros((r,3))
                holdout_ll = np.zeros((r,3))
                fitted_ll = np.zeros(r)
                moments_pass = np.ones((r,3), dtype=bool)
                saved_stats, fitted_covariances = [], []
                for li, lag in enumerate(lags):
                    z = normal[:,li*perlag:(li+1)*perlag,:]
                    cross = covariance(p,scenario,lag)
                    rho = cross/v
                    x = np.sqrt(v)*z[:,:,0]
                    y = np.sqrt(v)*(rho*z[:,:,0]+np.sqrt(1-rho*rho)*z[:,:,1])
                    stats = []
                    for selection in (slice(0,half),slice(half,perlag)):
                        xx, yy = x[:,selection], y[:,selection]
                        stats.append(np.column_stack([np.sum(xx*xx,axis=1),np.sum(yy*yy,axis=1),
                                                      np.sum(xx*yy,axis=1)]))
                    train, test = stats
                    total = train+test
                    aa = train[:,0]/half+p["ridge_fraction"]*v
                    bb = train[:,1]/half+p["ridge_fraction"]*v
                    cc = train[:,2]/half
                    positive_det &= bool(np.all(aa*bb-cc*cc>0))
                    fitted_ll += ll(aa,bb,cc,half,test)
                    crosses = np.array([covariance(p,c,lag) for c in candidates])
                    for j,candidate_cross in enumerate(crosses):
                        full_ll[:,j] += ll(v,v,candidate_cross,perlag,total)
                        holdout_ll[:,j] += ll(v,v,candidate_cross,half,test)
                    moments_pass &= moment_acceptance(v,crosses,perlag,total,lcount,
                                                       p["family_rejection_alpha"])
                    # Independent one-dataset direct matrix likelihood audit.
                    fitmat = np.array([[aa[0],cc[0]],[cc[0],bb[0]]])
                    testmat = np.array([[test[0,0],test[0,2]],[test[0,2],test[0,1]]])
                    direct = -half*np.log(2*np.pi)-half/2*np.linalg.slogdet(fitmat)[1]-.5*np.trace(
                        np.linalg.solve(fitmat,testmat))
                    all_scalar_reference_error = max(all_scalar_reference_error,
                        abs(direct-ll(aa,bb,cc,half,test)[0]))
                    saved_stats.append(np.stack([train,test],axis=1))
                    fitted_covariances.append(np.column_stack([aa,bb,cc]))
                loge = fitted_ll-np.max(holdout_ll,axis=1)
                # For each nominal truth, denominator maximum >= true holdout likelihood.
                if scenario["in_family"]:
                    true_idx = p["candidate_aliases"].index(int(scenario["alias"]))
                    fit_max_density_bound = max(fit_max_density_bound,
                        float(np.max(loge-(fitted_ll-holdout_ll[:,true_idx]))))
                rejects = {
                    "discrimination_only": np.zeros(r,dtype=bool),
                    "split_likelihood_gate": loge>np.log(1/p["family_rejection_alpha"]),
                    "concentration_gate": ~np.any(moments_pass,axis=1)}
                retained = confidence(full_ll,p["confidence_alpha"])
                nonempty &= bool(np.all(np.any(retained,axis=1)))
                winners = np.argmax(full_ll>=np.max(full_ll,axis=1,keepdims=True)-1e-10,axis=1)
                errors = abs(responses[winners]-response(p,scenario))/abs(response(p,scenario))
                key = f"{scenario['name']}_n{n}_{design}"
                arrays[key+"_stats"] = np.stack(saved_stats,axis=1)
                arrays[key+"_fitted_covariance"] = np.stack(fitted_covariances,axis=1)
                arrays[key+"_full_ll"] = full_ll
                arrays[key+"_holdout_ll"] = holdout_ll
                arrays[key+"_loge"] = loge
                arrays[key+"_moment_pass"] = moments_pass
                arrays[key+"_base_retained"] = retained
                for method,rejected in rejects.items():
                    accepted = retained&(~rejected[:,None])
                    sizes = np.sum(accepted,axis=1)
                    singleton = sizes==1
                    false_safe = singleton&(errors>p["response_tolerance"])
                    rejection_dominates &= bool(np.all(sizes[rejected]==0))
                    true_retained = accepted[:,true_idx] if scenario["in_family"] else None
                    rows.append({
                        "scenario": scenario["name"], "in_family": scenario["in_family"],
                        "pairs": n, "design": design, "method": method,
                        "family_rejection": wilson(rejected),
                        "singleton_rate": wilson(singleton),
                        "false_reassurance": wilson(false_safe),
                        "conditional_false_reassurance": wilson((errors>p["response_tolerance"])[singleton]),
                        "true_model_retained": wilson(true_retained) if true_retained is not None else None,
                        "mean_accepted_singleton_response_error": float(np.mean(errors[singleton])) if np.any(singleton) else None,
                        "mean_retained_count": float(np.mean(sizes))})
    check("all_fitted_covariances_positive",0. if positive_det else 1.)
    check("ungated_sets_nonempty",0. if nonempty else 1.)
    check("rejection_dominates_claims",0. if rejection_dominates else 1.)
    check("split_denominator_bounds_true_likelihood",max(0.,fit_max_density_bound))
    check("batch_fitted_likelihood_matches_matrix",all_scalar_reference_error,1e-7)
    report = {"protocol_sha256":hashlib.sha256(raw).hexdigest(),
              "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python":platform.python_version(),"numpy":np.__version__,"matplotlib":matplotlib.__version__,
              "scope":p["scope"],"dataset_evaluations":len(rows)//len(p["methods"])*r,
              "method_evaluations":len(rows)*r,"checks":checks,
              "all_checks_passed":all(v["passed"] for v in checks.values()),"cells":rows,
              "guarantees":{"nominal_family_rejection_upper_bound":p["family_rejection_alpha"],
                            "nominal_gated_true_exclusion_upper_bound":p["family_rejection_alpha"]+p["confidence_alpha"]},
              "limits":["Known finite Gaussian candidate family and independent equilibrium pairs.",
                        "No lower bound on power against omitted systems; acceptance is not proof of correctness.",
                        "Gates are established statistical controls, not a new physical theory.",
                        "Common random numbers couple designs and methods; totals are evaluations.",
                        "Per-cell Wilson intervals are approximate Monte Carlo intervals, not simultaneous bounds.",
                        "No nonlinear experiment or thermal-memory algorithm reproduction completed."]}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    np.savez_compressed(OUT/"replicates.npz",**arrays)
    fields=["scenario","pairs","design","method","family_rejection","singleton_rate","false_reassurance",
            "mean_accepted_singleton_response_error"]
    lines=[",".join(fields)]
    for row in rows:
        lines.append(",".join(str(row[f]["estimate"] if isinstance(row[f],dict) else row[f]) for f in fields))
    (OUT/"summary.csv").write_text("\n".join(lines)+"\n",encoding="utf-8")
    plot(p,rows)
    brief=[{k:(v["estimate"] if isinstance(v,dict) else v) for k,v in row.items()
            if k in fields} for row in rows if row["pairs"]==512 and row["design"]=="two_lags"]
    print(json.dumps({"checks":len(checks),"passed":report["all_checks_passed"],
                      "dataset_evaluations":report["dataset_evaluations"],"n512_two_lags":brief},indent=2))
    assert report["all_checks_passed"]


def plot(p,rows):
    fig,axes=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
    labels={"discrimination_only":"No family check","split_likelihood_gate":"Split likelihood",
            "concentration_gate":"Concentration bound"}
    colors=["#8a929b","#147e79","#865ba7"]
    for ax,(metric,nominal) in zip(axes.flat,[
        ("family_rejection",True),("family_rejection",False),
        ("false_reassurance",False),("singleton_rate",True)]):
        for design,style in (("single_lag","--"),("two_lags","-")):
            for method,color in zip(p["methods"],colors):
                values=[]
                for n in p["pair_budgets"]:
                    selected=[r for r in rows if r["in_family"]==nominal and r["pairs"]==n
                              and r["design"]==design and r["method"]==method]
                    values.append(np.mean([r[metric]["estimate"] for r in selected]))
                ax.plot(p["pair_budgets"],values,style,marker="o",color=color,
                        label=labels[method]+(" / 1 lag" if design=="single_lag" else " / 2 lags"))
        ax.set(xscale="log",xlabel="Total independent position pairs",ylim=(-.03,1.03))
        ax.set_xticks(p["pair_budgets"],[str(n) for n in p["pair_budgets"]])
        ax.grid(alpha=.2)
    axes[0,0].set(title="Nominal: rejection of a correct family",ylabel="False-rejection fraction",ylim=(-.003,.05))
    axes[0,0].axhline(p["family_rejection_alpha"],color="#b44d36",linewidth=1,label="2.5% bound")
    axes[0,1].set(title="Omitted physics: family rejection",ylabel="Detection fraction")
    axes[1,0].set(title="Omitted physics: false singleton reassurance",ylabel="False-reassurance fraction")
    axes[1,1].set(title="Nominal: retained singleton answers",ylabel="Singleton fraction")
    axes[0,1].legend(fontsize=7)
    fig.suptitle("Can the procedure say 'none of these models'?\n"
                 "Equal-weight scenario averages; per-scenario counts and intervals are in results.json.",fontsize=12)
    fig.savefig(OUT/"family_rejection.png",dpi=170)
    plt.close(fig)


if __name__=="__main__":
    main()
