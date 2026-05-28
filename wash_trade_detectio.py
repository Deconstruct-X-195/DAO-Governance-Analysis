import requests
import pandas as pd
import os
import time
from collections import defaultdict

API_KEY = "*******"
output_dir = "E:\\PYTHON练习册\\dao_research"

# 用Uniswap的PEPE/ETH池子作为分析对象
# 这是一个活跃的小币种池，洗售交易相对常见
TARGET_TOKEN = "0x6982508145454Ce325dDbE47a25d4ec3d2311933"  # PEPE token
TARGET_LABEL = "PEPE"

def get_token_transfers(token_address, pages=5):
    """拉取某代币的最近转账记录"""
    all_records = []
    for page in range(1, pages + 1):
        url = "https://api.etherscan.io/v2/api"
        params = {
            "chainid": "1",
            "module": "account",
            "action": "tokentx",
            "contractaddress": token_address,
            "page": page,
            "offset": 1000,
            "sort": "desc",
            "apikey": API_KEY
        }
        try:
            r = requests.get(url, params=params, timeout=15)
            data = r.json()
            if data["status"] == "1":
                all_records.extend(data["result"])
                print(f"第{page}页：获取到{len(data['result'])}条记录")
            else:
                print(f"第{page}页：{data.get('message')}")
                break
        except Exception as e:
            print(f"第{page}页请求失败：{e}")
            break
        time.sleep(0.3)
    return all_records

print(f"正在拉取{TARGET_LABEL}代币转账记录...")
records = get_token_transfers(TARGET_TOKEN, pages=3)
df = pd.DataFrame(records)
print(f"\n共获取{len(df)}条记录")

if len(df) > 0:
    # 基本处理
    df["timeStamp"] = pd.to_datetime(df["timeStamp"].astype(int), unit="s")
    df["value_token"] = df["value"].astype(float) / 1e18

    # === 检测1：同一地址短时间内既买又卖 ===
    print("\n=== 检测1：同一地址短时间内既买又卖（60分钟内）===")

    # 找出所有出现在from和to两侧的地址
    senders = set(df["from"].str.lower())
    receivers = set(df["to"].str.lower())
    both_sides = senders & receivers  # 既当买方又当卖方的地址
    print(f"既买又卖的地址数量：{len(both_sides)}")

    # 对每个双侧地址，检查时间间隔
    suspicious = []
    for addr in list(both_sides)[:50]:  # 先检查前50个
        sent = df[df["from"].str.lower() == addr][["timeStamp", "value_token"]].copy()
        sent["type"] = "sell"
        recv = df[df["to"].str.lower() == addr][["timeStamp", "value_token"]].copy()
        recv["type"] = "buy"
        combined = pd.concat([sent, recv]).sort_values("timeStamp")

        # 检查是否在60分钟内有买卖切换
        for i in range(len(combined) - 1):
            t1 = combined.iloc[i]
            t2 = combined.iloc[i + 1]
            time_diff = (t2["timeStamp"] - t1["timeStamp"]).total_seconds() / 60
            if time_diff <= 60 and t1["type"] != t2["type"]:
                suspicious.append({
                    "address": addr,
                    "action1": t1["type"],
                    "time1": t1["timeStamp"],
                    "action2": t2["type"],
                    "time2": t2["timeStamp"],
                    "interval_min": round(time_diff, 2),
                    "volume1": round(t1["value_token"], 2),
                    "volume2": round(t2["value_token"], 2)
                })

    sus_df = pd.DataFrame(suspicious)
    if len(sus_df) > 0:
        print(f"发现{len(sus_df)}笔可疑的快速买卖切换")
        print(sus_df.head(10).to_string())
    else:
        print("未发现可疑的快速买卖切换")

    # === 检测2：关联地址之间的互相转账 ===
    print("\n=== 检测2：地址对之间的双向转账 ===")
    pair_counts = defaultdict(int)
    for _, row in df.iterrows():
        pair = tuple(sorted([row["from"].lower(), row["to"].lower()]))
        pair_counts[pair] += 1

    bidirectional = {k: v for k, v in pair_counts.items() if v >= 3}
    print(f"发现{len(bidirectional)}对地址之间有3笔以上双向转账")
    if bidirectional:
        top_pairs = sorted(bidirectional.items(), key=lambda x: x[1], reverse=True)[:5]
        for pair, count in top_pairs:
            print(f"  {pair[0][:10]}... <-> {pair[1][:10]}... : {count}笔")

    # 保存
    path = os.path.join(output_dir, "wash_trade_analysis.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    if len(sus_df) > 0:
        sus_path = os.path.join(output_dir, "wash_trade_suspicious.csv")
        sus_df.to_csv(sus_path, index=False, encoding="utf-8-sig")
        print(f"\n可疑交易已保存到：{sus_path}")
    print(f"原始数据已保存到：{path}")
