
from flask import Blueprint, render_template,request, abort,redirect,url_for,session
from flask.helpers import flash
from sqlalchemy import func
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
    if shared_info['wifipassword'] == '':
        flash("Set Up Attend Config First",category='error')
        return redirect(url_for('views.admin_panel'))
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


@views.route('/online',methods=['POST','GET'])
def online():
    if shared_info['selected_subject'] == '':
        flash("Set Up Attend Config First",category='error')
        return redirect(url_for('views.admin_panel'))
    return render_template('online.html')

@views.route('/retrive-students',methods=['POST','GET'])
def retrive():
    update_students = Student.query.filter_by(date=current_time,subject=shared_info["selected_subject"]).all()
    num_students_c=len(students_IPs)
    num_students_r=len(update_students)
    return render_template('online_students.html',update_students=update_students,
    num_students_c=num_students_c,num_students_r=num_students_r)


@views.route('/show_search_students',methods=['POST','GET'])
def show_search_students():
    if request.remote_addr != IP:
        abort(403)
    student_name = str(request.form.get('name')).strip()
    student_deb = str(request.form.get('dep')).strip()
    subject = str(request.form.get('subject')).strip()
    database =  str(request.form.get('database')).strip()
    searched_name = ''
    days_attend = 0
    if database == "attend":
        if student_name == '':
            student_search_info = db.session.query(Student.name, func.count(Student.date)).filter_by(subject=subject,departement=student_deb).group_by(Student.name).all()
        else:
            student_search_info = Student.query.filter_by(name=student_name,departement=student_deb,subject=subject).all()
            days_attend = len(student_search_info)
            if days_attend == 0:
                return '<script>alert("Not Found")</script>'
            else:
                searched_name = student_search_info[0].name
            
    elif database == "names":
        if student_name == '':
            student_search_info = NAMES.query.filter_by(departement=student_deb,subject=subject).all()
        else:
            student_search_info = NAMES.query.filter_by(name =student_name,departement=student_deb,subject=subject).first()
            if student_search_info == None:
                return '<script>alert("Not Found")</script>'
            else:
                searched_name = student_search_info.name
        
    return render_template('searched-info.html',student_name= searched_name,days_attend=days_attend,database=database,
    student_search_info=student_search_info)

@views.route('/modify-students-action',methods=['POST','GET'])
def modify_students_action():
    student_name = str(request.form.get('name')).strip()
    student_deb = str(request.form.get('dep')).strip()
    subject = str(request.form.get('subject')).strip()
    database =  str(request.form.get('database')).strip()
    date =  str(request.form.get('date')).strip()
    if database == "names":
        if NAMES.query.filter_by(name =student_name,departement=student_deb,subject=subject).first():
            return '<script>alert("Student Alerady There")</script>' 
        new_student = NAMES(name =student_name,departement=student_deb,subject=subject)
        db.session.add(new_student)
        db.session.commit()
        return  '<script>alert("Student ADDED")</script>'
    elif database == 'attend':
        date = datetime.strptime(date, '%Y-%m-%d').date()
        if Student.query.filter_by(name =student_name,departement=student_deb,subject=subject,date=date).first():
            return '<script>alert("Student Alerady There")</script>' 
        new_student = Student(name =student_name,departement=student_deb,subject=subject,date=date)
        db.session.add(new_student)
        db.session.commit()
        return  '<script>alert("Student ADDED")</script>'
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
    elif 'admin-name' not in session: 
       return redirect(url_for('auth.admin_login'))
    else:
        return render_template('admin-panel.html')