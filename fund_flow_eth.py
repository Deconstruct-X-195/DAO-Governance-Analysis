import requests
import pandas as pd
import os
import time

API_KEY = "113RPPW4YE9DK9G916FXMEBF1CN55ZE354"
output_dir = "E:\\PYTHON练习册\\dao_research"

addresses = {
    "Gate_Deposit": "0x6455327F820eDD69c4Cd665b995E0fEC679d7F9E",
    "Split_1": "0xec01c918E2f700F47332Ddc2d216Ae9E747Bd1a5",
    "Split_2": "0x1E034344f7Ac9F1f5DFaE55E53f5D597C13F76bc",
    "Aster_Related": "0x128463A60784c4D3f46c23Af3f65Ed859Ba87974"
}

def get_eth_transactions(address, label):
    """拉取ETH原生转账记录"""
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": "1",
        "module": "account",
        "action": "txlist",
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
            print(f"{label}: 获取到 {len(df)} 条ETH交易记录")
            return df
        else:
            print(f"{label}: 无数据 - {data.get('message')}")
            return pd.DataFrame()
    except Exception as e:
        print(f"{label}: 请求异常 - {e}")
        return pd.DataFrame()

# 拉取所有地址
all_dfs = []
for label, address in addresses.items():
    df = get_eth_transactions(address, label)
    if not df.empty:
        all_dfs.append(df)
    time.sleep(0.3)

if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)

    # 保留关键列
    cols = ["address_label", "address", "from", "to", "value", "timeStamp", "isError"]
    combined = combined[[c for c in cols if c in combined.columns]]

    # 转换时间戳
    combined["timeStamp"] = pd.to_datetime(
        combined["timeStamp"].astype(int), unit="s"
    )

    # ETH金额转换（原始单位是wei，1 ETH = 10^18 wei）
    combined["eth_value"] = combined["value"].astype(float) / 1e18

    # 过滤掉失败的交易
    if "isError" in combined.columns:
        combined = combined[combined["isError"] == "0"]

    # 检查四个地址之间的直接转账
    address_list = [a.lower() for a in addresses.values()]
    internal = combined[
        combined["from"].str.lower().isin(address_list) &
        combined["to"].str.lower().isin(address_list)
    ]

    print(f"\n共获取 {len(combined)} 条ETH交易记录")

    if len(internal) > 0:
        print(f"\n发现 {len(internal)} 笔四地址间的直接ETH转账：")
        print(internal[["timeStamp", "from", "to", "eth_value"]].to_string())
    else:
        print("\n四个地址之间未发现直接ETH转账")

    # 保存
    path = os.path.join(output_dir, "fund_flow_eth.csv")
    combined.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"\n数据已保存到：{path}")