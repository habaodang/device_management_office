from flask import render_template, Blueprint, request, redirect, url_for,flash,session
from flask_login import login_user,logout_user
import device_management.controller.login as controll_login
from  device_management import login_manager
from device_management.controller import user_service

main=Blueprint('main',__name__)
login_manager.login_view = 'main.login'

# Trang login
@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        check,user=controll_login.check_login(username,password)
        # Kiểm tra thông tin đăng nhập (thực tế sẽ so sánh với CSDL)

        if check:
            userclass=user_service.UserClass()
            session['permission']=userclass.check_permission(user.role.stt)
            if 'admin' in session['permission']:
                login_user(user)
                return redirect(url_for('admin_route.admin_management'))
            else:
                login_user(user)
                return redirect(url_for('thietbi_route.main_information_page'))
        else:
            session.pop('_flashes', None)
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'danger')
    return render_template('login.html')

@main.route('/dang-xuat')
def logout():
    session.pop('permission', None)
    logout_user()
    return redirect(url_for('main.login'))



# # Route để tạo mã QR
# @main.route('/generate_qr')
# def generate_qr():
#     stt = request.args.get('stt')
#     device = ret.get_device_by_stt(stt)
#     # URL của trang mà QR sẽ dẫn tới
#     url = f"http://localhost:5000/form_repair?stt={stt}"  # Thay bằng URL thực tế của trang form repair
#
#     # Tạo mã QR
#     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
#     qr.add_data(url)
#     qr.make(fit=True)
#
#     # Lưu mã QR vào bộ nhớ
#     img = qr.make_image(fill='black', back_color='white')
#
#     # Lưu hình ảnh QR vào bộ nhớ
#     img_io = BytesIO()
#     img.save(img_io, 'PNG')
#     img_io.seek(0)
#
#     # Trả về mã QR dưới dạng hình ảnh
#     return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=f"{device.ten_thiet_bi}_{device.model}.png")
