from flask import Flask
from flask_cors import CORS  # 解决跨域问题

# 导入 Blueprint
from routes.download.download_routes import download_bp
from routes.ifcView.Rule_route import getRules_bp
from routes.upload.review_routes import review_bp
from routes.login.login_routes import login_bp
from routes.register.register_routes import register_bp
from routes.history.history_route import history_bp

from routes.ifcView.Compliance_route import compliance_bp
from routes.ifcView.NonCompliance_route import Noncompliance_bp
from routes.ifcView.Normal_route import normal_bp

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 注册 Blueprint
app.register_blueprint(review_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(history_bp)
app.register_blueprint(download_bp)

#审查结果
app.register_blueprint(normal_bp)
app.register_blueprint(compliance_bp)
app.register_blueprint(Noncompliance_bp)

app.register_blueprint(getRules_bp)


if __name__ == '__main__':
    # 运行 Flask 应用
    app.run(debug=True)