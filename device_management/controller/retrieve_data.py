from device_management.config import page_size
from device_management.models import ThietBi,BaoTri
from device_management import db
from sqlalchemy import or_



def get_device():
    return ThietBi.query.all()

def get_device_page(page):
    start = (page - 1) * page_size
    end = start + page_size
    return ThietBi.query.slice(start, end).all()

def get_device_by_stt(stt):
    return ThietBi.query.filter(ThietBi.stt==stt).first()

def add_baptri(stt,ngay_thang,hien_tuong,cach_sua,chuyen_vien,ghi_chu):

    baotri=BaoTri(ngay_thang=ngay_thang,hien_tuong_hu_hong=hien_tuong,cach_sua_chua=cach_sua,chuyen_vien_sua_chua=chuyen_vien,ghi_chu=ghi_chu,thietbi_stt=stt)
    db.session.add(baotri)
    db.session.commit()

def get_bao_tri(stt):
    return BaoTri.query.filter(BaoTri.thietbi_stt==stt).all()


from sqlalchemy import or_

def search_device(keyword):
    # Tạo danh sách các thuộc tính cần tìm kiếm
    search_columns = [
        ThietBi.ten_thiet_bi,
        ThietBi.ma_tb,
        ThietBi.nam_sx,
        ThietBi.nsx,
        ThietBi.model,
        ThietBi.sl,
        ThietBi.nguyen_gia,
        ThietBi.gia_tri_con_lai,
        ThietBi.so_hieu,
        ThietBi.hang_sx,
        ThietBi.nguon_cap,
        ThietBi.ghi_chu,
        ThietBi.khoa,
        ThietBi.ngay_lap_cho_khoa,
        ThietBi.ngay_chuyen_khoa_khac
    ]



    # Tìm kiếm theo keyword trong các cột trên
    results = ThietBi.query.filter(
        or_(*[column.ilike(f"%{keyword}%") for column in search_columns])
    ).all()

    return results


# Hàm thêm thiết bị vào cơ sở dữ liệu
def add_device_to_db(ten_thiet_bi, ma_tb, nam_sx, nsx, model, sl, nguyen_gia,
                     gia_tri_con_lai, so_hieu, hang_sx, nguon_cap, ghi_chu, khoa,
                     ngay_lap_cho_khoa, ngay_chuyen_khoa_khac):
    # Tạo đối tượng thiết bị mới
    new_device = ThietBi(
        ten_thiet_bi=ten_thiet_bi,
        ma_tb=ma_tb,
        nam_sx=nam_sx,
        nsx=nsx,
        model=model,
        sl=sl,
        nguyen_gia=nguyen_gia,
        gia_tri_con_lai=gia_tri_con_lai,
        so_hieu=so_hieu,
        hang_sx=hang_sx,
        nguon_cap=nguon_cap,
        ghi_chu=ghi_chu,
        khoa=khoa,
        ngay_lap_cho_khoa=ngay_lap_cho_khoa,
        ngay_chuyen_khoa_khac=ngay_chuyen_khoa_khac
    )

    # Thêm thiết bị vào cơ sở dữ liệu
    db.session.add(new_device)
    db.session.commit()

def add_bao_tri_to_db(ngay_thang, hien_tuong_hu_hong, cach_sua_chua,
                       chuyen_vien_sua_chua, ghi_chu, thietbi_stt):
    # Tạo đối tượng BaoTri mới
    new_baotri = BaoTri(
        ngay_thang=ngay_thang,
        hien_tuong_hu_hong=hien_tuong_hu_hong,
        cach_sua_chua=cach_sua_chua,
        chuyen_vien_sua_chua=chuyen_vien_sua_chua,
        ghi_chu=ghi_chu,
        thietbi_stt=thietbi_stt
    )

    # Thêm bảo trì vào cơ sở dữ liệu
    db.session.add(new_baotri)
    db.session.commit()

def count_data_size():
    return ThietBi.query.count()

# Hàm cập nhật thông tin thiết bị
def update_device_info(form_data):
    thietbị=ThietBi.query.filter(ThietBi.stt==form_data['stt']).first()
    thietbị.ten_thiet_bi = form_data['ten_thiet_bi']
    thietbị.ma_tb = form_data['ma_tb']
    thietbị.model = form_data['model']
    thietbị.so_hieu = form_data['so_hieu']
    thietbị.nsx = form_data['nuoc_san_xuat']
    thietbị.nam_sx = form_data['nam_sx']
    thietbị.nguyen_gia = form_data['nguyen_gia']
    thietbị.hang_sx = form_data['hang_sx']
    thietbị.khoa = form_data['khoa']
    thietbị.nguon_cap = form_data['nguon_cap']
    thietbị.sl = form_data['sl']
    thietbị.ngay_lap_cho_khoa = form_data['ngay_lap_cho_khoa']
    thietbị.ghi_chu = form_data['ghi_chu']

    # Cập nhật vào cơ sở dữ liệu
    db.session.commit()

def delete_device(stt):
    thietbị = ThietBi.query.filter(ThietBi.stt == stt).first()
    # Xóa thiết bị khỏi cơ sở dữ liệu
    try:
        db.session.delete(thietbị)
        db.session.commit()
        return 'Đã xóa thiết bị thành công'
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return 'Xóa thiết bị thất bại'

def set_status_maintenance(stt):
    thietbị = ThietBi.query.filter(ThietBi.stt == stt).first()
    if thietbị.maintenance_status:
        thietbị.maintenance_status=False
    else:
        thietbị.maintenance_status=True
    db.session.commit()

def get_device_status_maintenance():
    return ThietBi.query.filter(ThietBi.maintenance_status == True).all()