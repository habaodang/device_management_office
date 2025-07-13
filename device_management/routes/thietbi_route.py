from flask import Blueprint,request,redirect,render_template,url_for,flash,session
from device_management import config
import math
import device_management.controller.Thietbi_service as thietbi_service
from flask_login import login_required

thietbi_route=Blueprint('thietbi_route', __name__)

#trang chinh sau khi login thanh cong
@thietbi_route.route('/danh-sach-thiet-bi', methods=['POST', 'GET'])
@login_required
def main_information_page():
    thietbi=thietbi_service.Thietbi_service()

    #xu ly phan trang
    page = int(request.args.get('page', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    paginate = int(request.args.get('paginate', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    page_size = config.page_size  # Số lượng thiết bị trên mỗi trang
    pages=thietbi.count_data_size()
    total_pages = math.ceil(pages / page_size)

    if request.method == 'POST':
        kw = request.form['kw']
        devices = thietbi.search_device(kw)  # Tìm kiếm thiết bị theo từ khóa
    else:
        devices = thietbi.get_device_page(page)  # Lấy danh sách thiết bị theo trang hiện tại

    return render_template('device_information/main_information_page.html', devices=devices, paginate=paginate,total_pages=total_pages,page=page)

#trang thong tin chi tiet
@thietbi_route.route('/information')
@login_required
def device_information():
    if 'Read' not in session['permission']:
        return redirect(url_for('thietbi_route.main_information_page'))
    thietbi=thietbi_service.Thietbi_service()

    stt = request.args.get('stt')
    device = thietbi.get_device_by_stt(stt)

    return render_template('device_information/device_information.html',device=device)

@thietbi_route.route('/add_devices')
@login_required
def add_devices():
    if 'Write' not in session['permission']:
        return redirect(url_for('thietbi_route.main_information_page'))
    return render_template('device_information/add_devices.html')

@thietbi_route.route('/add_device/data', methods=['GET', 'POST'])
@login_required
def procc_add_device():
    if request.method == 'POST':

        thietbi=thietbi_service.Thietbi_service()

        # Lấy dữ liệu từ form và gọi hàm thêm thiết bị
        thietbi.create(
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

        return redirect(url_for('thietbi_route.main_information_page'))
    return redirect(url_for('thietbi_route.add_devices'))

@thietbi_route.route('/delete_devices')
@login_required
def delete_device():
    if 'Delete' not in session['permission']:
        return redirect(url_for('thietbi_route.main_information_page'))
    device_id = request.args.get('stt')  # Lấy các thiết bị được chọn từ form

    if device_id:
        thietbi = thietbi_service.Thietbi_service()
        thietbi.delete(device_id)

    return redirect(url_for('thietbi_route.main_information_page'))

@thietbi_route.route('/update_info', methods=['GET', 'POST'])
@login_required
def update_infor():
    if 'Update' not in session['permission']:
        return redirect(url_for('thietbi_route.main_information_page'))
    thietbi = thietbi_service.Thietbi_service()
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        form_data=request.form
        stt = form_data['stt']
        device = thietbi.get_device_by_stt(stt)

        thietbi.update_device_info(form_data)

        # Thông báo cập nhật thành công
        flash('Cập nhật thông tin thiết bị thành công!', 'success')


    else:
        stt = request.args.get('stt')
    device = thietbi.get_device_by_stt(stt)
    return render_template('device_information/update_infor.html',device=device)
