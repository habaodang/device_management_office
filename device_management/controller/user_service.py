from device_management.controller import Database
from device_management.models import User
from device_management.controller.RolePermission import RolePermissionClass
import hashlib

class UserClass(Database.DatabaseAccess):
    def __init__(self,username='',password=''):
        self.username = username
        self.password = password
        super().__init__(User)

    def add_user(self,user, password, cmpassword, role):
        if user:
            if password == cmpassword:
                hash_password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
                new_user = super().create(name=user,password= hash_password, role_stt=role)
                if new_user:
                    return (True, 'Tạo tài khoản thành công')
                else:
                    return (False, 'Tạo tài khoản thất bại')
            else:
                return (False, 'Mật khẩu không khớp')
        else:
            return (False, 'Vui lòng nhập username')

    @staticmethod
    def check_permission(role_stt):
        role_permission = RolePermissionClass()
        list_role_permission=role_permission.get_by_field_all('role_stt',role_stt)
        list_permission=[]
        for permission in list_role_permission:
            list_permission.append(permission.permission.name)

        return list_permission