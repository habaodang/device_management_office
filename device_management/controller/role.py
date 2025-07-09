from device_management.controller import retrieve_data
from device_management.models import Role_Permission


def mapping_permission(role,permissions):
    if role and permissions:
        role=retrieve_data.add_role(role)
        for permission in permissions:
            retrieve_data.mapping_role_permission(role.stt,permission)

