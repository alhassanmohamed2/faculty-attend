from socket import gethostbyname, gethostname
from os import path, getcwd
import qrcode
from datetime import datetime

def openfile(name):
    with open(name,'r') as file:
        file_lines = file.readlines()
    return file_lines

current_time = datetime.now().date()
IP = gethostbyname(gethostname())
attend_qr_code = qrcode.make(f"http://{IP}:5000/login")
qr_code_path = path.join(getcwd(),'website','static','images','IP_QR.png')
wifi_qr_code_path = path.join(getcwd(),'website','static','images','WIFI.png')
attend_qr_code.save(qr_code_path)
wifipassword = ""
students_IPs = set()
admin_info_file = path.join(getcwd(),'website','data','admin_info.txt')
subjects_info_file = path.join(getcwd(),'website','data','subjects.txt')
departement_info_file = path.join(getcwd(),'website','data','departement.txt')

shared_info = {
"selected_subject":"",
"close_attend":True,
"wifipassword":""
}

admin_subjects = openfile(subjects_info_file)
admin_info = openfile(admin_info_file)
departements = openfile(departement_info_file)

