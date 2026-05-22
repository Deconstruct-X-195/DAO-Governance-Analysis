import pandas as pd
import os

output_dir = "******"

df = pd.read_csv(
    os.path.join(output_dir, "fund_flow_raw.csv"),
    encoding="utf-8-sig"
)

print(f"总记录数：{len(df)}")
print(f"涉及地址标签：{df['address_label'].unique()}")
print(f"涉及代币种类：{df['tokenSymbol'].nunique()} 种")
print(f"时间范围：{df['timeStamp'].min()} 至 {df['timeStamp'].max()}")
print()

# 每个地址的交易概况
print("=== 各地址交易概况 ===")
summary = df.groupby("address_label").agg(
    总交易数=("tokenSymbol", "count"),
    涉及代币种数=("tokenSymbol", "nunique"),
    转出次数=("from", lambda x: (x == df.loc[x.index, "address"]).sum()),
    转入次数=("to", lambda x: (x == df.loc[x.index, "address"]).sum()),
).reset_index()
print(summary.to_string())
print()

# 四个地址之间是否有直接转账
print("=== 四个地址之间的直接资金流动 ===")
address_list = df["address"].str.lower().unique().tolist()

internal = df[
    df["from"].str.lower().isin(address_list) &
    df["to"].str.lower().isin(address_list)
]

if len(internal) > 0:
    print(f"发现 {len(internal)} 笔内部转账：")
    print(internal[["timeStamp", "from", "to", "tokenSymbol", "value"]].to_string())
else:
    print("四个地址之间未发现直接转账记录（在最近100条内）")

print()

# 每个地址最活跃的代币
print("=== 各地址最活跃代币TOP3 ===")
for label in df["address_label"].unique():
    sub = df[df["address_label"] == label]
    top = sub["tokenSymbol"].value_counts().head(3)
    print(f"{label}: {top.to_dict()}")
