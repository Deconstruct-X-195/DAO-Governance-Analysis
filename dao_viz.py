import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
output_dir = "E:\\PYTHON练习册\\dao_research"

df = pd.read_csv(
    os.path.join(output_dir, "dao_gini_analysis.csv"),
    encoding="utf-8-sig"
)

# 简化提案标题
df["short_title"] = df["title"].str[:30] + "..."

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Uniswap DAO Governance Power Concentration", fontsize=14)

# 图1：基尼系数
axes[0].barh(df["short_title"], df["gini"], color="#E74C3C")
axes[0].set_xlabel("Gini Coefficient (closer to 1 = more concentrated)")
axes[0].set_xlim(0, 1)
axes[0].axvline(x=df["gini"].mean(), color="black", linestyle="--", label=f"Mean: {df['gini'].mean():.3f}")
axes[0].legend()
axes[0].set_title("Voting Power Gini Coefficient")

# 图2：前10地址控制比例
axes[1].barh(df["short_title"], df["top10_voters_pct"], color="#3498DB")
axes[1].set_xlabel("% of Voting Power Controlled by Top 10 Addresses")
axes[1].set_xlim(0, 100)
axes[1].axvline(x=df["top10_voters_pct"].mean(), color="black", linestyle="--", label=f"Mean: {df['top10_voters_pct'].mean():.1f}%")
axes[1].legend()
axes[1].set_title("Top 10 Addresses Control (%)")

plt.tight_layout()

# 保存图片
img_path = os.path.join(output_dir, "dao_power_concentration.png")
plt.savefig(img_path, dpi=150, bbox_inches="tight")
print(f"图表已保存到：{img_path}")
plt.show()