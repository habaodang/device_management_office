from flask import Blueprint,request,redirect,render_template,url_for,flash,session
import device_management.controller.role_service as role_service
import device_management.controller.Permission as Permission
import device_management.controller.RolePermission as rolepermission
import device_management.controller.user_service as user_service
from flask_login import login_required

admin_route = Blueprint('admin_route', __name__)

@admin_route.route('/admin-management')
@login_required
def admin_management():
    role= role_service.RoleClass()

    roles=role.get_all()

    return render_template('admin/create_user.html',roles=roles)

@admin_route.route('/admin-management/create_role')
@login_required
def admin_create_role():
    permission=Permission.PermissionClass()
    role= role_service.RoleClass()

    permissions=permission.get_all()
    roles=role.get_all()

    return render_template('admin/create_role.html',permissions=permissions,roles=roles)

@admin_route.route('/admin-management/delete')
@login_required
def delete_user():
    user=user_service.UserClass()

    listuser=user.get_all()
    print(listuser)
    return render_template('admin/delete_user.html',users=listuser)


@admin_route.route('/admin-management/delete/process')
@login_required
def delete_user_process():
    user_stt = request.args.get('stt')  # Lấy các thiết bị được chọn từ form

    if user_stt:
        user = user_service.UserClass()
        user.delete(user_stt)

    return redirect(url_for('admin_route.delete_user'))

@admin_route.route('/admin-add-user', methods=['GET', 'POST'])
@login_required
def admin_add_user():
    if request.method == 'POST':

        user=user_service.UserClass()

        username = request.form['user_name']
        password = request.form['password']
        cmpassword = request.form['cmpassword']
        role = request.form['role']
        try:
            check,message=user.add_user(username,password,cmpassword,role)
            if check == False:
                session.pop('_flashes', None)
                flash(message,'danger')
        except:
            session.pop('_flashes', None)
            flash("Không thể tạo với username này",'danger')
    return redirect(url_for('admin_route.admin_management'))

@admin_route.route('/admin-add-role', methods=['GET', 'POST'])
@login_required
def admin_add_role():
    if request.method == 'POST':
        name = request.form['rolename']
        selected_permission = request.form.getlist('permission')

        role_permission=rolepermission.RolePermissionClass()
        role_permission.create_role(name,selected_permission)

    return redirect(url_for('admin_route.admin_create_role'))

@admin_route.route('/delete-role')
@login_required
def delete_role():
    session.pop('_flashes', None)
    role=role_service.RoleClass()
    role_id = request.args.get('stt')
    try:
        role.delete_role(role_id)
    except:
        flash('Không thể xóa role vừa mới chọn')

    return redirect(url_for('admin_route.admin_create_role'))
