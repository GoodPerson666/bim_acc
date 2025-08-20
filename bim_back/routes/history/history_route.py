from flask import Blueprint, request, jsonify
from utils.connect_mysql import get_db_connection
# 创建蓝图

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['POST'])
def history():
    data = request.get_json()
    if not data or 'userID' not in data:
        return jsonify({'success': False, 'message': '缺少userID参数'}), 400

    user_id = data['userID']
    page = int(data.get('page', 1))  # 获取分页参数
    page_size = int(data.get('pageSize', 1))

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 查询总记录数
            count_sql = "SELECT COUNT(*) as total FROM history WHERE reviewer_user_id = %s"
            cursor.execute(count_sql, (user_id,))
            total = cursor.fetchone()['total']

            # 查询分页数据
            offset = (page - 1) * page_size
            sql = "SELECT * FROM history WHERE reviewer_user_id = %s LIMIT %s OFFSET %s"
            cursor.execute(sql, (user_id, page_size, offset))
            history = cursor.fetchall()

        if history:
            return jsonify({
                'success': True,
                'message': '查询成功',
                'history': history,
                'total': total  # 返回总记录数
            })
        else:
            return jsonify({'success': False, 'message': '未找到历史记录'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': '服务器错误'}), 500
    finally:
        if 'connection' in locals():
            connection.close()