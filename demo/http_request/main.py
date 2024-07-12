import requests
import json


url = "http://test.com"
headers = {"Content-Type": "application/json"}  # 设置请求头为JSON
response = requests.post(url, headers=headers, data=json.dumps({
    "test": "test",
}))
print(response.content)