
from device_management.models import User
import hashlib


#kiem tra tai khoan mat khau co chinh xac
def check_login(user_name,password):
    print('in def')
    # name va password khong null
    if user_name and password:
        print('exists user')
        password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()) # bam mat khau
        check =  User.query.filter(User.name.__eq__(user_name.strip()),User.password.__eq__(password)).first()
        if check:
            print('T')
            return True
        else:
            print('F')
            return False
#kiem tra trang thai co dang nhap
def is_active(id_account):
    if id_account:
        user=User.query.filter(User.id.__eq__(id_account)).first()
        return user.status
