from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.routes.user_route import user_bp

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Cấu hình app
    app.config.from_object(Config)  # Thay đổi thành ProductionConfig khi deploy

    # Khởi tạo DB và Migrate
    db.init_app(app)
    migrate.init_app(app, db)  # Khởi tạo migrate với app và db

    # Import các mô-đun models tại đây
    from .models import Thread, User, Comment

    # Đăng ký các Blueprint
    app.register_blueprint(user_bp)

    return app
