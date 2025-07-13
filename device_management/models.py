from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean,Enum
from sqlalchemy.orm import relationship
from device_management import db
from flask_login import UserMixin

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

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    stt = Column(Integer, autoincrement=True, primary_key=True)
    name=Column(String(255), nullable=False,unique=True)
    password=Column(String(255), nullable=False)
    role_stt = Column(Integer,ForeignKey('role.stt'), nullable=False)

    role=relationship('Role', back_populates='user', lazy=True)

    def get_id(self):
        return str(self.stt)

class Role(db.Model):
    __tablename__ = 'role'
    stt = Column(Integer, autoincrement=True, primary_key=True)
    name=Column(String(255), nullable=False,unique=True)

 # 1 Role có nhiều User
    user = relationship('User', back_populates='role', lazy=True)
    role_permission = relationship('Role_Permission', back_populates='role', lazy=True)

class Permission(db.Model):
    __tablename__ = 'permission'
    stt = Column(Integer, autoincrement=True, primary_key=True)
    name=Column(String(255), nullable=False,unique=True)

    role_permission = relationship('Role_Permission', back_populates='permission', lazy=True)

class Role_Permission(db.Model):
    __tablename__ = 'role_permission'
    stt = Column(Integer, autoincrement=True, primary_key=True)
    role_stt = Column(Integer,ForeignKey('role.stt'), nullable=False)
    permission_stt = Column(Integer,ForeignKey('permission.stt'), nullable=False)

    role=relationship('Role', back_populates='role_permission', lazy=True)
    permission=relationship('Permission', back_populates='role_permission', lazy=True)