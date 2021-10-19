from flask import Blueprint, render_template, request, abort, flash, redirect,url_for, session
from .models import NAMES, Student
from . import db
from .helpers import *

auth = Blueprint('auth',__name__)

@auth.route('/stop-attend')
def close_attend():
    shared_info['close_attend'] = True
    return 'Closed'

@auth.route('/start-attend')
def start_attend():
    shared_info['close_attend'] = False
    return 'Opened'



@auth.route('/login',methods=['POST','GET'])
def login():
    ip_address = request.remote_addr
    if ip_address == IP:
        pass
    elif (ip_address in students_IPs) or shared_info['close_attend'] :
        abort(403)
    students_names = NAMES.query.filter_by(subject=shared_info["selected_subject"]).all()
    if request.method == 'POST':
        name = str(request.form.get('name')).strip()
        departement = str(request.form.get('departement')).strip()
        student = Student.query.filter_by(name=name,date=current_time,subject=shared_info["selected_subject"]).first()
        if student:
            flash("This User is alerdy there",category='error')
        elif name == '' or departement == '':
             flash("Type Your Information",category='error')
        else:
            attend_student = Student(name=name, departement=departement, subject=shared_info["selected_subject"])
            db.session.add(attend_student)
            db.session.commit()
            flash("Success", category='success')
            students_IPs.add(ip_address)
            return redirect(url_for('views.home'))
    departements = openfile(departement_info_file)
    return render_template('login.html',departements=departements,students_names=students_names)



@auth.route('/admin-login',methods=['POST','GET'])
def admin_login():
    if request.remote_addr != IP:
        abort(403)
    if request.method == 'POST':
        admin_name = str(request.form.get('admin-name')).strip()
        admin_password = str(request.form.get('admin-password')).strip()
        if admin_name == '' or admin_password == '':
             flash("Type Your Information",category='error')
        else:
                if admin_info[0].strip() == admin_name and admin_info[1].strip() == admin_password:
                    session.permanent = True
                    session['admin-name'] = admin_info[0]
                    return redirect(url_for('views.admin_panel'))
                else:
                    flash("Incorrect Username Or PassWord",category='error')
    elif 'admin-name' in session:
        return redirect(url_for('views.admin_panel'))
    return render_template('admin-login.html')

@auth.route('/logout',methods=['POST','GET'])
def admin_logout():
    session.pop('admin-name',None)
    return redirect(url_for('auth.admin_login'))













