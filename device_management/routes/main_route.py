import math
from datetime import datetime
from flask import render_template, Blueprint, request, redirect, url_for,flash,send_file
from device_management import db
import device_management.config as config
from device_management.models import ThietBi,BaoTri
import device_management.controller.retrieve_data as ret
from io import BytesIO
import pandas as pd
import qrcode

main=Blueprint('main',__name__)

# Trang login
@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kiểm tra thông tin đăng nhập (thực tế sẽ so sánh với CSDL)
        if username == 'admin' and password == config.password:
            return redirect(url_for('main.index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'danger')

    return render_template('login.html')

@main.route('/index', methods=['POST', 'GET'])
def index():
    page = int(request.args.get('page', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    paginate = int(request.args.get('paginate', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    page_size = config.page_size  # Số lượng thiết bị trên mỗi trang
    pages=ret.count_data_size()
    total_pages = math.ceil(pages / page_size)

    if request.method == 'POST':
        kw = request.form['kw']
        devices = ret.search_device(kw)  # Tìm kiếm thiết bị theo từ khóa
    else:
        devices = ret.get_device_page(page)  # Lấy danh sách thiết bị theo trang hiện tại

    return render_template('index.html', devices=devices, paginate=paginate,total_pages=total_pages,page=page)

@main.route('/information')
def device_information():
    stt = request.args.get('stt')
    device = ret.get_device_by_stt(stt)
    print('ok')
    return render_template('device_information.html',device=device)

@main.route('/repair',methods=['POST','GET'])
def repair():
    page = int(request.args.get('page', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    paginate = int(request.args.get('paginate', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    page_size = config.page_size  # Số lượng thiết bị trên mỗi trang
    pages = ret.count_data_size()
    total_pages = math.ceil(pages / page_size)

    if request.method == 'POST':
        kw = request.form['kw']
        devices = ret.search_device(kw)  # Tìm kiếm thiết bị theo từ khóa
    else:
        devices = ret.get_device_page(page)  # Lấy danh sách thiết bị theo trang hiện tại

    return render_template('repair.html', devices=devices, paginate=paginate,total_pages=total_pages,page=page)


@main.route('/form_repair/<stt>')
def form_repair(stt):

    if not stt:
        stt = request.args.get('stt')

    device = ret.get_device_by_stt(stt)
    repairs = BaoTri.query.filter_by(thietbi_stt=stt).all()
    return render_template('form_repair.html', device=device, repairs=repairs)

@main.route('/add_devices')
def add_devices():
    return render_template('add_devices.html')


@main.route('/add_device/data', methods=['GET', 'POST'])
def procc_add_device():
    if request.method == 'POST':
        # Lấy dữ liệu từ form và gọi hàm thêm thiết bị
        ret.add_device_to_db(
            ten_thiet_bi=request.form['ten_thiet_bi'],
            ma_tb=request.form['ma_tb'],
            nam_sx=request.form['nam_sx'],
            nsx=request.form['nsx'],
            model=request.form['model'],
            sl=request.form['sl'],
            nguyen_gia=request.form['nguyen_gia'],
            gia_tri_con_lai=request.form['gia_tri_con_lai'],
            so_hieu=request.form['so_hieu'],
            hang_sx=request.form['hang_sx'],
            nguon_cap=request.form['nguon_cap'],
            ghi_chu=request.form['ghi_chu'],
            khoa=request.form['khoa'],
            ngay_lap_cho_khoa=request.form['ngay_lap_cho_khoa'],
            ngay_chuyen_khoa_khac=request.form['ngay_chuyen_khoa_khac']
        )

        return redirect(url_for('main.index'))
    return redirect(url_for('main.add_devices'))

@main.route('/add_bao_tri', methods=['GET', 'POST'])
def add_bao_tri():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ngay_thang = datetime.strptime(request.form['ngay_thang'], '%Y-%m-%d')
        hien_tuong_hu_hong = request.form['hien_tuong_hu_hong']
        cach_sua_chua = request.form['cach_sua_chua']
        chuyen_vien_sua_chua = request.form['chuyen_vien_sua_chua']
        ghi_chu = request.form['ghi_chu']
        thietbi_stt = request.form['stt']

        # Gọi hàm thêm bảo trì vào cơ sở dữ liệu
        ret.add_bao_tri_to_db(
            ngay_thang=ngay_thang,
            hien_tuong_hu_hong=hien_tuong_hu_hong,
            cach_sua_chua=cach_sua_chua,
            chuyen_vien_sua_chua=chuyen_vien_sua_chua,
            ghi_chu=ghi_chu,
            thietbi_stt=int(thietbi_stt)
        )

        return redirect(url_for('main.form_repair',stt=thietbi_stt))  # Chuyển hướng lại trang thêm bảo trì

    return redirect(url_for('main.form_repair'))  # Hiển thị form thêm bảo trì

@main.route('/delete_devices', methods=['POST'])
def delete_devices():
    device_ids = request.form.getlist('device_ids')  # Lấy các thiết bị được chọn từ form

    if not device_ids:
        flash('Không có thiết bị nào được chọn để xóa.', 'warning')
        return redirect(url_for('main.index'))

    try:
        # Xóa các thiết bị được chọn khỏi cơ sở dữ liệu
        ThietBi.query.filter(ThietBi.stt.in_(device_ids)).delete(synchronize_session=False)
        db.session.commit()
        flash('Các thiết bị đã được xóa thành công.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra: {str(e)}', 'danger')

    return redirect(url_for('main.index'))

@main.route('/update_info', methods=['GET', 'POST'])
def update_infor():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        form_data = request.form
        stt = form_data['stt']
        device = ret.get_device_by_stt(stt)
        # Gọi hàm cập nhật thông tin thiết bị
        ret.update_device_info(form_data)

        # Thông báo cập nhật thành công
        flash('Cập nhật thông tin thiết bị thành công!', 'success')


    else:
        stt = request.args.get('stt')
    device = ret.get_device_by_stt(stt)
    return render_template('update_infor.html',device=device)

@main.route('/delete-device')
def delete_device():
    device_id = request.args.get('stt')

    ret.delete_device(device_id)

    return redirect(url_for('main.index'))

@main.route('/maintenance')
def maintenance():
    devices=ret.get_device_status_maintenance()
    return render_template('maintenance.html',devices=devices)

@main.route('/status-maintenance')
def status_maintenance():
    stt=request.args.get('stt')
    device = ret.set_status_maintenance(stt)
    return redirect(url_for('main.form_repair',stt=stt))


@main.route('/export_excel', methods=['GET'])
def export_excel():
    stt = request.args.get('stt')
    device = ret.get_device_by_stt(stt)
    bao_tri=ret.get_bao_tri(stt)
    # Giả sử bạn đã có bảng dữ liệu từ cơ sở dữ liệu
    maintenance_data = []
    for record in bao_tri:
        maintenance_data.append({
            'Ngày tháng': record.ngay_thang.strftime('%Y-%m-%d'),  # Định dạng lại ngày tháng
            'Hiện tượng hư hỏng': record.hien_tuong_hu_hong,
            'Cách sửa chữa': record.cach_sua_chua,
            'Chuyên viên sửa chữa': record.chuyen_vien_sua_chua,
            'Ghi chú': record.ghi_chu
        })
    print(device)
    name= device.ten_thiet_bi
    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(maintenance_data)

    # Tạo file Excel từ DataFrame
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')

    # Lưu file và trả về cho người dùng
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name=f'{name}.xlsx')

# Route để tạo mã QR
@main.route('/generate_qr')
def generate_qr():
    stt = request.args.get('stt')
    device = ret.get_device_by_stt(stt)
    # URL của trang mà QR sẽ dẫn tới
    url = f"http://localhost:5000/form_repair?stt={stt}"  # Thay bằng URL thực tế của trang form repair

    # Tạo mã QR
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    # Lưu mã QR vào bộ nhớ
    img = qr.make_image(fill='black', back_color='white')

    # Lưu hình ảnh QR vào bộ nhớ
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Trả về mã QR dưới dạng hình ảnh
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=f"{device.ten_thiet_bi}_{device.model}.png")