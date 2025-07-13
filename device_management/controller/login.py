from device_management.models import User
from device_management.models import Role
import hashlib
from device_management import login_manager

#kiem tra tai khoan mat khau co chinh xac
def check_login(user_name,password):
    # name va password khong null
    if user_name and password:
        password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()) # bam mat khau
        check =  User.query.filter(User.name.__eq__(user_name.strip()),User.password.__eq__(password)).first()
        if check:
            return (True,check)
        else:
            return (False,None)
#kiem tra trang thai co dang nhap
def is_active(id_account):
    if id_account:
        user=User.query.filter(User.id.__eq__(id_account)).first()
        return user.status

def check_role(stt):
    if stt:
        role = Role.query.filter(Role.stt == stt).first()
        if role:
            return role.name  # trả về object Role
    return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))