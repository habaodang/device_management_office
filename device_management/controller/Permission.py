from device_management.controller import Database
from device_management.models import Permission

class PermissionClass(Database.DatabaseAccess):
    def __init__(self):
        super().__init__(Permission)

