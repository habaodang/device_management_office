from device_management.routes.main_route import main
from device_management.routes.thietbi_route import thietbi_route
from device_management.routes.baotri_route import baotri_route
from device_management.routes.maintenance_route import maintenance_route
from device_management.routes.admin_route import admin_route

def register_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(thietbi_route)
    app.register_blueprint(baotri_route)
    app.register_blueprint(maintenance_route)
    app.register_blueprint(admin_route)
