#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, warnings
from pathlib import Path
import numpy as np

warnings.filterwarnings("ignore", category=RuntimeWarning)
np.seterr(all="ignore")
ROOT = Path(__file__).resolve().parents[1]

def read_csv(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def as_bool(v):
    return str(v).strip().lower() in {"true", "1", "yes"}

def wilson(k, n, z=1.959963985):
    if n <= 0: return (0.0, 0.0)
    ph = k / n
    den = 1.0 + z*z/n
    cen = (ph + z*z/(2*n)) / den
    half = z * math.sqrt(ph*(1-ph)/n + z*z/(4*n*n)) / den
    return max(0.0, cen-half), min(1.0, cen+half)

def bpmf(k, n, p):
    return math.comb(n, k) * (p ** k) * ((1-p) ** (n-k))

def binom2(k, n, p=.5):
    if n <= 0: return 1.0
    obs = bpmf(k, n, p)
    return min(1.0, sum(bpmf(i, n, p) for i in range(n+1) if bpmf(i, n, p) <= obs + 1e-15))

def mcnemar(b, c):
    return binom2(min(b, c), b+c, .5) if b+c else 1.0

def q7(vals, q):
    xs = sorted(float(v) for v in vals)
    if not xs: return 0.0
    if len(xs) == 1: return xs[0]
    h = (len(xs)-1) * q
    lo, hi = math.floor(h), math.ceil(h)
    return xs[int(h)] if lo == hi else xs[lo] + (xs[hi]-xs[lo]) * (h-lo)

def ranks(vals):
    order = sorted(enumerate(vals), key=lambda x: x[1])
    out = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and order[j][1] == order[i][1]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[order[k][0]] = rank
        i = j
    return out

def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx)/len(rx), sum(ry)/len(ry)
    num = sum((x-mx)*(y-my) for x, y in zip(rx, ry))
    den = math.sqrt(sum((x-mx)**2 for x in rx)) * math.sqrt(sum((y-my)**2 for y in ry))
    return num / den

def mann_whitney_u(group1, group2):
    vals = [(float(v), 1) for v in group1] + [(float(v), 2) for v in group2]
    ranked = ranks([v for v, _ in vals])
    r1 = sum(rank for rank, (_, group) in zip(ranked, vals) if group == 1)
    n1 = len(group1)
    return r1 - n1 * (n1 + 1) / 2.0

def fisher(a, b, c, d):
    row1, col1, n = a+b, a+c, a+b+c+d
    def p(x):
        return math.comb(col1, x) * math.comb(n-col1, row1-x) / math.comb(n, row1)
    lo, hi = max(0, row1-(n-col1)), min(row1, col1)
    obs = p(a)
    return sum(p(x) for x in range(lo, hi+1) if p(x) <= obs + 1e-12)

def holm(pairs):
    ordered = sorted(pairs, key=lambda x: (x[1], x[0]))
    m = len(ordered)
    out = {}
    running = 0.0
    for idx, (name, pval) in enumerate(ordered, start=1):
        adjusted = min(1.0, (m - idx + 1) * pval)
        running = max(running, adjusted)
        out[name] = (idx, running)
    return out

WEIGHTS = (-math.sqrt(3/2), -1.0, -math.sqrt(1/2), math.sqrt(1/2), 1.0, math.sqrt(3/2))

def webb(ep, seed, rep, cluster):
    limit = (1 << 64) - ((1 << 64) % 6)
    counter = 0
    while True:
        msg = f"RFACTOR-WCR-WEBB|v0.96|{ep}|{seed}|{rep}|{cluster}|{counter}".encode()
        value = int.from_bytes(hashlib.sha256(msg).digest()[:8], "big")
        if value < limit:
            return WEIGHTS[value % 6]
        counter += 1

def wcr(X, y, clusters, r, ep, seed, gmin, gmax, step, theta0=0.0, B=9999):
    X, y, r = np.asarray(X, float), np.asarray(y, float), np.asarray(r, float)
    clusters = np.asarray([str(c) for c in clusters])
    unique = sorted(set(clusters.tolist()))
    n, k = X.shape
    G = len(unique)
    inv = np.linalg.inv(X.T @ X)
    beta = inv @ X.T @ y
    resid = y - X @ beta
    q = inv @ r
    denom = float(r @ q)
    h = X @ q
    mult = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    score0 = []
    hscore = []
    qscore0 = []
    qhscore = []
    mvals = []
    for g in unique:
        mask = clusters == g
        Xg = X[mask]
        rg = resid[mask]
        hg = h[mask]
        score = Xg.T @ rg
        hs = Xg.T @ hg
        score0.append(score)
        hscore.append(hs)
        qscore0.append(float(q @ score))
        qhscore.append(float(q @ hs))
        mvals.append(inv @ hs)
    score0, hscore = np.asarray(score0), np.asarray(hscore)
    qscore0, qhscore, mvals = np.asarray(qscore0), np.asarray(qhscore), np.asarray(mvals)
    W = np.empty((B, len(unique)))
    for rep in range(1, B+1):
        for j, g in enumerate(unique):
            W[rep-1, j] = webb(ep, seed, rep, g)
    S0, S1 = W @ score0, W @ hscore
    n0, n1 = S0 @ q, S1 @ q
    A, BB = np.empty_like(W), np.empty_like(W)
    for j in range(W.shape[1]):
        A[:, j] = W[:, j] * qscore0[j] - S0 @ mvals[j]
        BB[:, j] = W[:, j] * qhscore[j] - S1 @ mvals[j]
    v0, v1, v2 = np.sum(A*A, axis=1), np.sum(A*BB, axis=1), np.sum(BB*BB, axis=1)
    meat = np.zeros((k, k))
    for g in unique:
        mask = clusters == g
        score = X[mask].T @ resid[mask]
        meat += np.outer(score, score)
    cov = mult * inv @ meat @ inv
    est = float(r @ beta)
    se = math.sqrt(float(r @ cov @ r))
    def p_for(theta):
        t_obs = (est - theta) / se
        c = (est - theta) / denom
        var = mult * (v0 + 2*c*v1 + c*c*v2)
        tstar = (n0 + c*n1) / np.sqrt(var)
        return (1 + int(np.count_nonzero(np.abs(tstar) >= abs(t_obs)))) / (B + 1)
    accepted = []
    for i in range(int(round((gmax - gmin) / step)) + 1):
        th = round(gmin + i*step, 12)
        if p_for(th) > 0.05:
            accepted.append(th)
    return {"estimate": est, "standard_error": se, "ci_lower": min(accepted), "ci_upper": max(accepted), "p_two_sided": p_for(theta0)}

def h1_design(rows, outcome):
    games = sorted({r["nba_game_id"] for r in rows})
    periods = sorted({int(r["period"]) for r in rows})
    names = ["intercept"] + [f"game_{g}" for g in games[1:]] + [f"period_{p}" for p in periods[1:]] + ["home_control_indicator", "away_control_indicator", "home_score_differential_after_index", "index_end_clock_seconds", "lag5_signed_net_points"]
    X = []
    for row in rows:
        v = [1.0]
        v += [1.0 if row["nba_game_id"] == g else 0.0 for g in games[1:]]
        v += [1.0 if int(row["period"]) == p else 0.0 for p in periods[1:]]
        v += [1.0 if as_bool(row["home_control_indicator"]) else 0.0, 1.0 if as_bool(row["away_control_indicator"]) else 0.0, float(row["home_score_differential_after_index"]), float(row["index_end_clock_seconds"]), float(row["lag5_signed_net_points"])]
        X.append(v)
    y = np.asarray([float(r[outcome]) for r in rows], float)
    clusters = [r["series_id"] for r in rows]
    rv = np.zeros(len(names))
    rv[names.index("home_control_indicator")] = 1.0
    rv[names.index("away_control_indicator")] = -1.0
    return np.asarray(X, float), y, clusters, rv

def add(checks, name, exp, obs, tol=0.0, note=""):
    if isinstance(exp, (int, str, bool)) and tol == 0.0:
        ok, diff = exp == obs, ""
    else:
        diff = abs(float(exp) - float(obs))
        ok = diff <= tol
    checks.append({"check": name, "expected": exp, "observed": obs, "tolerance": tol, "difference": diff, "status": "PASS" if ok else "FAIL", "note": note})

def main():
    checks = []
    h1 = read_csv("data/h1_downstream_window_dataset.csv")
    y10 = [r for r in h1 if as_bool(r["h1_y10_model_eligible"])]
    expected_h1 = {r["model_id"]: r for r in read_csv("results/h1_model_results_expected.csv")}
    for mid, rows, outcome, ep, seed in [
        ("H1_PRIMARY_Y5_WCR_WEBB", h1, "future5_signed_net_points", "H1_Y5", 2026082401),
        ("H1_SECONDARY_Y10_WCR_WEBB", y10, "future10_signed_net_points", "H1_Y10", 2026082402),
        ("H1_SECONDARY_STRUCTURAL_FAILURE_Y5_WCR_WEBB", h1, "future5_structural_failure_differential", "H1_STRUCTURAL_FAILURE", 2026082403),
    ]:
        X, y, clusters, rv = h1_design(rows, outcome)
        obs = wcr(X, y, clusters, rv, ep, seed, -5.0, 5.0, 0.005)
        exp = expected_h1[mid]
        add(checks, mid + ".eligible_rows", int(exp["eligible_rows"]), len(rows))
        add(checks, mid + ".estimate", float(exp["estimate"]), obs["estimate"], 2e-6, "public H1 derivative reproduces within stated floating tolerance")
        add(checks, mid + ".standard_error", float(exp["standard_error"]), obs["standard_error"], 2e-6, "public H1 derivative reproduces within stated floating tolerance")
        for key in ["ci_lower", "ci_upper", "p_two_sided"]:
            add(checks, mid + "." + key, float(exp[key]), obs[key], 1e-12)

    h2 = read_csv("data/h2_downstream_master_ledger.csv")
    cat = read_json("results/h2_categorical_summary_expected.json")
    cat_rows = [r for r in h2 if as_bool(r["categorical_eligible"])]
    k = sum(1 for r in cat_rows if as_bool(r["categorical_correct"]))
    lo, hi = wilson(k, len(cat_rows))
    add(checks, "H2.categorical.eligible_n", cat["eligible_n"], len(cat_rows))
    add(checks, "H2.categorical.correct_k", cat["correct_k"], k)
    add(checks, "H2.categorical.accuracy", cat["accuracy"], k/len(cat_rows), 1e-15)
    add(checks, "H2.categorical.wilson_ci_lower", cat["wilson_ci_lower"], lo, 5e-10)
    add(checks, "H2.categorical.wilson_ci_upper", cat["wilson_ci_upper"], hi, 5e-10)
    add(checks, "H2.categorical.exact_binomial", cat["exact_binomial_p_two_sided"], binom2(k, len(cat_rows)), 1e-15)

    cont = read_json("results/h2_continuous_summary_expected.json")
    cont_rows = [r for r in h2 if as_bool(r["continuous_eligible"]) and r["signed_regulation_control_share_margin"] != ""]
    vals = [float(r["signed_regulation_control_share_margin"]) for r in cont_rows]
    clusters = [r["series_id"] for r in cont_rows]
    cw = wcr(np.ones((len(vals), 1)), np.asarray(vals), clusters, np.asarray([1.0]), "H2_CONTINUOUS", 2026082404, -1.0, 1.0, 0.001)
    add(checks, "H2.continuous.eligible_n", cont["eligible_n"], len(vals))
    add(checks, "H2.continuous.mean", cont["mean_signed_margin"], sum(vals)/len(vals), 1e-15)
    add(checks, "H2.continuous.median", cont["median_signed_margin"], q7(vals, .5), 1e-15)
    add(checks, "H2.continuous.q1", cont["q1"], q7(vals, .25), 1e-15)
    add(checks, "H2.continuous.q3", cont["q3"], q7(vals, .75), 1e-15)
    add(checks, "H2.continuous.prop_gt_zero", cont["proportion_strictly_above_zero"], sum(v > 0 for v in vals)/len(vals), 1e-15)
    add(checks, "H2.continuous.wcr_ci_lower", cont["wcr_ci_lower"], cw["ci_lower"], 1e-12)
    add(checks, "H2.continuous.wcr_ci_upper", cont["wcr_ci_upper"], cw["ci_upper"], 1e-12)
    add(checks, "H2.continuous.wcr_p", cont["wcr_p_two_sided"], cw["p_two_sided"], 1e-12)

    benches = {r["benchmark_id"]: r for r in read_csv("results/h2_benchmark_results_expected.csv")}
    for bid, col in [("HOME_ALWAYS", "home_always_correct"), ("HIGHER_SEED_ALWAYS", "higher_seed_always_correct")]:
        rows = [r for r in cat_rows if r[col] != ""]
        kk = sum(1 for r in rows if as_bool(r[col]))
        exp = benches[bid]
        add(checks, "H2.benchmark." + bid + ".n", int(exp["benchmark_accuracy_n"]), len(rows))
        add(checks, "H2.benchmark." + bid + ".correct", int(exp["benchmark_correct_k"]), kk)
        add(checks, "H2.benchmark." + bid + ".accuracy", float(exp["benchmark_accuracy"]), kk/len(rows), 1e-15)
        bd = sum(1 for r in rows if as_bool(r["categorical_correct"]) and not as_bool(r[col]))
        cd = sum(1 for r in rows if (not as_bool(r["categorical_correct"])) and as_bool(r[col]))
        add(checks, "H2.benchmark." + bid + ".mcnemar_p", float(exp["exact_mcnemar_p_two_sided"]), mcnemar(bd, cd), 1e-15)

    det_rows = {r["sensitivity_id"]: r for r in read_csv("results/h2_determinacy_sensitivity_expected.csv")}
    explicit = [r for r in h2 if as_bool(r["explicit_call_eligible"])]
    indet = [r for r in explicit if r["adjudicability_status"] == "INDETERMINATE"]
    det_correct = sum(1 for r in cat_rows if as_bool(r["categorical_correct"]))
    det_specs = [
        ("LOWER_BOUND_INDETERMINATE_INCORRECT", len(explicit), det_correct),
        ("UPPER_BOUND_INDETERMINATE_CORRECT", len(explicit), det_correct + len(indet)),
    ]
    margin_rows = [r for r in indet if r["signed_regulation_control_share_margin"] not in {"", "0", "0.0"}]
    det_specs.append(("MARGIN_SIGN_INDETERMINATE_SENSITIVITY", len(cat_rows) + len(margin_rows), det_correct + sum(1 for r in margin_rows if float(r["signed_regulation_control_share_margin"]) > 0)))
    for sid, n, correct in det_specs:
        exp = det_rows[sid]
        lo, hi = wilson(correct, n)
        add(checks, "H2.det." + sid + ".eligible_n", int(exp["eligible_n"]), n)
        add(checks, "H2.det." + sid + ".correct_k", int(exp["correct_k"]), correct)
        add(checks, "H2.det." + sid + ".accuracy", float(exp["accuracy"]), correct/n, 1e-15)
        add(checks, "H2.det." + sid + ".wilson_lower", float(exp["wilson_ci_lower"]), lo, 5e-10)
        add(checks, "H2.det." + sid + ".wilson_upper", float(exp["wilson_ci_upper"]), hi, 5e-10)

    sens = {r["sensitivity_id"]: r for r in read_csv("results/h2_sensitivity_results_expected.csv")}
    ex_edit = [r for r in cat_rows if not as_bool(r["edited_note_flag"])]
    ex_k = sum(1 for r in ex_edit if as_bool(r["categorical_correct"]))
    lo, hi = wilson(ex_k, len(ex_edit))
    exp = sens["EXCLUDE_EDITED_NOTES"]
    add(checks, "H2.sens.exclude_edited.n", int(exp["eligible_n"]), len(ex_edit))
    add(checks, "H2.sens.exclude_edited.estimate", float(exp["estimate"]), ex_k/len(ex_edit), 1e-15)
    add(checks, "H2.sens.exclude_edited.wilson_lower", float(exp["ci_lower"]), lo, 5e-10)
    add(checks, "H2.sens.exclude_edited.wilson_upper", float(exp["ci_upper"]), hi, 5e-10)
    add(checks, "H2.sens.exclude_edited.binomial_p", float(exp["p_two_sided"]), binom2(ex_k, len(ex_edit)), 1e-15)
    loso = []
    for series in sorted({r["series_id"] for r in cat_rows}):
        sub = [r for r in cat_rows if r["series_id"] != series]
        loso.append(sum(1 for r in sub if as_bool(r["categorical_correct"])) / len(sub))
    exp = sens["LEAVE_ONE_SERIES_OUT_ACCURACY_RANGE"]
    add(checks, "H2.sens.loso.estimate", float(exp["estimate"]), k/len(cat_rows), 1e-15)
    add(checks, "H2.sens.loso.lower", float(exp["ci_lower"]), min(loso), 1e-15)
    add(checks, "H2.sens.loso.upper", float(exp["ci_upper"]), max(loso), 1e-15)
    for sid in ["STRUCTURED_FIELD_ONLY_CALLS", "EXCLUDE_STRUCTURED_PROSE_CONFLICT_FLAGS"]:
        exp = sens[sid]
        add(checks, "H2.sens." + sid + ".n", int(exp["eligible_n"]), len(cat_rows))
        add(checks, "H2.sens." + sid + ".estimate", float(exp["estimate"]), k/len(cat_rows), 1e-15)
        add(checks, "H2.sens." + sid + ".p", float(exp["p_two_sided"]), binom2(k, len(cat_rows)), 1e-15)
    cap = read_csv("data/cap_frozen_evaluation_input.csv")
    overtime_rate = sum(1 for r in cap if as_bool(r["overtime"])) / len(cap)
    exp = sens["OVERTIME_DESCRIPTION_SEPARATE_FROM_REGULATION"]
    add(checks, "H2.sens.overtime.rate", float(exp["estimate"]), overtime_rate, 1e-15)

    post = read_csv("data/posthoc_winner_forecast_comparison.csv")
    ps = read_json("results/posthoc_machine_readable_summary_expected.json")
    rules = {r["rule"]: r for r in ps["winner_forecast_rules"]}
    for rule, col in [("R_FACTOR", "rfactor_correct"), ("ALWAYS_HOME", "always_home_correct"), ("ALWAYS_HIGHER_SEED", "always_higher_seed_correct")]:
        kk = sum(1 for r in post if as_bool(r[col]))
        add(checks, "posthoc." + rule + ".eligible_n", rules[rule]["eligible_n"], len(post))
        add(checks, "posthoc." + rule + ".correct", rules[rule]["correct_k"], kk)
        add(checks, "posthoc." + rule + ".accuracy", rules[rule]["accuracy"], kk/len(post), 1e-15)
    paired = ps["paired_benchmark_tests"]
    for bid, col in [("ALWAYS_HOME", "always_home_correct"), ("ALWAYS_HIGHER_SEED", "always_higher_seed_correct")]:
        bd = sum(1 for r in post if as_bool(r["rfactor_correct"]) and not as_bool(r[col]))
        cd = sum(1 for r in post if (not as_bool(r["rfactor_correct"])) and as_bool(r[col]))
        add(checks, "posthoc.mcnemar." + bid, paired[bid]["exact_mcnemar_p_two_sided"], mcnemar(bd, cd), 1e-15)

    c1_exp = {r["endpoint_id"]: r for r in read_csv("results/cap_convergent_association_c1_results_expected.csv")}
    c1_p = []
    for ep, comp_col in [("C1_A", "team_led_longer"), ("C1_B", "halftime_leader"), ("C1_C", "largest_lead_team")]:
        table = {("HOME", "HOME"): 0, ("HOME", "AWAY"): 0, ("AWAY", "HOME"): 0, ("AWAY", "AWAY"): 0}
        for r in cap:
            loc, comp = r["cap_controller_location"], r[comp_col]
            if r["cap_determinacy_status"] == "DETERMINATE" and loc in {"HOME", "AWAY"} and comp in {"HOME", "AWAY"}:
                table[(loc, comp)] += 1
        a, bc, cc, d = table[("HOME", "HOME")], table[("HOME", "AWAY")], table[("AWAY", "HOME")], table[("AWAY", "AWAY")]
        n = a + bc + cc + d
        agree = a + d
        lo, hi = wilson(agree, n)
        p = fisher(a, bc, cc, d)
        c1_p.append((ep, p))
        exp = c1_exp[ep]
        add(checks, "CAP." + ep + ".eligible_n", int(exp["eligible_n"]), n)
        add(checks, "CAP." + ep + ".agreement_count", int(exp["agreement_count"]), agree)
        add(checks, "CAP." + ep + ".agreement_proportion", float(exp["agreement_proportion"]), agree/n, 1e-15)
        add(checks, "CAP." + ep + ".wilson_lower", float(exp["wilson_95_ci_lower"]), lo, 5e-10)
        add(checks, "CAP." + ep + ".wilson_upper", float(exp["wilson_95_ci_upper"]), hi, 5e-10)
        add(checks, "CAP." + ep + ".fisher_raw", float(exp["fisher_exact_two_sided_p_raw"]), p, 1e-15)
    hadj = holm(c1_p)
    for ep, (_, adjusted) in hadj.items():
        add(checks, "CAP." + ep + ".holm", float(c1_exp[ep]["fisher_exact_two_sided_p_holm"]), adjusted, 1e-15)

    for rel, prefix in [("results/cap_convergent_association_a1_results_expected.csv", "A1"), ("results/cap_convergent_association_s1_results_expected.csv", "S1")]:
        for exp in read_csv(rel):
            pairs = [(float(r[exp["x_variable"]]), float(r[exp["y_variable"]])) for r in cap if r[exp["x_variable"]] != "" and r[exp["y_variable"]] != ""]
            add(checks, "CAP." + prefix + "." + exp["endpoint_id"] + ".spearman", float(exp["spearman_rho"]), spearman([x for x, _ in pairs], [y for _, y in pairs]), 1e-12)

    for exp in read_csv("results/cap_convergent_association_b1_results_expected.csv"):
        var = exp["group_variable"]
        if exp["endpoint_id"] == "B1_1":
            g1 = [float(r["absolute_cap_share_gap"]) for r in cap if as_bool(r[var])]
            g2 = [float(r["absolute_cap_share_gap"]) for r in cap if not as_bool(r[var])]
        else:
            g1 = [float(r["absolute_cap_share_gap"]) for r in cap if as_bool(r[var])]
            g2 = [float(r["absolute_cap_share_gap"]) for r in cap if not as_bool(r[var])]
        add(checks, "CAP.B1." + exp["endpoint_id"] + ".group1_n", int(exp["group1_n"]), len(g1))
        add(checks, "CAP.B1." + exp["endpoint_id"] + ".group2_n", int(exp["group2_n"]), len(g2))
        add(checks, "CAP.B1." + exp["endpoint_id"] + ".group1_median", float(exp["group1_median"]), q7(g1, .5), 1e-15)
        add(checks, "CAP.B1." + exp["endpoint_id"] + ".group2_median", float(exp["group2_median"]), q7(g2, .5), 1e-15)
        add(checks, "CAP.B1." + exp["endpoint_id"] + ".u", float(exp["mann_whitney_u_named_first_group"]), mann_whitney_u(g1, g2), 1e-12)

    status = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    out = ROOT / "generated_results"
    out.mkdir(exist_ok=True)
    (out / "reproduction_summary.json").write_text(json.dumps({"status": status, "check_count": len(checks), "checks": checks}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(status)
    print(f"check_count={len(checks)}")
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
