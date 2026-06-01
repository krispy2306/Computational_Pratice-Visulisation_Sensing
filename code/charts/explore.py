

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Load data ─────────────────────────────────────────────────────────────────

CSV_PATH = "london_noise.csv"
df = pd.read_csv(CSV_PATH)

print("── Dataset overview ─────────────────────────────────────")
print(f"  Rows (measurement areas) : {len(df)}")
print(f"  Boroughs                 : {df['borough'].nunique()}")
print(f"  Columns                  : {list(df.columns)}")
print(f"\n── LAeq statistics ──────────────────────────────────────")
print(df["laeq"].describe().round(2))
print(f"\n── Date range ───────────────────────────────────────────")
print(f"  Earliest measurement : {df['first_measure'].min()}")
print(f"  Latest measurement   : {df['last_measure'].max()}")

os.makedirs("charts", exist_ok=True)

# ── Shared style ──────────────────────────────────────────────────────────────

plt.rcParams.update({
    "figure.facecolor": "#0e1117",
    "axes.facecolor":   "#181c26",
    "axes.edgecolor":   "#2a2f3d",
    "axes.labelcolor":  "#c8ccd8",
    "text.color":       "#c8ccd8",
    "xtick.color":      "#666e82",
    "ytick.color":      "#666e82",
    "grid.color":       "#2a2f3d",
    "font.family":      "monospace",
})

ACCENT = "#e05252"
BAR_COLOUR = "#378ADD"


# ── Chart 1: Histogram of all LAeq dB values ─────────────────────────────────
# Shows the overall distribution of noise levels across all measurement areas.

fig, ax = plt.subplots(figsize=(9, 5))
fig.suptitle("Sonic City Portrait — London NoiseCapture Data",
             fontsize=11, color="#c8ccd8", y=0.98)

ax.hist(df["laeq"], bins=40, color=ACCENT, edgecolor="#0e1117", linewidth=0.4, alpha=0.9)

mean_db = df["laeq"].mean()
ax.axvline(mean_db, color="#f5c542", linewidth=1.4, linestyle="--",
           label=f"Mean: {mean_db:.1f} dB")

ax.set_title("Distribution of LAeq values across all London measurement areas",
             fontsize=10, color="#666e82", pad=8)
ax.set_xlabel("LAeq dB(A)", labelpad=8)
ax.set_ylabel("Number of measurement areas", labelpad=8)
ax.legend(fontsize=9)
ax.grid(axis="y", linewidth=0.5)

plt.tight_layout()
plt.savefig("charts/01_laeq_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n✓ Saved charts/01_laeq_distribution.png")


# ── Chart 2: Mean LAeq per borough, sorted ────────────────────────────────────
# Immediately shows which boroughs are loudest / quietest on average.

borough_means = (
    df.groupby("borough")["laeq"]
      .mean()
      .sort_values(ascending=True)
      .round(1)
)

fig, ax = plt.subplots(figsize=(10, 8))
fig.suptitle("Sonic City Portrait — London NoiseCapture Data",
             fontsize=11, color="#c8ccd8", y=0.99)

bars = ax.barh(borough_means.index, borough_means.values,
               color=BAR_COLOUR, edgecolor="#0e1117", linewidth=0.3, alpha=0.9)

# # Colour the loudest 5 boroughs differently
# top5_threshold = borough_means.nlargest(5).min()
# for bar, val in zip(bars, borough_means.values):
#     if val >= top5_threshold:
#         bar.set_color(ACCENT)

# Value labels
for bar, val in zip(bars, borough_means.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}", va="center", fontsize=7.5, color="#c8ccd8")

ax.set_title("Mean LAeq dB(A) per London borough  (red = top 5 loudest)",
             fontsize=10, color="#666e82", pad=8)
ax.set_xlabel("Mean LAeq dB(A)", labelpad=8)
ax.set_xlim(right=borough_means.max() + 5)
ax.grid(axis="x", linewidth=0.5)
ax.tick_params(axis="y", labelsize=8)

plt.tight_layout()
plt.savefig("charts/02_borough_means.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Saved charts/02_borough_means.png")


# ── Chart 3: Measurement coverage per borough ─────────────────────────────────
# Highlights which boroughs have more data points — important for knowing
# where the visualisation will be reliable vs sparse.

borough_counts = (
    df.groupby("borough")["measure_count"]
      .sum()
      .sort_values(ascending=True)
)

fig, ax = plt.subplots(figsize=(10, 8))
fig.suptitle("Sonic City Portrait — London NoiseCapture Data",
             fontsize=11, color="#c8ccd8", y=0.99)

ax.barh(borough_counts.index, borough_counts.values,
        color="#44bb77", edgecolor="#0e1117", linewidth=0.3, alpha=0.85)

ax.set_title("Total individual measurements per London borough",
             fontsize=10, color="#666e82", pad=8)
ax.set_xlabel("Number of individual measurements", labelpad=8)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"{int(x):,}"
))
ax.grid(axis="x", linewidth=0.5)
ax.tick_params(axis="y", labelsize=8)

# Annotation: flag boroughs with very low coverage
low_coverage = borough_counts[borough_counts < borough_counts.quantile(0.25)]
for borough in low_coverage.index:
    idx = list(borough_counts.index).index(borough)
    ax.get_yticklabels()[idx].set_color("#e05252")

ax.annotate("⚠ Red labels = low coverage\n  (bottom 25% — treat with caution)",
            xy=(0.98, 0.05), xycoords="axes fraction",
            ha="right", fontsize=8, color="#e05252",
            bbox=dict(boxstyle="round,pad=0.4", fc="#181c26", ec="#2a2f3d"))

plt.tight_layout()
plt.savefig("charts/03_measurement_coverage.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Saved charts/03_measurement_coverage.png")

print("\nAll done. Open the charts/ folder to see your exploration output.")
print("These PNG files are your first portfolio screenshots.\n")
