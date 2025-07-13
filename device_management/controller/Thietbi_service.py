from device_management.controller import Database
from device_management.models import ThietBi
from device_management.config import page_size
from device_management import db
from sqlalchemy import or_

class Thietbi_service(Database.DatabaseAccess):
    def __init__(self):
        super().__init__(ThietBi)

    @staticmethod
    def get_device_page(page):
        start = (page - 1) * page_size
        end = start + page_size
        return ThietBi.query.slice(start, end).all()

    def get_device_by_stt(self,stt):
        return super().get_by_field('stt',stt)

    @staticmethod
    def count_data_size():
        return ThietBi.query.count()

    @staticmethod
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
    @staticmethod

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

    def set_status_maintenance(self,stt):
        thietbị = super().get_by_field('stt',stt)
        if thietbị.maintenance_status:
            thietbị.maintenance_status=False
        else:
            thietbị.maintenance_status=True
        db.session.commit()

    def get_device_status_maintenance(self):
        return super().get_by_field_all('maintenance_status',True)