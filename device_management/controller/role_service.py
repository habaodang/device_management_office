from device_management.controller import Database
from device_management.models import Role
from device_management.models import Role
from device_management.controller import RolePermission

class RoleClass (Database.DatabaseAccess):

    def __init__(self):
        super().__init__(Role)

    def add_role(self, rolename):
        return super().create(name=rolename)

    def delete_role(self,stt):
        role_permission=RolePermission.RolePermissionClass()
        role_permission.delete_by_role(stt)
        return super().delete(stt)

