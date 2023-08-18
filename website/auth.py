from flask import Blueprint, render_template, request, abort, flash, redirect,url_for, session
from .models import NAMES, Student
from . import db
from .helpers import *

import subprocess

auth = Blueprint('auth',__name__)

@auth.route('/stop-attend')
def close_attend():
    shared_info['close_attend'] = True
    return 'Closed'

@auth.route('/start-attend')
def start_attend():
    if shared_info["selected_subject"] == "":
        return '<script>alert("select the subject from the configuration first")</script>' 
    shared_info['close_attend'] = False
    return f'<script>alert(\'Selected Subject is: {shared_info["selected_subject"]}\')</script>'



@auth.route('/login',methods=['POST','GET'])
def login():
    mac_addr = set()
    ip_address = request.remote_addr
    mac_adress =  subprocess.run(f'for /f "tokens=2" %a in (\'arp -a ^| find "{ip_address}"\') do @echo %a'
                                 , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    mac_adress = mac_adress.stdout
    departements = openfile(departement_info_file)
    if ip_address == IP:
        pass
    elif (mac_adress[0:17] in students_IPs) or shared_info['close_attend'] :
        abort(403)
    if request.method == 'POST':
        
        if request.form.get('registere') != None:
            if request.form.get('name') == None:
                flash("Select Departement To Show the Names",category='error')
                return redirect(url_for('auth.login'))
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
                students_IPs.add(str(mac_adress)[0:17])
                return redirect(url_for('views.home'))
        elif request.form.get('select_dep') != None:
            departement = str(request.form.get('departement')).strip()
            students_info = NAMES.query.filter_by(subject=shared_info["selected_subject"],departement=departement).all()
            return render_template('login.html',departements=departements,students_names=students_info)
    return render_template('login.html',departements=departements)


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













