import requests
import json

url = "https://chat.cqjtu.edu.cn/ds/api/v1/chat/completions"
file_path = r'C:\Users\16021\Desktop\毕设\文件\result.json'
# 从文件中读取内容
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

path = r'C:\Users\16021\Desktop\毕设\规范\规范3.txt'
with open(path, 'r', encoding='utf-8') as standard:
    standard_content = standard.read()

query = f'''
    你是一位专精于建筑法规合规性评估的建筑法规专家，擅长分析建筑描述与规范要求的合规性。
    请根据给定的BIM待审查文件{file_content}和规范条文{standard_content}，判断待审查文件中的信息是否符合条文要求。
    要求：
    1.逐个判断待审查文件中的每条属性信息
    2.请仅返回csv格式，具体包含：审查属性,规范条目,是否合规
    '''
payload = json.dumps({
  "messages": [
    {
      "content": query,
      "role": "user"
    }
  ],
  "model": "deepseek-reasoner",
  "frequency_penalty": 0,
  "max_tokens": 8192,
  "presence_penalty": 0,
  "response_format": {
    "type": "text"
  },
  "stop": None,
  "stream": False,
  "stream_options": None,
  "temperature": 0.5,
  "top_p": 1,
  "tools": None,
  "tool_choice": "none",
  "logprobs": False,
  "top_logprobs": None
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'sk-33ef4c8dd34cbc60e4f301e65044d7b5'
}

response = requests.request("POST", url, headers=headers, data=payload)
print("状态码:", response.status_code)  # 正常应为200
result = response.json()['choices'][0]['message']['content']
print(result)
