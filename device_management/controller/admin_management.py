from sqlalchemy import false

from device_management.models import User
from device_management.controller import retrieve_data
def create_user(user,password,cmpassword,role):
    if user:
        if password == cmpassword:
            new_user=retrieve_data.add_user(user,password,role)
            if new_user:
                return (True,'Tạo tài khoản thành công')
            else:
                return (False,'Tạo tài khoản thất bại')
        else:
            return (False,'Mật khẩu không khớp')
    else:
        return (False,'Vui lòng nhập username')