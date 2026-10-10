"""Reproducible simulations for: Frameworks Without Evidence? (2026).
Runtime trust scoring as specified in TAZAI (Agballog & Botero, 2026):
  T = a*I + b*B + g*C ;  T(t+1) = T(t)*exp(-lam*R) ;  access iff T >= tau ;  T_group = mean(T_i)
Run: python3 trust_sim.py  -> writes results.json and prints tables."""
import numpy as np, json, math
SEED = 20261010
rng = np.random.default_rng(SEED)
TAU, T0 = 0.7, 0.9
out = {"seed": SEED, "tau": TAU, "T0": T0}

# ---------- Exp 1: behavioural floor (Prop. 1) ----------
floor = []
for tau in [0.6, 0.7, 0.8]:
    for a in [0.2, 1/3, 0.4, 0.5]:
        b = g = (1 - a) / 2
        floor.append(dict(tau=tau, alpha=round(a, 3), beta=round(b, 3),
                          B_min=round(max(0.0, (tau - a - g) / b), 3)))
out["exp1_floor"] = floor

# ---------- Exp 2: decay with and without recovery (Props. 2-3) ----------
H, RUNS, LAM = 500, 4000, 1.0
P_FLAG, R_MAX = 0.05, 0.2        # benign monitor noise: 5% of steps flagged, risk ~ U(0,0.2) (< budget)
MU_B = P_FLAG * R_MAX / 2         # 0.005
def benign_noise():
    return (rng.random((RUNS, H)) < P_FLAG) * rng.uniform(0, R_MAX, (RUNS, H))
def simulate(rho, mode, r_h=0.1, k=20, margin=0.0):
    """mode: benign | periodic | adaptive.  Leaky log-trust: L <- min(L0, L - lam*R + rho)."""
    R = benign_noise()
    L0, Lt = math.log(T0), math.log(TAU)
    L = np.full(RUNS, L0); alive = np.ones(RUNS, bool)
    harms = np.zeros(RUNS); t_rev = np.full(RUNS, np.nan)
    for t in range(H):
        r = R[:, t].copy()
        if mode == "periodic":
            act = np.full(RUNS, (t % k) == k - 1)
        elif mode == "adaptive":   # threshold-aware: acts only if post-action trust stays >= tau+margin
            act = (L - LAM * (r + r_h)) >= math.log(TAU + margin)
        else:
            act = np.zeros(RUNS, bool)
        act &= alive
        r = r + act * r_h
        harms += act
        L = np.minimum(L0, L - LAM * r + rho)
        newly = alive & (L < Lt)
        t_rev[newly] = t; alive &= ~newly
    return dict(revoked=float((~alive).mean()), harms=float(harms.mean()),
                median_revoke=float(np.nanmedian(t_rev)) if (~alive).any() else None)
rows = []
for rho in [0.0, 0.005, 0.0075, 0.01, 0.015, 0.02]:
    ben = simulate(rho, "benign")
    per = simulate(rho, "periodic")
    ada = simulate(rho, "adaptive", margin=0.02)
    rows.append(dict(rho=rho, benign_revoked=round(ben["revoked"], 4),
                     benign_median_revoke=ben["median_revoke"],
                     periodic_harms=round(per["harms"], 2), periodic_revoked=round(per["revoked"], 4),
                     adaptive_harms=round(ada["harms"], 2), adaptive_revoked=round(ada["revoked"], 4)))
out["exp2_decay"] = dict(H=H, runs=RUNS, lam=LAM, mu_b=MU_B, r_h=0.1, k=20,
                         budget=round(math.log(T0 / TAU), 4), rows=rows)
# Wald prediction of benign false-revocation time under pure compounding
out["exp2_wald_steps"] = round(math.log(T0 / TAU) / (LAM * MU_B), 1)
# lambda sweep under pure compounding
sweep = []
for lam in [0.25, 0.5, 1, 2, 4]:
    LAM = lam
    ben = simulate(0.0, "benign"); ada = simulate(0.0, "adaptive", margin=0.02)
    sweep.append(dict(lam=lam, benign_median_revoke=ben["median_revoke"], adaptive_harms=round(ada["harms"], 2)))
LAM = 1.0
out["exp2_lambda_sweep"] = sweep

# ---------- Exp 3: group aggregation (Prop. 4) ----------
def masking_curve(Tb=0.9, Tc=0.0):
    return [dict(n=n, group_mean=round(((n - 1) * Tb + Tc) / n, 4)) for n in range(1, 21)]
out["exp3_mask_curve"] = masking_curve()
out["exp3_nstar"] = [dict(Tb=Tb, n_star=math.ceil(Tb / (Tb - TAU) - 1e-12),
                          max_masked_fraction=round((Tb - TAU) / Tb, 4)) for Tb in [0.8, 0.85, 0.9, 0.95]]
def agg(n, sigma, Tc, trials=20000, k=3.5):
    res = {}
    for label, comp in [("false_alarm", False), ("detect", True)]:
        X = np.clip(rng.normal(0.9, sigma, (trials, n)), 0, 1)
        if comp: X[:, 0] = np.clip(rng.normal(Tc, sigma, trials), 0, 1)
        med = np.median(X, 1, keepdims=True)
        mad = 1.4826 * np.median(np.abs(X - med), 1, keepdims=True) + 1e-9
        res[label] = {"mean": (X.mean(1) < TAU).mean(), "min": (X.min(1) < TAU).mean(),
                      "robust_z": (((med - X) / mad) > k).any(1).mean()}
    return res
agg_rows = []
for sigma in [0.05, 0.08]:
    for n in [3, 5, 10, 20, 50]:
        r = agg(n, sigma, Tc=0.5)
        for rule in ["mean", "min", "robust_z"]:
            agg_rows.append(dict(sigma=sigma, n=n, rule=rule,
                                 detect=round(float(r["detect"][rule]), 4),
                                 false_alarm=round(float(r["false_alarm"][rule]), 4)))
out["exp3_agg"] = agg_rows
json.dump(out, open("results.json", "w"), indent=1)
if __name__ == "__main__":
    print(json.dumps({k: v for k, v in out.items() if k not in ("exp3_agg","exp3_mask_curve")}, indent=1))
    for r in agg_rows: print(r)
