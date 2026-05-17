import os
import numpy as np
import pandas as pd

output_dir = "E:\\PYTHON练习册\\dao_research"

# 1. 安全读取投票数据
try:
    votes_df = pd.read_csv(
        os.path.join(output_dir, "uniswap_votes.csv"), encoding="utf-8-sig"
    )
except Exception as e:
    votes_df = pd.read_csv(
        os.path.join(output_dir, "uniswap_votes.csv"),
        encoding="utf-8",
        errors="ignore",
    )

# 2. 安全读取提案数据（加入多重编码兼容，解决 0xa1 报错）
proposals_path = os.path.join(output_dir, "uniswap_proposals.csv")
try:
    proposals_df = pd.read_csv(proposals_path, encoding="gb18030")
except UnicodeDecodeError:
    try:
        proposals_df = pd.read_csv(proposals_path, encoding="utf-8-sig")
    except Exception as e:
        proposals_df = pd.read_csv(
            proposals_path, encoding="utf-8", errors="ignore"
        )
        print("警告：读取提案文件时自动忽略了部分特殊乱码字符。")


def gini(array):
    """计算基尼系数"""
    array = np.array(array, dtype=float)
    array = array[array > 0]  # 过滤零值或负值（有些特殊链上投票可能存在0票）
    if len(array) <= 1:
        return 0  # 只有一个人投票或者没人投票时，基尼系数无意义，设为 0
    array = np.sort(array)
    n = len(array)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * array) / (n * np.sum(array))) - (n + 1) / n


# 3. 按提案计算治理集中度指标
results = []
for pid, group in votes_df.groupby("proposal_id"):
    # 确保投票权重列（vp）为数值型，填充空值为 0
    vp_values = pd.to_numeric(group["vp"], errors="coerce").fillna(0).values

    g = gini(vp_values)
    voter_count = len(group)
    total_vp = vp_values.sum()

    # 计算前10名巨鲸的投票集中度
    top10_vp = group.nlargest(10, "vp")["vp"].sum() if voter_count > 0 else 0
    top10_pct = top10_vp / total_vp * 100 if total_vp > 0 else 0

    results.append(
        {
            "proposal_id": pid,
            "voter_count": voter_count,
            "total_vp_M": round(total_vp / 1e6, 2),
            "gini": round(g, 4),
            "top10_voters_pct": round(top10_pct, 2),
        }
    )

results_df = pd.DataFrame(results)

# 4. 关联提案标题（为了防止 id 列有空格，进行去空格处理）
proposals_df["id"] = proposals_df["id"].astype(str).str.strip()
results_df["proposal_id"] = results_df["proposal_id"].astype(str).str.strip()

results_df = results_df.merge(
    proposals_df[["id", "title"]],
    left_on="proposal_id",
    right_on="id",
    how="left",
)

# 5. 打印分析报告
print("\n=== Uniswap DAO 治理权力集中度分析 ===\n")
# 如果有关联失败导致 title 为空的，用 id 代替显示
results_df["title"] = results_df["title"].fillna(results_df["proposal_id"])

print(
    results_df[
        ["title", "voter_count", "total_vp_M", "gini", "top10_voters_pct"]
    ].to_string(index=False)
)

print("-" * 50)
print(f"平均基尼系数：{results_df['gini'].mean():.4f}")
print(f"前10地址平均控制投票权：{results_df['top10_voters_pct'].mean():.2f}%")

# 6. 保存分析结果
out_path = os.path.join(output_dir, "dao_gini_analysis.csv")
results_df.to_csv(out_path, index=False, encoding="utf-8-sig")
print(f"\n分析结果已保存到：{out_path}")