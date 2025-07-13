from flask import Blueprint,request,redirect,render_template,url_for,session
import device_management.controller.Thietbi_service as thietbi_service
from flask_login import login_required

maintenance_route=Blueprint('maintenance_route',__name__)

@maintenance_route.route('/maintenance')
@login_required
def maintenance():
    if 'Read' not in session['permission']:
        return redirect(url_for('thietbi_route.main_information_page'))
    thietbi=thietbi_service.Thietbi_service()

    devices=thietbi.get_device_status_maintenance()
    return render_template('maintenance.html',devices=devices)

@maintenance_route.route('/status-maintenance')
@login_required
def status_maintenance():
    thietbi=thietbi_service.Thietbi_service()
    stt=request.args.get('stt')
    device = thietbi.set_status_maintenance(stt)
    return redirect(url_for('baotri_route.form_repair',stt=stt))
