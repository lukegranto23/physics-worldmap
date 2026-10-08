"""Near-resonance detection: calibrated known-alternative oracle and information bound."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import platform
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
PROTOCOL=HERE/"oracle_detection_protocol.json"
DEPENDENCY=HERE/"20_family_rejection.py"
OUT=HERE/"results"/"oracle_detection"
spec=importlib.util.spec_from_file_location("family_rejection_reference",DEPENDENCY)
family=importlib.util.module_from_spec(spec)
spec.loader.exec_module(family)


def cov(alias,t,decay=.2):
    w=2*np.pi*alias
    return np.exp(-decay*np.abs(t))*(np.cos(w*t)+decay/w*np.sin(w*np.abs(t)))


def chi(alias,p):
    m=1/((2*np.pi*alias)**2+p["decay_rate"]**2)
    w=p["force_frequency"]
    return 1/(1-m*w*w+2j*p["decay_rate"]*m*w)


def information(alias,t,v,h,decay):
    c=cov(alias,t,decay)
    derivative=(cov(alias+h,t,decay)-cov(alias-h,t,decay))/(2*h)
    return .5*derivative**2*((v+c)**-2+(v-c)**-2)


def draw_stats(rng,r,n,v,c):
    """Exact two-dimensional Wishart sufficient statistics via Bartlett factors."""
    a=rng.chisquare(n,r)
    b=rng.standard_normal(r)
    d=rng.chisquare(n-1,r)
    plus=(v+c)*a
    cross=np.sqrt((v+c)*(v-c)*a)*b
    minus=(v-c)*(b*b+d)
    return np.column_stack([(plus+minus+2*cross)/2,(plus+minus-2*cross)/2,
                            (plus-minus)/2])


def datasets(rng,r,n,lags,v,alias,p):
    per=n//len(lags)
    assert per%2==0
    return [(draw_stats(rng,r,per//2,v,cov(alias,t,p["decay_rate"])),
             draw_stats(rng,r,per//2,v,cov(alias,t,p["decay_rate"]))) for t in lags]


def oracle_score(data,lags,n,v,alternative,p):
    score=np.zeros(len(data[0][0]))
    per=n//len(lags)
    for t,(train,test) in zip(lags,data):
        total=train+test
        score+=family.ll(v,v,cov(alternative,t,p["decay_rate"]),per,total)
        score-=family.ll(v,v,cov(p["null_alias"],t,p["decay_rate"]),per,total)
    return score


def practical_scores(data,lags,n,v,p):
    r=len(data[0][0]); per=n//len(lags); half=per//2
    fitted=np.zeros(r); listed=np.zeros((r,3)); passes=np.ones((r,3),dtype=bool)
    for t,(train,test) in zip(lags,data):
        a=train[:,0]/half+p["ridge_fraction"]*v
        b=train[:,1]/half+p["ridge_fraction"]*v
        c=train[:,2]/half
        fitted+=family.ll(a,b,c,half,test)
        crosses=np.array([cov(j,t,p["decay_rate"]) for j in p["candidate_aliases"]])
        for j,candidate_cross in enumerate(crosses):
            listed[:,j]+=family.ll(v,v,candidate_cross,half,test)
        passes&=family.moment_acceptance(v,crosses,per,train+test,len(lags),p["alpha"])
    return fitted-np.max(listed,axis=1),~np.any(passes,axis=1)


def divergences(null,alt,lags,n,v,p):
    forward=reverse=0.
    for t in lags:
        c0,c1=cov(null,t,p["decay_rate"]),cov(alt,t,p["decay_rate"])
        ratio=np.array([(v+c1)/(v+c0),(v-c1)/(v-c0)])
        forward+=n/len(lags)*.5*np.sum(ratio-1-np.log(ratio))
        reverse+=n/len(lags)*.5*np.sum(1/ratio-1+np.log(ratio))
    return float(forward),float(reverse)


def main():
    raw=PROTOCOL.read_bytes(); p=json.loads(raw)
    grid=np.linspace(*p["lag_grid"][:2],int(p["lag_grid"][2]))
    chosen={}; checks={}
    def check(name,error,tol=1e-9):
        checks[name]={"error":float(error),"tolerance":tol,"passed":bool(error<tol)}
    for noise in p["measurement_noise_sds"]:
        v=1+noise*noise
        fi=information(p["null_alias"],grid,v,p["fisher_derivative_step"],p["decay_rate"])
        chosen[str(noise)]=float(grid[np.argmax(fi)])
        refined=information(p["null_alias"],grid,v,p["fisher_derivative_step"]/2,p["decay_rate"])
        check(f"fisher_derivative_refinement_{noise}",np.linalg.norm(fi-refined)/np.linalg.norm(refined),1e-6)
    k=int(np.ceil((p["calibration_replicates"]+1)*(1-p["alpha"])))
    check("calibration_rank_valid",0. if 1<=k<=p["calibration_replicates"] else 1.)
    rank_size=(p["calibration_replicates"]+1-k)/(p["calibration_replicates"]+1)
    check("rank_marginal_size_control",max(0.,rank_size-p["alpha"]))
    check("same_model_zero_kl",sum(divergences(1,1,[.17,.43],64,1.1,p)))
    c0,c1=cov(1,.43),cov(1.015,.43)
    s0=np.array([[1.1,c0],[c0,1.1]]); s1=np.array([[1.1,c1],[c1,1.1]])
    direct=.5*(np.trace(np.linalg.solve(s0,s1))-2+np.linalg.slogdet(s0)[1]-np.linalg.slogdet(s1)[1])
    check("kl_matrix_vs_diagonal_formula",abs(direct-divergences(1,1.015,[.43],1,1.1,p)[0]))
    check("fisher_matrix_formula",abs(
        information(1,.43,1.1,1e-5,.2)-
        .5*np.trace(np.linalg.matrix_power(np.linalg.solve(s0,np.array([[0.,
            (cov(1+1e-5,.43)-cov(1-1e-5,.43))/2e-5],
            [(cov(1+1e-5,.43)-cov(1-1e-5,.43))/2e-5,0.]])),2))))
    # Sampling implementation check, independent of study calibration/evaluation.
    audit_rng=np.random.default_rng(p["seed"]+999)
    audit=draw_stats(audit_rng,100000,16,1.1,.4)
    expected=np.array([17.6,17.6,6.4])
    # Sampling uncertainty tolerance, not a proof of generator correctness.
    check("wishart_mean_audit",np.max(abs(audit.mean(axis=0)-expected)/expected),.01)
    check("wishart_positive_definite",0. if np.all(audit[:,0]*audit[:,1]-audit[:,2]**2>0) else 1.)
    arrays={"lag_grid":grid}; rows=[]; index=0
    for noise in p["measurement_noise_sds"]:
        v=1+noise*noise
        arrays[f"fisher_noise{noise}"]=information(1,grid,v,p["fisher_derivative_step"],p["decay_rate"])
        for n in p["pair_budgets"]:
            for design in p["designs"]:
                lags=p["previous_lags"] if design=="previous_two_lags" else [chosen[str(noise)]]
                for alternative in p["alternative_aliases"]:
                    streams=np.random.SeedSequence([p["seed"],index]).spawn(3)
                    cal=datasets(np.random.default_rng(streams[0]),p["calibration_replicates"],
                                 n,lags,v,1,p)
                    cal_score=oracle_score(cal,lags,n,v,alternative,p)
                    threshold=float(np.partition(cal_score,k-1)[k-1])
                    row={"noise_sd":noise,"pairs":n,"design":design,"lags":lags,
                         "alternative_alias":alternative,"oracle_threshold":threshold,
                         "response_relative_error":float(abs(chi(1,p)-chi(alternative,p))/abs(chi(alternative,p)))}
                    for label,alias,stream in (("null",1,streams[1]),("alternative",alternative,streams[2])):
                        data=datasets(np.random.default_rng(stream),p["evaluation_replicates"],n,lags,v,alias,p)
                        oracle=oracle_score(data,lags,n,v,alternative,p)
                        split,concentration=practical_scores(data,lags,n,v,p)
                        row[label]={
                            "oracle":family.wilson(oracle>threshold),
                            "split":family.wilson(split>np.log(1/p["alpha"])),
                            "concentration":family.wilson(concentration)}
                        arrays[f"cell{index}_{label}"]=np.column_stack([oracle,split,concentration])
                    forward,reverse=divergences(1,alternative,lags,n,v,p)
                    bound=min(1.,p["alpha"]+np.sqrt(min(forward,reverse)/2))
                    row.update({"kl_alt_to_null":forward,"kl_null_to_alt":reverse,
                                "pinsker_power_upper_bound":float(bound),
                                "information_limited_below_half":bool(bound<p["information_limited_power_cutoff"]),
                                "oracle_practical_gap":bool(
                                    row["alternative"]["oracle"]["estimate"]>p["oracle_high_power_cutoff"] and
                                    max(row["alternative"][name]["estimate"] for name in ("split","concentration"))<
                                    p["practical_low_power_cutoff"])})
                    rows.append(row); index+=1
    report={"protocol_sha256":hashlib.sha256(raw).hexdigest(),
            "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256":hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest(),
            "python":platform.python_version(),"numpy":np.__version__,"matplotlib":matplotlib.__version__,
            "scope":p["scope"],"selected_lags":chosen,"oracle_rank":k,
            "oracle_marginal_null_rejection_bound":rank_size,
            "calibration_evaluations":len(rows)*p["calibration_replicates"],
            "evaluation_datasets":len(rows)*2*p["evaluation_replicates"],
            "checks":checks,"all_checks_passed":all(v["passed"] for v in checks.values()),
            "information_limited_cells":sum(r["information_limited_below_half"] for r in rows),
            "oracle_practical_gap_cells":sum(r["oracle_practical_gap"] for r in rows),
            "cells":rows,
            "limits":["The oracle knows the alternative and controls null 1 only; not an information-matched method.",
                      "Oracle power is a calibrated Monte Carlo approximation to ideal NP power, not a rigorous numerical ceiling.",
                      "Rank calibration controls null rejection marginally over calibration; conditional size varies.",
                      "Evaluation Wilson intervals do not include calibration variability.",
                      "Pinsker bound applies to any level-alpha test at null 1, including randomized tests.",
                      "Fisher design uses null sensitivity, not held-out alternatives; local criterion is not globally optimal power.",
                      "All candidate parameters and Gaussian noise are known; not an unknown-memory reconstruction.",
                      "No new theory, nonlinear validation, or universal response certificate is claimed."]}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"results.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    np.savez_compressed(OUT/"scores.npz",**arrays)
    fields=["noise_sd","pairs","design","alternative_alias","response_relative_error","pinsker_power_upper_bound"]
    lines=[",".join(fields+["oracle_power","split_power","concentration_power"])]
    for row in rows:
        lines.append(",".join([str(row[f]) for f in fields]+[
            str(row["alternative"][name]["estimate"]) for name in ("oracle","split","concentration")]))
    (OUT/"summary.csv").write_text("\n".join(lines)+"\n",encoding="utf-8")
    plot(p,rows,chosen)
    print(json.dumps({"checks":len(checks),"passed":report["all_checks_passed"],
          "selected_lags":chosen,"information_limited_cells":report["information_limited_cells"],
          "oracle_practical_gap_cells":report["oracle_practical_gap_cells"],
          "middle_noise": [{**{f:r[f] for f in fields},
              **{name:r["alternative"][name]["estimate"] for name in ("oracle","split","concentration")}}
              for r in rows if r["noise_sd"]==.35]},indent=2))
    assert report["all_checks_passed"]


def plot(p,rows,chosen):
    fig,axes=plt.subplots(2,3,figsize=(14,8),constrained_layout=True)
    noise=.35
    for col,alternative in enumerate(p["alternative_aliases"]):
        for row_index,design in enumerate(p["designs"]):
            ax=axes[row_index,col]
            selected=[r for r in rows if r["noise_sd"]==noise and r["alternative_alias"]==alternative
                      and r["design"]==design]
            for method,color in (("oracle","#172c4c"),("split","#147e79"),("concentration","#865ba7")):
                ax.plot(p["pair_budgets"],[r["alternative"][method]["estimate"] for r in selected],
                        "o-",color=color,label=method)
            ax.plot(p["pair_budgets"],[r["pinsker_power_upper_bound"] for r in selected],
                    "--",color="#c0763c",label="Information upper bound")
            lag_text="Earlier two lags" if design=="previous_two_lags" else f"Fisher lag {chosen[str(noise)]:.2f}"
            ax.set(title=f"{lag_text}; frequency +{100*(alternative-1):.1f}%",
                   xscale="log",ylim=(-.03,1.03),xlabel="Independent position pairs",ylabel="Detection probability")
            ax.set_xticks(p["pair_budgets"],[str(n) for n in p["pair_budgets"]])
            ax.grid(alpha=.2)
    axes[0,0].legend(fontsize=8)
    fig.suptitle("Is the failure in the data or in the test? Sensor noise SD = 0.35\n"
                 "Oracle knows the alternative; practical tests do not. Curves are estimates, bound is analytic.",
                 fontsize=12)
    fig.savefig(OUT/"oracle_detection.png",dpi=170)
    plt.close(fig)


if __name__=="__main__":
    main()
