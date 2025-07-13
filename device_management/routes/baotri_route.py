from io import BytesIO
import pandas as pd
from flask import Blueprint,request,redirect,render_template,url_for,session,send_file
import device_management.config as config
import device_management.controller.Thietbi_service as thietbi_service
import device_management.controller.baotri_service as baotri_service
import math
from datetime import datetime
from flask_login import login_required


baotri_route = Blueprint('baotri_route',__name__)

@baotri_route.route('/repair',methods=['POST','GET'])
@login_required
def repair():
    thietbi = thietbi_service.Thietbi_service()
    page = int(request.args.get('page', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    paginate = int(request.args.get('paginate', 1))  # Lấy số trang từ URL hoặc mặc định là 1
    page_size = config.page_size  # Số lượng thiết bị trên mỗi trang
    pages = thietbi.count_data_size()
    total_pages = math.ceil(pages / page_size)

    if request.method == 'POST':
        kw = request.form['kw']
        devices = thietbi.search_device(kw)  # Tìm kiếm thiết bị theo từ khóa
    else:
        devices = thietbi.get_device_page(page)  # Lấy danh sách thiết bị theo trang hiện tại

    return render_template('repair/repair.html', devices=devices, paginate=paginate,total_pages=total_pages,page=page)

@baotri_route.route('/form_repair/<stt>')
@login_required
def form_repair(stt):
    if 'Read' not in session['permission']:
        return redirect(url_for('baotri_route.repair'))
    baotri=baotri_service.baotri_service()
    thietbi=thietbi_service.Thietbi_service()
    if not stt:
        stt = request.args.get('stt')

    device = thietbi.get_device_by_stt(stt)
    repairs = baotri.get_device_by_stt_all(stt)

    return render_template('repair/form_repair.html', device=device, repairs=repairs)

@baotri_route.route('/add_bao_tri', methods=['GET', 'POST'])
@login_required
def add_bao_tri():
    if 'Write' not in session['permission']:
        return redirect(url_for('baotri_route.repair'))
    if request.method == 'POST':
        baotri = baotri_service.baotri_service()
        # Lấy dữ liệu từ form
        ngay_thang = datetime.strptime(request.form['ngay_thang'], '%Y-%m-%d')
        hien_tuong_hu_hong = request.form['hien_tuong_hu_hong']
        cach_sua_chua = request.form['cach_sua_chua']
        chuyen_vien_sua_chua = request.form['chuyen_vien_sua_chua']
        ghi_chu = request.form['ghi_chu']
        thietbi_stt = request.form['stt']

        # Gọi hàm thêm bảo trì vào cơ sở dữ liệu
        baotri.create(
            ngay_thang=ngay_thang,
            hien_tuong_hu_hong=hien_tuong_hu_hong,
            cach_sua_chua=cach_sua_chua,
            chuyen_vien_sua_chua=chuyen_vien_sua_chua,
            ghi_chu=ghi_chu,
            thietbi_stt=int(thietbi_stt)
        )

        return redirect(url_for('baotri_route.form_repair',stt=thietbi_stt))  # Chuyển hướng lại trang thêm bảo trì

    return redirect(url_for('baotri_route.form_repair'))  # Hiển thị form thêm bảo trì

@baotri_route.route('/export_excel', methods=['GET'])
@login_required
def export_excel():
    baotri = baotri_service.baotri_service()
    thietbi = thietbi_service.Thietbi_service()

    stt = request.args.get('stt')
    device = thietbi.get_device_by_stt(stt)
    bao_tri=baotri.get_device_by_stt_all(stt)
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
