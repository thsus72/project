class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://flask_user:password@localhost/flask_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT 설정
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_TOKEN_LOCATION = ['cookies']  # 쿠키에 JWT 저장
    JWT_ACCESS_COOKIE_PATH = '/'  # Access Token 쿠키 경로
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'  # Refresh Token 쿠키 경로
    JWT_COOKIE_SECURE = False  # HTTPS에서만 활성화 (테스트 환경에서는 False)
    JWT_COOKIE_CSRF_PROTECT = True  # CSRF 방어 활성화