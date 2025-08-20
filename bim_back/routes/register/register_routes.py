import logging

from flask import Blueprint, request, jsonify

from utils.connect_mysql import get_db_connection

# 创建日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建蓝图
register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    try:
        # 获取请求数据
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = "user"  # 默认角色为用户

        # 验证请求数据
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400

        # 验证用户名格式
        if not isinstance(username, str) or len(username) < 3 or len(username) > 20:
            return jsonify({'success': False, 'message': '用户名长度应在3-20个字符之间'}), 400

        # 验证密码强度
        if len(password) < 3:
            return jsonify({'success': False, 'message': '密码长度至少为3个字符'}), 400


        # 数据库操作
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查用户名是否已存在
                sql = "SELECT * FROM user WHERE username = %s"
                cursor.execute(sql, (username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    return jsonify({'success': False, 'message': '用户名已存在'}), 400

                # 插入新用户
                sql = "INSERT INTO user (username, password, role) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, password, role))
                connection.commit()

            return jsonify({
                'success': True,
                'message': '注册成功',
                'data': {
                    'username': username,
                    'role': role
                }
            })

        except Exception as db_error:
            connection.rollback()
            logger.error(f"Database error: {db_error}")
            return jsonify({'success': False, 'message': '数据库操作失败'}), 500
        finally:
            connection.close()

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': '服务器错误'}), 500