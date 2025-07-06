from flask import Flask
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Abcd1234@localhost/thietbivien?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'mysecretkey12345'

    # Khởi tạo SQLAlchemy
    db.init_app(app)
    # Đăng ký Blueprint
    from device_management.routes import register_routes


    register_routes(app)
    # Tạo bảng (chỉ khi chạy lần đầu)
    with app.app_context():
        try:
            db.create_all()
            print("Tạo bảng thành công!")
        except Exception as e:
            print(f"Error: {e}")

    return app