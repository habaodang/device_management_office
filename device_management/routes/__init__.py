from device_management.routes.main_route import main

def register_routes(app):
    app.register_blueprint(main)