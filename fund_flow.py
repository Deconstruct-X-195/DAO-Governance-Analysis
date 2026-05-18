import requests
import pandas as pd
import os
import time

API_KEY = "113RPPW4YE9DK9G916FXMEBF1CN55ZE354"
output_dir = "E:\\PYTHON练习册\\dao_research"

# EnHeng提到的四个地址
addresses = {
    "Gate_Deposit": "0x6455327F820eDD69c4Cd665b995E0fEC679d7F9E",
    "Split_1": "0xec01c918E2f700F47332Ddc2d216Ae9E747Bd1a5",
    "Split_2": "0x1E034344f7Ac9F1f5DFaE55E53f5D597C13F76bc",
    "Aster_Related": "0x128463A60784c4D3f46c23Af3f65Ed859Ba87974"
}

def get_transactions(address, label):
    """拉取一个地址最近100笔ERC20代币转账记录"""
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": "1",
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 1000,
        "sort": "desc",
        "apikey": API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()

        if data["status"] == "1":
            df = pd.DataFrame(data["result"])
            df["address_label"] = label
            df["address"] = address
            print(f"{label}: 获取到 {len(df)} 条记录")
            return df
        else:
            print(f"{label}: 无数据或请求失败 - {data.get('message')} - {data.get('result')}")
            return pd.DataFrame()
    except Exception as e:
        print(f"{label}: 请求异常 - {e}")
        return pd.DataFrame()

# 拉取所有地址的交易记录
all_dfs = []
for label, address in addresses.items():
    df = get_transactions(address, label)
    if not df.empty:
        all_dfs.append(df)
    time.sleep(0.3)

if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)

    # 只保留关键列
    cols = ["address_label", "address", "tokenSymbol",
            "from", "to", "value", "timeStamp"]
    combined = combined[cols]

    # 时间戳转换
    combined["timeStamp"] = pd.to_datetime(
        combined["timeStamp"].astype(int), unit="s"
    )

    # 保存
    path = os.path.join(output_dir, "fund_flow_raw.csv")
    combined.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"\n共获取 {len(combined)} 条记录，已保存到：{path}")
    print(combined.head(10))
else:
    print("所有地址均未获取到数据")