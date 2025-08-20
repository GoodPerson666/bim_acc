
from flask import Blueprint, request, jsonify
from utils.connect_mysql import get_db_connection
# 创建蓝图

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名或密码不能为空'}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            user = cursor.fetchone()

        if user:
            # 模拟返回一个 token 和用户信息
            return jsonify({
                'success': True,
                'message': '登录成功',
                'token': 'your_generated_token_here',
                'user': {
                    'id': user.get('userid'),
                    'username': user.get('username'),
                    'role':user.get('role')
                }
            })
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': '服务器错误'}), 500
    finally:
        if 'connection' in locals():
            connection.close()