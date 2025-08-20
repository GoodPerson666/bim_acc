import json

from flask import Blueprint, request, jsonify
import sqlite3
Noncompliance_bp = Blueprint('Noncompliance', __name__)

@Noncompliance_bp.route('/ifcView/Noncompliance', methods=['POST'])

def Noncompliance():
    list = []
    guid_list = []

    # 连接到数据库
    conn = sqlite3.connect(r'D:\毕设代码\bim_back\instance\data.db')
    cursor = conn.execute("select * from 报告_自然语言生成与合规性审查合并视图 where 判断结果 = '不合规' limit 100 ")
    rows = cursor.fetchall()
    for row in rows:
        list.append(row[4])

    conn.close()

    for item in list:
        list_json = json.loads(item)
        guid_list.append(list_json[1]['guid'])
    return jsonify(guid_list)