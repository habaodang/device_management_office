
from device_management.models import Account
import hashlib


#kiem tra tai khoan mat khau co chinh xac
def check_login(user_name,password):

    # name va password khong null
    if user_name and password:
        password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()) # bam mat khau
        return  Account.query.filter(Account.name_account.__eq__(user_name.strip()),Account.password.__eq__(password)).first()

#kiem tra trang thai co dang nhap
def is_active(id_account):
    if id_account:
        account=Account.query.filter(Account.id.__eq__(id_account)).first()
        return account.status
