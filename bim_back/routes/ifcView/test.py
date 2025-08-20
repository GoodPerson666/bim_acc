import json
import sqlite3

list = []
guid_list = []

# 连接到数据库
conn = sqlite3.connect(r'D:\毕设代码\bim_back\instance\data.db')
cursor = conn.execute("select * from 报告_自然语言生成与合规性审查合并视图 where 判断结果 = '不适用' limit 10,20 ")
rows = cursor.fetchall()

for row in rows:
    # print(row[0])
    list.append(row[4])
    # list_json = json.load(rows[4])
    # print(row[4])
conn.close()

for item in list:
    list_json = json.loads(item)
    guid_list.append(list_json[1]['guid'])
    # print(type(list_json[1]['guid']))
print(guid_list)