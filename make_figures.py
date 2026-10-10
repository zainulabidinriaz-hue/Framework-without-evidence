"""Figures for: Frameworks Without Evidence? (Riaz et al.)
Produces fig_overview.png, fig_pipeline.png, fig_trajectories.png, fig_tradeoff.png.
Run: python3 make_figures.py   (needs numpy, matplotlib; reads results.json from trust_sim.py)"""
import json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
INK, MUTED, GRID = "#1f2328", "#6e7781", "#d0d7de"
BLUE, RED, FILL = "#1f6feb", "#c0392b", "#f6f8fa"
DPI = 300


def box(ax, x, y, w, h, text, fc=FILL, ec="#8c959f", fs=9.5, bold_first=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=1.1))
    lines = text.split("\n")
    if bold_first and len(lines) > 1:
        ax.text(x + w / 2, y + h - 0.2, lines[0], ha="center", va="top", fontsize=fs,
                weight="bold", color=INK)
        ax.text(x + w / 2, y + h - 0.2 - fs / 30, "\n".join(lines[1:]), ha="center", va="top",
                fontsize=fs - 1.2, color=INK, linespacing=1.3)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK)


def arrow(ax, x1, y1, x2, y2, color="#57606a"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, shrinkA=0, shrinkB=0))


# ---------------- Figure 1: study overview ----------------
def fig_overview():
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
    ax.text(0.05, 5.4, "Part A: Validation audit (Sections 3\u20134)", fontsize=10, weight="bold", color=INK, va="top")
    ax.text(0.05, 2.75, "Part B: Analysis of one runtime mechanism (Sections 5\u20137)", fontsize=10,
            weight="bold", color=INK, va="top")
    w, h, y1 = 2.95, 1.4, 3.55
    xs = [0.05, 3.5, 6.95]
    box(ax, xs[0], y1, w, h, "Corpus\n9 publications, 2025\u20132026\n(frameworks and reviews)", fs=9)
    box(ax, xs[1], y1, w, h, "Inclusion\n5 papers propose their own\nframework; 4 reviews excluded", fs=9)
    box(ax, xs[2], y1, w, h, "Audit\n10 criteria \u00d7 5 frameworks\n= 50 cells; only 3 fully met", fc="#eaf2ff", ec=BLUE, fs=9)
    arrow(ax, xs[0] + w, y1 + h / 2, xs[1], y1 + h / 2)
    arrow(ax, xs[1] + w, y1 + h / 2, xs[2], y1 + h / 2)
    w2, h2, y2 = 2.3, 1.75, 0.15
    xs2 = [0.05, 2.55, 5.05, 7.55]
    box(ax, xs2[0], y2, w2, h2, "Selection\nTAZAI trust model,\nthe most precisely\nspecified mechanism", fs=9.5)
    box(ax, xs2[1], y2, w2, h2, "Formal analysis\nfour propositions\nwith proofs\n(Section 5)", fs=9.5)
    box(ax, xs2[2], y2, w2, h2, "Simulation\nseeded Monte Carlo,\n4,000\u201320,000 runs\n(Section 6)", fs=9.5)
    box(ax, xs2[3], y2, w2, h2, "Protocol\n7 attack families,\n10-item checklist\n(Section 7)", fc="#eaf2ff", ec=BLUE, fs=9.5)
    for i in range(3):
        arrow(ax, xs2[i] + w2, y2 + h2 / 2, xs2[i + 1], y2 + h2 / 2)
    ax.plot([xs[2] + w / 2, xs[2] + w / 2, 9.85, 9.85], [y1, 3.1, 3.1, 3.1], color="#57606a", lw=1.2)
    ax.plot([9.85, 9.85], [3.1, 2.15], color="#57606a", lw=1.2)
    ax.plot([9.85, 1.2], [2.15, 2.15], color="#57606a", lw=1.2)
    arrow(ax, 1.2, 2.15, 1.2, y2 + h2)
    fig.savefig("fig_overview.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------- Figure 2: TAZAI pipeline and failure points ----------------
def tag(ax, x, y, label):
    ax.add_patch(FancyBboxPatch((x - 0.22, y - 0.15), 0.44, 0.3, boxstyle="round,pad=0.01,rounding_size=0.08",
                                fc=RED, ec=RED))
    ax.text(x, y, label, ha="center", va="center", fontsize=7.5, weight="bold", color="white")


def fig_pipeline():
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 10.6); ax.set_ylim(0, 6.7); ax.axis("off")
    for i, (sym, name) in enumerate([("I", "identity confidence"), ("B(t)", "behavioural consistency"),
                                     ("C(t)", "contextual compliance")]):
        y = 5.0 - i * 1.0
        box(ax, 0.05, y, 2.15, 0.82, f"{sym}\n{name}", fs=8.0)
        arrow(ax, 2.2, y + 0.41, 2.45, 4.45)
    box(ax, 2.45, 3.95, 1.95, 1.0, "Weighted score\n\u03b1I + \u03b2B + \u03b3C", fs=8.2)
    tag(ax, 4.3, 4.95, "P1")
    arrow(ax, 4.4, 4.45, 4.8, 4.45)
    box(ax, 4.8, 3.95, 2.0, 1.0, "Decay\nT \u2190 T\u00b7e^(\u2212\u03bbR)", fs=9)
    tag(ax, 6.2, 4.95, "P2"); tag(ax, 6.7, 4.95, "P3")
    box(ax, 4.8, 5.65, 2.0, 0.85, "Monitor\nrisk score R per action", fs=8.2)
    arrow(ax, 5.8, 5.65, 5.8, 4.95)
    arrow(ax, 6.8, 4.45, 7.2, 4.45)
    box(ax, 7.2, 3.95, 1.75, 1.0, "Access check\nT \u2265 \u03c4 ?", fs=8.2)
    arrow(ax, 8.95, 4.65, 9.3, 5.0); arrow(ax, 8.95, 4.25, 9.3, 3.9)
    box(ax, 9.3, 4.8, 1.25, 0.6, "allow", fc="#eef7ee", ec="#2f8f46", bold_first=False, fs=9)
    box(ax, 9.3, 3.55, 1.25, 0.6, "revoke", fc="#fdecea", ec=RED, bold_first=False, fs=9)
    box(ax, 4.8, 2.3, 2.0, 1.0, "Group score\naverage trust\nof n agents", fs=9)
    tag(ax, 6.7, 3.3, "P4")
    arrow(ax, 5.8, 3.95, 5.8, 3.3)
    arrow(ax, 6.8, 2.8, 7.2, 2.8)
    box(ax, 7.2, 2.3, 1.75, 1.0, "Group check\nmean \u2265 \u03c4 ?", fs=8.2)
    # legend of failure points
    items = [("P1", "Heavy identity weight lets credentials outvote behaviour"),
             ("P2", "Decay never refills, so honest agents are eventually revoked"),
             ("P3", "Adding recovery lets an attacker cause harm at a steady rate"),
             ("P4", "The group average hides a compromised agent")]
    ax.add_patch(FancyBboxPatch((0.05, 0.05), 10.5, 1.85, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#fdf6f5", ec="#e6b8b2", lw=0.9))
    for j, (lab, txt) in enumerate(items):
        yy = 1.6 - j * 0.42
        tag(ax, 0.45, yy, lab)
        ax.text(0.8, yy, f"{txt} (Proposition {lab[1]})", va="center", fontsize=8.5, color=INK)
    fig.savefig("fig_pipeline.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------- simulation helpers (same model as trust_sim.py) ----------------
T0, TAU, LAM, P_FLAG, R_MAX, RH, K = 0.9, 0.7, 1.0, 0.05, 0.2, 0.1, 20


def trajectories(rho, attacker, runs, H, rng):
    R = (rng.random((runs, H)) < P_FLAG) * rng.uniform(0, R_MAX, (runs, H))
    if attacker:
        R[:, K - 1::K] += RH
    L = np.full(runs, math.log(T0)); out = np.empty((runs, H)); alive = np.ones(runs, bool)
    rev = np.full(runs, H)
    for t in range(H):
        L = np.where(alive, np.minimum(math.log(T0), L - LAM * R[:, t] + rho), L)
        out[:, t] = np.exp(L)
        newly = alive & (L < math.log(TAU)); rev[newly] = t; alive &= ~newly
    return out, rev


def fig_trajectories():
    rng = np.random.default_rng(20261010)
    H, runs = 300, 400
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    for ax, rho, title in [(axes[0], 0.0, "No recovery (TAZAI, ρ = 0)"),
                           (axes[1], 0.02, "With recovery (ρ = 0.02)")]:
        for attacker, color, name in [(False, "#8c959f", "Honest agent"), (True, BLUE, "Periodic attacker")]:
            tr, rev = trajectories(rho, attacker, runs, H, rng)
            med = np.median(rev)
            i = int(np.argmin(np.abs(rev - med)))  # run closest to the median outcome
            stop = rev[i] if rev[i] < H else H - 1
            ax.plot(np.arange(stop + 1), tr[i, :stop + 1], color=color, lw=1.4, label=name)
            if rev[i] < H:
                ax.plot(rev[i], tr[i, rev[i]], marker="x", color=RED, ms=7, mew=2)
        ax.axhline(TAU, color=INK, ls="--", lw=1)
        if rho > 0:
            ax.text(4, TAU + 0.006, "threshold τ = 0.7", ha="left", va="bottom", fontsize=8, color=MUTED)
        ax.set_title(title, fontsize=9.5, color=INK)
        ax.set_xlim(0, H); ax.set_ylim(0.55, 0.92)
        ax.set_xlabel("Step")
        ax.grid(axis="y", color=GRID, lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0].set_ylabel("Trust score T")
    axes[1].plot([], [], marker="x", color=RED, ls="", mew=2, label="Revoked")
    axes[1].legend(loc="lower left", fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig("fig_trajectories.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------- Figure: trade-off curve (from results.json) ----------------
def fig_tradeoff():
    rows = json.load(open("results.json"))["exp2_decay"]["rows"]
    x = [100 * r["benign_revoked"] for r in rows]
    yp = [r["periodic_harms"] for r in rows]
    ya = [r["adaptive_harms"] for r in rows]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x, yp, "-o", color=BLUE, lw=1.6, ms=5, label="Periodic attacker")
    ax.plot(x, ya, "-s", color="#8c959f", lw=1.4, ms=4.5, label="Adaptive attacker")
    for xi, yi, r in zip(x, yp, rows):
        lab = "ρ = 0 (TAZAI)" if r["rho"] == 0 else f"ρ = {r['rho']:g}"
        above = r["rho"] >= 0.015
        ax.annotate(lab, (xi, yi), textcoords="offset points", xytext=(-6, 6) if above else (5, -13),
                    ha="right" if above else "left", fontsize=7.5, color=INK)
    ax.set_ylim(0, 14.5)
    ax.invert_xaxis()
    ax.set_xlabel("Honest agents falsely revoked within 500 steps (%)")
    ax.set_ylabel("Harmful actions completed (mean)")
    ax.set_title("Fewer false revocations always means more attacker harm", fontsize=10, color=INK)
    ax.annotate("more recovery →", xy=(0.62, 0.06), xycoords="axes fraction", fontsize=8, color=MUTED)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig("fig_tradeoff.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig_overview(); fig_pipeline(); fig_trajectories(); fig_tradeoff()
    print("figures written")


# ================= additional explanatory figures =================
def fig_audit_heatmap():
    import csv
    rows = list(csv.DictReader(open("audit_coding_sheet.csv")))
    fws = ["Leo et al. [1]", "MAAIS [2]", "AGENTSAFE [3]", "Radanliev et al. [4]", "TAZAI [6]"]
    crit = []
    for r in rows:
        if r["criterion"] not in crit:
            crit.append(r["criterion"])
    code = {(r["framework"], r["criterion"]): r["code"] for r in rows}
    col = {"Y": "#2f8f46", "P": "#e3b341", "N": "#e6e9ec"}
    txt = {"Y": "white", "P": INK, "N": MUTED}
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    for j, c in enumerate(crit):
        for i, f in enumerate(fws):
            v = code[(f, c)]
            ax.add_patch(plt.Rectangle((i, len(crit) - 1 - j), 0.94, 0.9, fc=col[v], ec="white"))
            ax.text(i + 0.47, len(crit) - 1 - j + 0.45, v, ha="center", va="center", fontsize=9,
                    color=txt[v], weight="bold")
    ax.set_xlim(-0.05, len(fws)); ax.set_ylim(-0.1, len(crit))
    ax.set_xticks([i + 0.47 for i in range(len(fws))])
    ax.set_xticklabels(fws, fontsize=8.5)
    ax.xaxis.tick_top()
    ax.set_yticks([len(crit) - 1 - j + 0.45 for j in range(len(crit))])
    ax.set_yticklabels(crit, fontsize=8.5)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=col["Y"], label="Yes: met, with evidence"),
                       Patch(fc=col["P"], label="Partial: specified or discussed, not tested on agents"),
                       Patch(fc=col["N"], label="No: absent")],
              loc="upper center", bbox_to_anchor=(0.42, -0.02), ncol=3, fontsize=7.5, frameon=False)
    fig.savefig("fig_audit.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig_threat_model():
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    ax.set_xlim(0, 10.6); ax.set_ylim(0, 5.2); ax.axis("off")
    box(ax, 0.05, 3.7, 2.0, 1.15, "Attacker\nwrites hidden\ninstructions", fc="#fdecea", ec=RED, fs=8.8)
    box(ax, 2.45, 3.7, 2.55, 1.15, "Poisoned content\nweb page, email\nor document", fs=8.8)
    box(ax, 0.05, 1.6, 2.0, 1.15, "User\ngives the agent\na normal task", fs=8.8)
    box(ax, 5.55, 2.45, 2.45, 1.5, "Hijacked agent\nvalid credentials (I = 1)\nnormal context (C \u2248 1)\nbehaviour changed", fc="#fff5e6", ec="#d4a017", fs=8.8)
    box(ax, 8.4, 3.7, 2.15, 1.15, "Harmful tool\nactions, each made\nto look ordinary", fc="#fdecea", ec=RED, fs=8.8)
    box(ax, 8.4, 1.35, 2.15, 1.15, "Monitor\nsmall risk score r\u2095\nper harmful action", fs=8.8)
    box(ax, 5.55, 0.1, 2.45, 1.1, "Trust score\nstays above \u03c4,\naccess continues", fc="#eaf2ff", ec=BLUE, fs=8.8)
    arrow(ax, 2.05, 4.27, 2.45, 4.27)
    arrow(ax, 5.0, 3.9, 5.55, 3.55)
    ax.text(5.3, 4.05, "agent reads it through a tool", fontsize=7.5, color=MUTED, ha="left", va="bottom")
    arrow(ax, 2.05, 2.17, 5.55, 2.85)
    arrow(ax, 8.0, 3.6, 8.4, 4.0)
    arrow(ax, 9.47, 3.7, 9.47, 2.5)
    arrow(ax, 8.4, 1.6, 8.0, 0.75)
    ax.annotate("", xy=(6.77, 2.45), xytext=(6.77, 1.2),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2, ls=(0, (3, 2))))
    ax.text(6.87, 1.75, "loop repeats", fontsize=7.5, color=BLUE)
    fig.savefig("fig_threat.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig_behaviour_floor():
    beta = np.linspace(0.01, 1, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    shades = {0.6: 0.45, 0.7: 1.0, 0.8: 0.7}
    for tau, a in [(0.6, 0.45), (0.7, 1.0), (0.8, 0.7)]:
        bmin = np.maximum(0, 1 - (1 - tau) / beta)
        ax.plot(beta, bmin, color=BLUE if tau == 0.7 else "#8c959f", lw=2 if tau == 0.7 else 1.4,
                alpha=1 if tau == 0.7 else a)
        ax.text(0.99, 1 - (1 - tau) / 0.99 + 0.02, f"τ = {tau}", ha="right", va="bottom", fontsize=8,
                color=BLUE if tau == 0.7 else MUTED)
    ax.axvspan(0, 0.3, color="#fdecea", alpha=0.7, lw=0)
    ax.text(0.15, 0.62, "For τ = 0.7:\nany behaviour\npasses when\nβ ≤ 0.3", ha="center", fontsize=8, color=RED)
    for b, lab in [(1 / 3, "equal weights\nβ = 1/3 → B_min = 0.1"), (0.3, "")]:
        pass
    ax.plot([1 / 3], [0.1], "o", color=BLUE, ms=6)
    ax.annotate("equal weights: β = 1/3,\nB_min = 0.1", (1 / 3, 0.1), textcoords="offset points",
                xytext=(80, -14), fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel("Behaviour weight β")
    ax.set_ylabel("Minimum behaviour score to pass, B_min")
    ax.set_title("A hijacked agent with valid credentials needs very little good behaviour to pass",
                 fontsize=9.5, color=INK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig("fig_floor.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig_group_rules():
    benign = np.array([0.84, 0.86, 0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.95])
    comp = 0.5
    allv = np.append(benign, comp)
    mean = allv.mean(); med = np.median(allv)
    mad = 1.4826 * np.median(np.abs(allv - med))
    lo = med - 3.5 * mad
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    ax.axvline(TAU, color=INK, ls="--", lw=1)
    ax.text(TAU, 1.62, "threshold τ = 0.7", ha="center", fontsize=8, color=INK)
    ax.axvspan(lo, 1.0, ymin=0.02, ymax=0.3, color="#eaf2ff", lw=0)
    ax.scatter(benign, np.zeros_like(benign) + 0.3, s=45, color="#8c959f", zorder=3, label="Benign agents")
    ax.scatter([comp], [0.3], s=60, color=RED, zorder=3, label="Compromised agent")
    rules = [(1.25, "Mean rule (TAZAI)", mean, f"average = {mean:.3f} ≥ τ → no alarm", "#8c959f"),
             (0.95, "Min rule", comp, f"lowest {comp} < τ → alarm", RED),
             (0.65, "Robust-z rule", lo, f"agent far below median ({med:.3f}) → alarm", RED)]
    for y, name, x, text, c in rules:
        ax.plot([x], [y], marker="v", color=c, ms=8)
        ax.text(0.405, y, name, fontsize=8.5, weight="bold", color=INK, va="center")
        ax.text(x + 0.012, y, text, fontsize=8, color=INK, va="center", ha="left")
    ax.text(lo + 0.005, 0.06, "robust range: median ± 3.5 MAD", fontsize=7.5, color=BLUE)
    ax.set_xlim(0.4, 1.13); ax.set_ylim(-0.02, 1.75)
    ax.set_yticks([]); ax.set_xlabel("Trust score")
    ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.spines["bottom"].set_bounds(0.4, 1.0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="upper right", fontsize=7.5, frameon=False, bbox_to_anchor=(1.0, 1.08), ncol=2)
    fig.savefig("fig_rules.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig_attack_timelines():
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    H = 100
    names = ["A1 Low-and-slow", "A2 Payload splitting", "A3 Delayed memory poisoning", "A4 Gradual goal drift"]
    for k, n in enumerate(names):
        y = 3 - k
        ax.plot([0, H], [y, y], color=GRID, lw=6, solid_capstyle="butt", zorder=1)
        ax.text(-2, y, n, ha="right", va="center", fontsize=8.5, weight="bold", color=INK)
    # A1
    for t in range(15, H, 20):
        ax.plot(t, 3, marker="v", color=RED, ms=8, zorder=3)
    ax.text(50, 3.28, "one small harmful action at a time, spaced to stay under the trust budget",
            ha="center", fontsize=7.5, color=MUTED)
    # A2
    for t, lab in [(12, "1/3"), (38, "2/3"), (64, "3/3")]:
        ax.plot(t, 2, marker="s", color="#d4a017", ms=8, zorder=3)
        ax.text(t, 2.2, lab, ha="center", fontsize=7.5, color=INK)
    ax.plot(64, 2, marker="v", color=RED, ms=9, zorder=4)
    ax.text(68, 2.2, "pieces combine: attack executes", fontsize=7.5, color=INK, va="bottom")
    ax.text(25, 1.72, "each fragment looks harmless on its own", ha="center", fontsize=7.5, color=MUTED)
    # A3
    ax.plot(8, 1, marker="D", color="#d4a017", ms=7, zorder=3)
    ax.text(8, 1.2, "planted in memory", ha="center", fontsize=7.5, color=INK)
    ax.plot([8, 80], [1, 1], color="#d4a017", lw=1.2, ls=(0, (2, 2)), zorder=2)
    ax.text(44, 0.72, "dormant across sessions", ha="center", fontsize=7.5, color=MUTED)
    ax.plot(80, 1, marker="v", color=RED, ms=9, zorder=3)
    ax.text(80, 1.2, "triggered later", ha="center", fontsize=7.5, color=INK)
    # A4
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list("drift", ["#8c959f", RED])
    for t in range(0, H, 2):
        ax.plot([t, t + 2], [0, 0], color=cm(t / H), lw=6, solid_capstyle="butt", zorder=2)
    ax.text(2, -0.3, "user's goal", fontsize=7.5, color=MUTED)
    ax.text(H - 2, -0.3, "attacker's goal", fontsize=7.5, color=RED, ha="right")
    ax.text(50, -0.3, "each step changes the goal only slightly", ha="center", fontsize=7.5, color=MUTED)
    ax.set_xlim(-42, H + 2); ax.set_ylim(-0.55, 3.5)
    ax.set_yticks([]); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Agent step (illustrative)")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_bounds(0, H)
    fig.savefig("fig_attacks.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig_audit_heatmap(); fig_threat_model(); fig_behaviour_floor(); fig_group_rules(); fig_attack_timelines()
    print("extra figures written")
