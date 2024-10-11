from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager
from redis import Redis

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Cấu hình app
    app.config.from_object(Config)  # Thay đổi thành ProductionConfig khi deploy

    # Khởi tạo DB và Migrate
    db.init_app(app)
    migrate.init_app(app, db)  # Khởi tạo migrate với app và db
    jwt.init_app(app)
    redis_client = Redis.from_url(app.config["REDIS_URL"])

    # Gán redis_client vào ứng dụng Flask để có thể truy cập từ bất kỳ đâu
    app.redis_client = redis_client
    # Import các mô-đun models tại đây
    from .models import Thread, User, Comment

    # Đăng ký các Blueprint
    from app.routes.user_route import user_bp
    from app.routes.auth_route import auth_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    return app
