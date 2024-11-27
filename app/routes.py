from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
import bcrypt
from .models import User
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies

main = Blueprint('main', __name__)

# 메인 페이지
@main.route('/main')
@jwt_required()  # JWT 인증이 필요한 엔드포인트
def index():
    user_id = get_jwt_identity()  # JWT에서 사용자 ID 추출
    if user_id:
        user = User.query.get(user_id)
        if user:
            return render_template('index.html', username=user.username)
    flash("로그인이 필요합니다.", "danger")
    return redirect(url_for('main.login'))

# 첫 화면
@main.route('/')
def home():
    return render_template('home.html')

# 회원가입 라우트
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        email = request.form.get('email')

        if not username or len(username) < 3:
            flash("아이디는 최소 3자 이상이어야 합니다.", "danger")
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash("이미 사용 중인 아이디입니다.", "danger")
            return render_template('register.html')
        if not password or len(password) < 8 or password != password_confirm:
            flash("비밀번호는 최소 8자 이상이어야 하며 확인이 일치해야 합니다.", "danger")
            return render_template('register.html')
        if not email or "@" not in email or User.query.filter_by(email=email).first():
            flash("올바른 이메일 형식을 입력하세요.", "danger")
            return render_template('register.html')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("회원가입이 완료되었습니다!", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html')

# 로그인 라우트
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("존재하지 않는 아이디입니다.", "danger")
            return render_template('login.html')

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            flash("비밀번호가 올바르지 않습니다.", "danger")
            return render_template('login.html')

        # JWT 생성
        access_token = create_access_token(identity=str(user.user_id))  # `identity`를 문자열로 전달
        response = make_response(redirect(url_for('main.index')))
        set_access_cookies(response, access_token)
        return response
        

    return render_template('login.html')

# 로그아웃 라우트
@main.route('/logout')
def logout():
    response = make_response(redirect(url_for('main.login')))
    unset_jwt_cookies(response)
    # Flash 메시지를 설정하지 않거나 불필요한 메시지를 추가하지 않음
    return response
