"""Build every chart in /charts from the CSVs in /data.

Run from the repo root:
    python analysis/make_charts.py
"""
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "charts"
OUT.mkdir(exist_ok=True)

# Palette: one consistent set of colors for every chart
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK_2,
    "xtick.color": MUTED,
    "ytick.color": INK_2,
    "text.color": INK,
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "axes.titlesize": 14,
    "axes.titlelocation": "left",
})


def note(fig, text):
    fig.text(0.01, -0.06, text, fontsize=8.5, color=MUTED, ha="left", va="top")


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# 1. Market-size estimates disagree by ~60x
m = pd.read_csv(DATA / "market_estimates.csv")
fig, ax = plt.subplots(figsize=(8, 3.4))
labels = [f"{r.publisher}\n({r.scope}, {r.base_year})" for r in m.itertuples()]
bars = ax.barh(labels, m.base_value_usd_bn, color=BLUE, height=0.5)
for b, v in zip(bars, m.base_value_usd_bn):
    ax.text(b.get_width() + 3, b.get_y() + b.get_height() / 2, f"${v:,.2f}B",
            va="center", color=INK, fontsize=11, fontweight="bold")
ax.invert_yaxis()
ax.set_xlim(0, 215)
ax.xaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_xlabel("Estimated market size (US$ billions)")
ratio = m.base_value_usd_bn.max() / m.base_value_usd_bn.min()
ax.set_title(f"Historical publisher claims: values differ ~{ratio:.0f}x")
note(fig, "Sources: Exactitude Consultancy (Jul 2024); Research Nester. Different scope/base years; not comparable market estimates.")
save(fig, "market_estimates.png")

# 2. Germany: openness by age group (2025)
s = pd.read_csv(DATA / "consumer_surveys.csv")
age = s[(s.year == 2025) & s.group.str.startswith("Ages")]
fig, ax = plt.subplots(figsize=(7, 3.8))
bars = ax.bar(age.group.str.replace("Ages ", ""), age.value_pct, color=BLUE, width=0.55)
for b, v in zip(bars, age.value_pct):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v}%", ha="center", color=INK, fontweight="bold")
ax.axhline(24, color=MUTED, lw=1.2, ls="--")
ax.text(3.35, 25, "All adults: 24%", color=INK_2, fontsize=9.5, ha="right")
ax.set_ylim(0, 42)
ax.set_ylabel("% open to eating cultivated printed meat")
ax.set_xlabel("Age group")
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_title("Under-50s are about twice as open as older Germans")
note(fig, "Source: Bitkom 2025 release. Total n=1,004, aged 16+; subgroup n not disclosed.")
save(fig, "germany_openness_by_age.png")

# 3. Germany: 2019 vs 2025
trend = s[(s.group == "All adults 16+") & (s.metric == "Open to eating cultivated 3D-printed meat")]
fig, ax = plt.subplots(figsize=(5, 3.6))
bars = ax.bar(trend.year.astype(str), trend.value_pct, color=BLUE, width=0.45)
for b, v in zip(bars, trend.value_pct):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v}%", ha="center", fontweight="bold")
ax.set_ylim(0, 30)
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_ylabel("% open to eating it")
ax.set_title("Cultivated printed meat: stated openness in Germany")
note(fig, "Source: Bitkom 2025 release; 2019 retrospective comparator, original methodology not reviewed.")
save(fig, "germany_trend.png")

# 4. Steakholder printer throughput
fig, ax = plt.subplots(figsize=(7, 2.8))
names = ["MX200 meat printer\n(Fused Paste Layering)", "HD144 seafood printer\n(Drop Location in Space)"]
vals = [420, 100]
bars = ax.barh(names, vals, color=BLUE, height=0.5)
for b, v in zip(bars, vals):
    ax.text(v + 6, b.get_y() + b.get_height() / 2, f"{'up to ' if v == 420 else '~'}{v} kg/hr",
            va="center", fontweight="bold")
ax.invert_yaxis()
ax.set_xlim(0, 520)
ax.xaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_xlabel("Plant-based product per hour (kg)")
ax.set_title("Industrial food printers: Steakholder Foods' stated output")
note(fig, "Legacy supplier claims via Green Queen; not reverified. Rated output is not actual production.")
save(fig, "printer_throughput.png")

# 5. Timeline of milestones
t = pd.read_csv(DATA / "timeline.csv", parse_dates=["date"])
fig, ax = plt.subplots(figsize=(11, 5.2))
ax.axhline(0, color="#c3c2b7", lw=2, zorder=1)
for i, r in enumerate(t.itertuples()):
    color = ORANGE if r.company == "Texas" else BLUE
    level = [1.6, -1.6, 0.9, -0.9][i % 4]
    ax.plot([r.date, r.date], [0, level], color=GRID, lw=1, zorder=1)
    ax.scatter(r.date, 0, s=70, color=color, edgecolor=SURFACE, linewidth=2, zorder=3)
    va = "bottom" if level > 0 else "top"
    ax.text(r.date, level, f"{r.date:%b %Y}\n{r.company}", ha="center", va=va,
            fontsize=8.5, fontweight="bold", color=INK)
ax.set_ylim(-2.6, 2.6)
ax.yaxis.set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.scatter([], [], color=BLUE, label="Company milestone")
ax.scatter([], [], color=ORANGE, label="Regulation (Texas)")
ax.legend(loc="upper left", frameon=False, fontsize=9)
ax.set_title("3D-printed meat milestones, 2021-2026")
note(fig, "Details for each point in data/timeline.csv.")
save(fig, "timeline.png")

# 6. US state actions on cultivated meat
law = pd.read_csv(DATA / "us_state_laws.csv")
order = ["Sale ban", "Labeling", "Study"]
colors = {"Sale ban": BLUE, "Labeling": ORANGE, "Study": AQUA}
fig, ax = plt.subplots(figsize=(7, 3.6))
for x, kind in enumerate(order):
    states = law[law.action_type == kind].state.tolist()
    for y, st in enumerate(states):
        ax.add_patch(plt.Rectangle((x + 0.05, -y - 0.9), 0.9, 0.8, color=colors[kind], alpha=0.16, lw=0))
        weight = "bold" if st == "Texas" else "normal"
        ax.text(x + 0.5, -y - 0.5, st + (" *" if st == "Texas" else ""), ha="center", va="center",
                fontsize=10.5, fontweight=weight)
    ax.text(x + 0.5, 0.35, f"{kind} ({len(states)})", ha="center", fontweight="bold", color=colors[kind])
ax.set_xlim(0, 3)
ax.set_ylim(-3.2, 0.8)
ax.axis("off")
ax.set_title("Selected historical state records (not current legal status)")
note(fig, "Legacy selected sample; not a complete/current 50-state review. Consult current statutes and court orders.")
save(fig, "state_laws.png")
