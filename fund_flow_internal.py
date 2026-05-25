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

def get_internal_transactions(address, label):
    """拉取内部合约调用记录"""
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid": "1",
        "module": "account",
        "action": "txlistinternal",
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
            print(f"{label}: 获取到 {len(df)} 条内部调用记录")
            return df
        else:
            print(f"{label}: 无数据 - {data.get('message')}")
            return pd.DataFrame()
    except Exception as e:
        print(f"{label}: 请求异常 - {e}")
        return pd.DataFrame()

all_dfs = []
for label, address in addresses.items():
    df = get_internal_transactions(address, label)
    if not df.empty:
        all_dfs.append(df)
    time.sleep(0.3)

if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)
    combined["timeStamp"] = pd.to_datetime(
        combined["timeStamp"].astype(int), unit="s"
    )
    combined["eth_value"] = combined["value"].astype(float) / 1e18

    # 检查四地址之间的内部调用
    address_list = [a.lower() for a in addresses.values()]
    internal = combined[
        combined["from"].str.lower().isin(address_list) &
        combined["to"].str.lower().isin(address_list)
    ]

    print(f"\n共获取 {len(combined)} 条内部调用记录")

    if len(internal) > 0:
        print(f"\n发现 {len(internal)} 笔四地址间的内部调用：")
        print(internal[["timeStamp", "from", "to", "eth_value"]].to_string())
    else:
        print("\n四个地址之间未发现内部合约调用")

    path = os.path.join(output_dir, "fund_flow_internal.csv")
    combined.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"\n数据已保存到：{path}")
else:
    print("所有地址均未获取到内部调用数据")