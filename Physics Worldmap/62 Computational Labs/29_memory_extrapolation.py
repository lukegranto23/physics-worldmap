"""Post-hoc response and diffusion-horizon audit of saved thermal realizations."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from scipy.special import gamma

HERE = Path(__file__).resolve().parent
OUT = HERE/'results'/'noisy_memory_stress'
PROTOCOL = HERE/'memory_extrapolation_protocol.json'


def target_msd(t):
    # Laplace: M~ = 2 s^-3/2 - 2/(1+s^3/2), hence
    # M(t) = 4 sqrt(t/pi) + 2 C'(t). Evaluate C' by pole + cut.
    derivative_poles = 4/3*np.exp(-t/2)*(-.5*np.cos(np.sqrt(3)*t/2)
                                                -np.sqrt(3)/2*np.sin(np.sqrt(3)*t/2))
    integral = quad(lambda u: u**1.5*np.exp(-u)/(1+(u/t)**3),
                    0, np.inf, epsabs=1e-12, epsrel=1e-11)[0]
    return 4*np.sqrt(t/np.pi)+2*(derivative_poles+integral/(np.pi*t**2.5))


def target_msd_series(t):
    return float(2*sum((-1)**k*t**(1.5*k+2)/gamma(1.5*k+3) for k in range(90)))


def model_msd(A,t):
    n = len(A)
    augmented = np.zeros((n+2,n+2))
    augmented[:n,:n] = A
    augmented[0,n] = 1
    augmented[n,n+1] = 1
    return float(2*expm(t*augmented)[0,n+1])


def mobility(A,omega):
    e1=np.eye(len(A))[0]
    return np.array([e1@np.linalg.solve(1j*w*np.eye(len(A))-A,e1) for w in omega])


def target_mobility(omega):
    s=1j*np.asarray(omega)
    return 1/(s+s**(-.5))


def diffusion(A):
    e1=np.eye(len(A))[0]
    direct=float(e1@np.linalg.solve(-A,e1))
    delta=-A[0,0]
    kappa0=A[0,1:]@np.linalg.solve(-A[1:,1:],-A[1:,0])
    return direct,float(1/(delta+kappa0))


def main():
    p=json.loads(PROTOCOL.read_text(encoding='utf-8'))
    clean_path=HERE/'results'/'thermal_memory_reproduction'/'curves.npz'
    noisy_path=OUT/'inputs_and_models.npz'
    clean=np.load(clean_path)['regularized_system']
    noisy=np.load(noisy_path)
    checks=[]
    def check(name,valid,value):
        checks.append({'name':name,'passed':bool(valid),'value':value})
        if not valid: raise AssertionError(name+': '+str(value))
    errs=[abs(target_msd(t)-target_msd_series(t)) for t in [.05,.1,.5,1,2,3,5]]
    check('analytic MSD quadrature versus independent series',max(errs)<1e-8,max(errs))
    check('target long-time coefficient',abs(target_msd(1e5)/(4*np.sqrt(1e5/np.pi))-1)<1e-8,
          target_msd(1e5)/(4*np.sqrt(1e5/np.pi)))
    tg=p['time_grid']; ts=np.geomspace(tg['minimum'],tg['maximum'],tg['points'])
    exact=np.array([target_msd(t) for t in ts]); predicted=np.array([model_msd(clean,t) for t in ts])
    D,Dschur=diffusion(clean)
    check('clean zero-frequency identities',abs(D-Dschur)<1e-10,abs(D-Dschur))
    check('clean long-time MSD slope',abs(predicted[-1]/(2*D*ts[-1])-1)<.01,
          predicted[-1]/(2*D*ts[-1]))
    closed_errors=[]
    for t in [1,10,100]:
        e1=np.eye(len(clean))[0]
        closed=2*e1@np.linalg.solve(clean,np.linalg.solve(clean,(expm(t*clean)-np.eye(len(clean))-t*clean)@e1))
        closed_errors.append(abs(closed-model_msd(clean,t)))
    check('independent MSD matrix-integration identity',max(closed_errors)<1e-7,float(max(closed_errors)))
    all_models=[('clean',0,clean)]
    for (M,rep,n),padded in zip(noisy['accepted_ids'],noisy['systems']):
        all_models.append((int(M),int(rep),padded[:n,:n]))
    rows=[]; max_diff=0.; min_D=np.inf; response_identity_error=0.
    spectra={}
    for M,rep,A in all_models:
        check_stable=max(np.linalg.eigvals(A).real)<0 and max(np.linalg.eigvals(A[1:,1:]).real)<0
        if not check_stable: raise AssertionError('model violates asymptotic assumptions')
        d,ds=diffusion(A); max_diff=max(max_diff,abs(d-ds)); min_D=min(min_D,d)
        row={'ensemble_size':M,'replicate':rep,'n':len(A),'diffusivity':d,'bands':{}}
        for name,(lo,hi) in p['frequency_bands'].items():
            omega=np.geomspace(lo,hi,p['points_per_band'])
            estimate=mobility(A,omega); truth=target_mobility(omega)
            rel=abs(estimate-truth)/abs(truth)
            phase=np.angle(estimate/truth)
            amplitude=abs(estimate)/abs(truth)
            row['bands'][name]={'max_complex_relative_error':float(max(rel)),
                                'max_abs_phase_error_radians':float(max(abs(phase))),
                                'amplitude_ratio_min':float(min(amplitude)),
                                'amplitude_ratio_max':float(max(amplitude))}
            if M=='clean': spectra[name]=(omega,estimate,truth,rel)
            b,c,a0=A[0,1:],-A[1:,0],A[1:,1:]
            kappa=np.array([b@np.linalg.solve(1j*w*np.eye(len(a0))-a0,c) for w in omega])
            schur=1/(1j*omega-A[0,0]+kappa)
            response_identity_error=max(response_identity_error,float(max(abs(estimate-schur))))
        rows.append(row)
    check('all accepted models have positive diffusivity',min_D>0,float(min_D))
    check('all diffusion formulas agree',max_diff<1e-8,float(max_diff))
    check('full resolvent versus memory transfer',response_identity_error<1e-8,response_identity_error)
    summary=[]
    for M in noisy['ensemble_sizes']:
        subset=[r for r in rows if r['ensemble_size']==int(M)]
        summary.append({'ensemble_size':int(M),'accepted_models':len(subset),
                        'diffusivity_median':float(np.median([r['diffusivity'] for r in subset])),
                        'median_band_max_errors':{band:float(np.median([r['bands'][band]['max_complex_relative_error']
                                                                       for r in subset])) for band in p['frequency_bands']}})
    relative=abs(predicted-exact)/exact
    outside=(ts>11.4)&(relative>p['time_horizon_threshold'])
    horizon=float(ts[np.where(outside)[0][0]]) if np.any(outside) else None
    table=[{'time':t,'target_msd':target_msd(t),'clean_model_msd':model_msd(clean,t),
            'relative_error':abs(model_msd(clean,t)-target_msd(t))/target_msd(t)} for t in p['clean_checks_at_times']]
    fig,axes=plt.subplots(2,2,figsize=(12,8.2))
    axes[0,0].loglog(ts,exact,color='black',label='fractional target')
    axes[0,0].loglog(ts,predicted,color='#0072B2',ls='--',label='clean fitted model')
    axes[0,0].axvline(11.4,color='grey',ls=':',label='last fit sample')
    axes[0,0].set(xlabel='time',ylabel='mean-square displacement',title='Short-window fit, different long-time motion')
    axes[0,0].legend(frameon=False,fontsize=8)
    axes[0,1].semilogx(ts,np.gradient(np.log(exact),np.log(ts)),color='black',label='target')
    axes[0,1].semilogx(ts,np.gradient(np.log(predicted),np.log(ts)),color='#0072B2',ls='--',label='clean model')
    axes[0,1].axhline(.5,color='grey',lw=.6); axes[0,1].axhline(1,color='grey',lw=.6)
    axes[0,1].set(xlabel='time',ylabel='local slope d log(MSD) / d log(t)',title='Subdiffusion (1/2) versus normal diffusion (1)')
    omega=np.geomspace(1e-5,30,500)
    chi=mobility(clean,omega); true_chi=target_mobility(omega)
    axes[1,0].loglog(omega,abs(true_chi),color='black',label='target')
    axes[1,0].loglog(omega,abs(chi),color='#0072B2',ls='--',label='clean model')
    axes[1,0].axhline(D,color='#D55E00',ls=':',label='model DC mobility')
    axes[1,0].set(xlabel='angular frequency',ylabel='mobility magnitude',title='Slow forcing exposes the cutoff')
    axes[1,0].legend(frameon=False,fontsize=8)
    ax=axes[1,1]
    bands=list(p['frequency_bands'])
    for s in summary:
        ax.plot(np.arange(len(bands)),[s['median_band_max_errors'][b] for b in bands],'o-',label=str(s['ensemble_size']))
    ax.plot(np.arange(len(bands)),[rows[0]['bands'][b]['max_complex_relative_error'] for b in bands],'k--',label='clean')
    ax.set(yscale='log',xticks=np.arange(len(bands)),xticklabels=bands,ylabel='median maximum relative response error',
           title='Response errors among accepted models')
    ax.legend(title='ensemble',frameon=False,fontsize=8)
    fig.suptitle('Post-hoc extrapolation audit: a finite-memory model has a finite horizon',fontsize=13)
    fig.tight_layout();fig.savefig(OUT/'memory_extrapolation.png',dpi=180);plt.close(fig)
    result={'study':p['title'],'scope':p['status'],'clean_diffusivity':D,'clean_msd_table':table,
            'clean_first_grid_exceedance_after_training':horizon,'threshold':p['time_horizon_threshold'],
            'clean_response':rows[0]['bands'],'noisy_summary':summary,'models':rows,
            'checks':checks,'passed_checks':len(checks),
            'hashes':{str(path.relative_to(HERE)):hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in [PROTOCOL,Path(__file__),clean_path,noisy_path]}}
    (OUT/'extrapolation.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    np.savez_compressed(OUT/'extrapolation_curves.npz',time=ts,msd_target=exact,msd_clean=predicted,
                        omega=omega,mobility_target=true_chi,mobility_clean=chi)
    print(json.dumps({k:v for k,v in result.items() if k!='models'},indent=2,allow_nan=False))


if __name__=='__main__':main()
