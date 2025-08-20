from datetime import datetime
from flask import Blueprint, request, jsonify
import os
from utils.bim_parser import parse_bim_file
from utils.deepseek_631b import local_api_631b
from utils.deepseek_7b import local_api_7b
from utils.call_api import api
from utils.connect_mysql import get_db_connection

# 创建一个 Blueprint，用于处理文件上传和审查功能
review_bp = Blueprint('review', __name__)

# 配置文件上传目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), '../../results')  # 新增结果目录

# 确保上传目录和结果目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)


@review_bp.route('/review', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    # 获取 userID
    user_id = request.form.get('userID')  # 从 FormData 中获取 userID

    if not user_id:
        return jsonify({"error": "Missing userID in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 保存文件
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 解析 BIM 文件
        bim_data = parse_bim_file(file_path)
        print("开始审查")
        # 调用审查 API
        # review_result = local_api_7b(bim_data)
        review_result = api(bim_data)
        # review_result = local_api_631b(bim_data)


        # 将结果保存到数据库
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "insert into history (review_time,reviewer_user_id,review_content) values(%s,%s,%s)"
                cursor.execute(sql, (datetime.now(), user_id, review_result))
                connection.commit()  # 提交事务
        except Exception as e:
            print("数据库连接失败:", str(e))
        finally:
            if 'connection' in locals():
                connection.close()

        # 将审查结果写入文件
        result_filename = f"review_result.txt"
        result_filepath = os.path.join(RESULTS_FOLDER, result_filename)

        with open(result_filepath, 'w', encoding='utf-8') as f:
            f.write(f"审查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"用户ID: {user_id}\n")
            f.write(f"原始文件: {file.filename}\n")
            f.write("\n审查结果:\n")
            f.write(review_result)

        # 返回 JSON 响应
        return jsonify({
            "message": "文件上传和审查成功",
            "文件路径": file_path,
            "结果文件": result_filepath,
            "审查结果": review_result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500