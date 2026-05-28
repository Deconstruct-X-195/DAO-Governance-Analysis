import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
output_dir = "E:\\PYTHON练习册\\dao_research"

sus = pd.read_csv(
    os.path.join(output_dir, "wash_trade_suspicious.csv"),
    encoding="utf-8-sig"
)
df = pd.read_csv(
    os.path.join(output_dir, "wash_trade_analysis.csv"),
    encoding="utf-8-sig"
)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("PEPE Token Wash Trade Detection Analysis", fontsize=14)

# 图1：切换间隔分布
axes[0].hist(sus["interval_min"], bins=20, color="#E74C3C", edgecolor="white")
axes[0].set_xlabel("Time Interval Between Buy/Sell Switch (minutes)")
axes[0].set_ylabel("Count")
axes[0].set_title("Distribution of Buy-Sell Switch Intervals")
axes[0].axvline(x=sus["interval_min"].mean(), color="black",
                linestyle="--", label=f"Mean: {sus['interval_min'].mean():.1f} min")
axes[0].legend()

# 图2：最可疑地址出现频次
top_addrs = sus["address"].value_counts().head(8)
short_labels = [a[:8]+"..." for a in top_addrs.index]
axes[1].barh(short_labels, top_addrs.values, color="#3498DB")
axes[1].set_xlabel("Number of Suspicious Switches")
axes[1].set_title("Top Suspicious Addresses by Frequency")

# 图3：可疑交易量分布（log scale）
volumes = sus["volume1"].replace(0, 1)
axes[2].hist(volumes, bins=20, color="#2ECC71", edgecolor="white")
axes[2].set_xlabel("Token Volume per Transaction")
axes[2].set_ylabel("Count")
axes[2].set_title("Volume Distribution of Suspicious Trades")
axes[2].set_xscale("log")

plt.tight_layout()

img_path = os.path.join(output_dir, "wash_trade_detection.png")
plt.savefig(img_path, dpi=150, bbox_inches="tight")
print(f"图表已保存到：{img_path}")
plt.show()