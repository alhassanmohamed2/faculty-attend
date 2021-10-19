
from flask import Blueprint, render_template,request, abort,redirect,url_for,session
from flask.helpers import flash
from .models import Student, NAMES
from .helpers import *
from . import db
import time
views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/attend',methods=['POST','GET'])
def attend():
    if request.remote_addr != IP:
        abort(403)
    return render_template('attend.html',IP=IP,wifi=shared_info['wifipassword'],time=time.time())

@views.route('/attend-config',methods=['POST','GET'])
def attend_config():
    if request.remote_addr != IP:
        abort(403)
    return render_template('attend-config.html',admin_subjects=admin_subjects)

@views.route('/modify-students',methods=['POST','GET'])
def modify_students():
    if request.remote_addr != IP:
        abort(403)
    return render_template('modify-students.html',admin_subjects=admin_subjects,departements=departements)

@views.route('/search-students',methods=['POST','GET'])
def search_students():
    if request.remote_addr != IP:
        abort(403)
    return render_template('search-students.html',admin_subjects=admin_subjects,departements=departements)

@views.route('/show_search_students',methods=['POST','GET'])
def show_search_students():
    if request.remote_addr != IP:
        abort(403)
    student_name = str(request.form.get('name')).strip()
    student_deb = str(request.form.get('dep')).strip()
    subject = str(request.form.get('subject')).strip()
    student_search_info = Student.query.filter_by(name=student_name,departement=student_deb,subject=subject).all()
    days_attend = len(student_search_info)
    if days_attend == 0:
        return '<script>alert("Not Found")</script>'
    return render_template('searched-info.html',student_name= student_search_info[0].name,days_attend=days_attend)

@views.route('/admin-panel',methods=['POST','GET'])
def admin_panel():
    if request.remote_addr != IP:
        abort(403)
    if request.method == 'POST':
        if request.form.get('attend-config') != None:
            shared_info["selected_subject"] = str(request.form.get('subject')).strip()
            shared_info['wifipassword'] = str(request.form.get('wifi')).strip()
            shared_info["close_attend"] = False
            wifi_qr = qrcode.make(shared_info['wifipassword'])
            wifi_qr.save(wifi_qr_code_path)
            return redirect(url_for('views.attend'))
        elif request.form.get('modify') != None:
            student_name = str(request.form.get('s-name')).strip()
            student_deb = str(request.form.get('departement')).strip()
            subject = str(request.form.get('subject')).strip()
            new_student = NAMES(name =student_name,departement=student_deb,subject=subject)
            db.session.add(new_student)
            db.session.commit()
            flash("Student ADDED", category='success')
            return render_template('admin-panel.html') 
    elif 'admin-name' not in session: 
       return redirect(url_for('auth.admin_login'))
    else:
        return render_template('admin-panel.html')