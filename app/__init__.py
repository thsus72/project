from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager  # JWT 추가

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 초기화
    db.init_app(app)

    # JWT 초기화
    jwt = JWTManager(app)

    # 라우트 등록
    from .routes import main
    app.register_blueprint(main)

    return app
