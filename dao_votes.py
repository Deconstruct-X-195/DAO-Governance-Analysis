import os
import time
import pandas as pd
import requests

url = "https://hub.snapshot.org/graphql"
output_dir = "******"
csv_input_path = os.path.join(output_dir, "uniswap_proposals.csv")

# 1. 健壮地读取已有的提案数据
try:
    # 优先使用本地中文最常用的 gb18030 编码读取
    proposals_df = pd.read_csv(csv_input_path, encoding="gb18030")
except UnicodeDecodeError:
    try:
        # 如果报错，自动切回 utf-8-sig 尝试
        proposals_df = pd.read_csv(csv_input_path, encoding="utf-8-sig")
    except Exception as e:
        # 如果还报错，强行忽略乱码字符读取
        proposals_df = pd.read_csv(csv_input_path, encoding="utf-8", errors="ignore")
        print("警告：读取提案文件时遇到特殊字符，已自动忽略脏字符。")

# 检查 id 列是否存在
if "id" not in proposals_df.columns:
    raise KeyError("在 csv 文件中未找到 'id' 列，请检查表头是否正确！")

# 只取前5个提案做测试，避免请求太多
proposal_ids = proposals_df["id"].head(5).tolist()


def get_votes(proposal_id):
    """拉取单个提案的所有投票者和票数"""
    query = f"""
    {{
      votes(
        where: {{ proposal: "{proposal_id}" }}
        first: 1000
        orderBy: "vp"
        orderDirection: desc
      ) {{
        voter
        vp
        choice
      }}
    }}
    """
    try:
        response = requests.post(url, json={"query": query}, timeout=15)
        response.raise_for_status()  # 如果状态码不是200则抛出异常
        data = response.json()

        # 防御性判断：确保返回的 json 里有完整的数据结构
        if "data" in data and data["data"] and "votes" in data["data"]:
            return data["data"]["votes"] or []
        else:
            print(f"提示：提案 {proposal_id[:12]}... 未返回有效的投票数据")
            return []
    except Exception as e:
        print(f"请求提案 {proposal_id[:12]}... 时发生网络或解析错误: {e}")
        return []


# 2. 循环拉取每个提案的投票数据
all_votes = []
for pid in proposal_ids:
    print(f"正在获取提案：{pid[:20]}...")
    votes = get_votes(pid)

    for v in votes:
        v["proposal_id"] = pid

    all_votes.extend(votes)
    time.sleep(0.5)  # 避免请求频率过快被接口封禁

# 3. 处理并保存数据
if all_votes:
    # 转成DataFrame
    votes_df = pd.DataFrame(all_votes)
    print(f"\n共获取 {len(votes_df)} 条投票记录")
    print(votes_df.head(10))

    # 保存结果（导出时统一使用 utf-8-sig，确保中英文字符在 Excel 中打开不乱码）
    csv_output_path = os.path.join(output_dir, "uniswap_votes.csv")
    votes_df.to_csv(csv_output_path, index=False, encoding="utf-8-sig")
    print(f"\n数据已成功保存到：{csv_output_path}")
else:
    print("\n未获取到任何有效投票数据，请检查网络或提案 ID 是否有效。")
