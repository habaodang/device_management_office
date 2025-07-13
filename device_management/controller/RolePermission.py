from device_management.controller import Database
from device_management.models import Role_Permission
from device_management.controller import role_service

class RolePermissionClass(Database.DatabaseAccess):
    def __init__(self):

        super().__init__(Role_Permission)

    def mapping_role_permission(self,stt_role,stt_permission):
        return super().create(role_stt=stt_role, permission_stt=stt_permission)

    def create_role(self,sttrole,permissions):
        if sttrole and permissions:
            print('vao if')
            role=role_service.RoleClass()
            newrole = role.add_role(sttrole)
            print(newrole)
            for permission in permissions:
                print('check')
                print(permission)

                self.mapping_role_permission(newrole.stt, permission)

    def delete_by_role(self,stt):
        print('vao if xoa')
        role=role_service.RoleClass()
        listrole = self.get_by_field_all('role_stt',stt)
        if listrole:
            for role in listrole:
                print(role)
                super().delete(role.stt)
            print('da xoa')

            return True
        print('khong tim thay')
        return False
