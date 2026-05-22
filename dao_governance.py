import requests
import pandas as pd
import os

url = "https://hub.snapshot.org/graphql"

query = """
{
  proposals(
    where: { space_in: ["uniswapgovernance.eth"] }
    orderBy: "created"
    orderDirection: desc
    first: 20
  ) {
    id
    title
    start
    end
    state
    votes
    scores_total
  }
}
"""

response = requests.post(url, json={"query": query})
data = response.json()

proposals = data["data"]["proposals"]
df = pd.DataFrame(proposals)

df["start"] = pd.to_datetime(df["start"], unit="s")
df["end"] = pd.to_datetime(df["end"], unit="s")

# 计算平均每票持有UNI数量
df["avg_tokens_per_voter"] = df["scores_total"] / df["votes"]
df["scores_total_M"] = (df["scores_total"] / 1e6).round(2)
df["avg_tokens_per_voter_M"] = (df["avg_tokens_per_voter"] / 1e6).round(2)

# 保存CSV
output_dir = "******"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "uniswap_proposals.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"数据已保存到：{csv_path}\n")

print(f"共获取 {len(df)} 个提案\n")
print(df[["title", "votes", "scores_total_M", "avg_tokens_per_voter_M"]].to_string())
print(f"\n平均每票持有UNI（百万）：{df['avg_tokens_per_voter_M'].mean():.2f}M")
print(f"最高：{df['avg_tokens_per_voter_M'].max():.2f}M")
print(f"最低：{df['avg_tokens_per_voter_M'].min():.2f}M")
