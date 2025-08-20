import json

from flask import Blueprint, request, jsonify
import sqlite3
compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/ifcView/compliance', methods=['POST'])

def compliance():
    list = []
    guid_list = []

    # 连接到数据库
    conn = sqlite3.connect(r'D:\毕设代码\bim_back\instance\data.db')
    cursor = conn.execute("select * from 报告_自然语言生成与合规性审查合并视图 where 判断结果 = '合规' limit 100 ")
    rows = cursor.fetchall()
    for row in rows:
        list.append(row[4])

    conn.close()

    for item in list:
        list_json = json.loads(item)
        guid_list.append(list_json[1]['guid'])
    return jsonify(guid_list)