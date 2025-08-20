import json
import sqlite3
from flask import Blueprint, request, jsonify

getRules_bp = Blueprint('getRules', __name__)

@getRules_bp.route('/ifcView/getRules', methods=['GET'])
def getRules():
    guid = request.args.get('guid')          # 从查询参数取
    if not guid:
        return jsonify({'success': False, 'message': '缺少 guid'}), 400

    try:
        conn = sqlite3.connect(r'D:\毕设代码\bim_back\instance\data.db')
        sql = """
            SELECT 内容, 判断结果
            FROM 报告_自然语言生成与合规性审查合并视图
            WHERE IFC实体组 LIKE ?
        """
        rows = conn.execute(sql, (f'%{guid}%',)).fetchall()
        conn.close()

        data = [{'内容': r[0], '判断结果': r[1]} for r in rows]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500