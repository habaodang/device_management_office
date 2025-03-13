from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean,Enum
from sqlalchemy.orm import relationship
from device_management import db

# Mô hình bảng ThietBi
class ThietBi(db.Model):
    __tablename__ = 'thiet_bi'

    stt = Column(Integer, primary_key=True)  # Kiểu Integer cho cột stt
    ten_thiet_bi = Column( String(255), nullable=False)
    ma_tb = Column(String(100))
    nam_sx = Column(String(50))
    nsx = Column( String(100))
    model = Column(String(500))
    sl = Column(String(50))
    nguyen_gia = Column(String(50))
    gia_tri_con_lai = Column(String(500))
    so_hieu = Column(String(500))
    hang_sx = Column(String(100))
    nguon_cap = Column(String(255))
    ghi_chu = Column( String(255))
    khoa = Column(String(100))
    ngay_lap_cho_khoa = Column(String(500))
    ngay_chuyen_khoa_khac = Column(String(500))
    maintenance_status = Column(Boolean, default=False)

    # Mối quan hệ với bảng BaoTri
    bao_tri = relationship('BaoTri', back_populates='thietbi', lazy=True)

# Mô hình bảng BaoTri
class BaoTri(db.Model):
    __tablename__ = 'bao_tri'

    stt = Column(Integer, autoincrement=True, primary_key=True)
    ngay_thang = Column(Date)
    hien_tuong_hu_hong = Column(String(255))
    cach_sua_chua = Column(String(255))
    chuyen_vien_sua_chua = Column(String(100))
    ghi_chu = Column(String(255))

    # Thay đổi kiểu dữ liệu của thietbi_stt thành Integer
    thietbi_stt = Column(Integer, ForeignKey('thiet_bi.stt'))  # Kiểu Integer thay vì String

    # Mối quan hệ với bảng ThietBi
    thietbi = relationship('ThietBi', back_populates='bao_tri', lazy=True)
