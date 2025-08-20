import os

from flask import Blueprint, request, jsonify, send_file

# 创建蓝图

download_bp = Blueprint('download_bp', __name__)


@download_bp.route('/review-result/result',methods=['GET'])
def download_existing_file():
    # 文件路径
    file_path = os.path.join(download_bp.root_path, '../../results/review_result.txt')

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return "文件不存在", 404

    # 返回文件
    return send_file(
        file_path,
        as_attachment=True,
        download_name='report.txt',
        mimetype='text/plain'
    )