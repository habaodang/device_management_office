from device_management.controller import Database
from device_management.models import BaoTri


class baotri_service(Database.DatabaseAccess):
    def __init__(self):
        super().__init__(BaoTri)

    def get_device_by_stt_all(self, stt):
        return super().get_by_field_all('thietbi_stt', stt)

