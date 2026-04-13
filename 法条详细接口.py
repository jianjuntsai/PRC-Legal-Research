import requests
from config import API_KEY

url = "https://apiplatform.legalmind.cn/open/rh_ft_detail"
headers = {
    "accept": "application/json;charset=UTF-8",
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY
}

# 请求参数：可使用 id，或 fgmc + ftnum 组合
payload = {
    "fgmc": "中华人民共和国民法典",
    "ftnum": "第二百零一条"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

if result.get("status") == "success":
    data = result["data"]
    print(f"法条名称：{data['ftmc']}")
    print(f"法规名称：{data['fgmc']}")
    print(f"时效性：{data['sxx']}")
    print(f"发布日期：{data['fbrq']}")
    print(f"实施日期：{data['ssrq']}")
    print(f"\n内容：\n{data['content']}")
else:
    print(f"请求失败：{result.get('message')}")
