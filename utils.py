
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QLinearGradient, QColor
import subprocess
from datetime import datetime

            
def color_look(item , task):
    if task["sg_status_list"] in ["apr","cmpt", "fin"]:
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setStart(0, 30)
        gradient.setFinalStop(0, 50)
        gradient.setColorAt(0, QColor("#026773"))
        gradient.setColorAt(1, QColor("#000000"))
        item.setBackground(gradient)
        item.setTextAlignment(Qt.AlignCenter)
    elif task["sg_status_list"] in ["ip","kbk","hld"]:
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setStart(0, 30)
        gradient.setFinalStop(0, 50)
        gradient.setColorAt(0, QColor("#024959"))
        gradient.setColorAt(1, QColor("#000000"))
        item.setBackground(gradient)
        item.setTextAlignment(Qt.AlignCenter)
    else:
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setStart(0, 30)
        gradient.setFinalStop(0, 50)
        gradient.setColorAt(0, QColor("#012E40"))
        gradient.setColorAt(1, QColor("#000000"))
        item.setBackground(gradient)
        item.setTextAlignment(Qt.AlignCenter)

def color_look_notes(item , notes):

    if notes["sg_note_type"] == "Client_Brief":
        item.setBackground(QColor("#595959"))
        item.setTextAlignment(Qt.AlignCenter)

    else:
        item.setBackground(QColor("#262626"))
        item.setTextAlignment(Qt.AlignCenter)



def open_rv(selected_file=None):
    print("rv $$$$$$$$$$$$$$$$$$$$ rv")
    subprocess.Popen( "rv", shell=True)


def open_rv_file(selected_file=None):
    print("rv $$$$$$$$$$$$$$$$$$$$ rv")
    subprocess.Popen( ["rv", selected_file])



def open_3de(selected_file=None):
    print("3de $$$$$$$$$$$$$$$$$$$$ 3de")
    subprocess.Popen( "3dequalizer", shell=True)

def open_houdini(selected_file=None):
    print("houdini $$$$$$$$$$$$$$$$$$$$ houdini")
    subprocess.Popen( "houdini", shell=True)


def open_mari(selected_file=None):
    print("mari $$$$$$$$$$$$$$$$$$$$ mari")
    subprocess.Popen( "mari", shell=True)


def open_nuke_file(selected_file=None):
    print("nuke $$$$$$$$$$$$$$$$$$$$ nuke")
    subprocess.Popen( ["nuke", selected_file])

def open_nuke(selected_file=None):
    print("nuke $$$$$$$$$$$$$$$$$$$$ nuke")
    subprocess.Popen( "nuke", shell=True)

def open_maya(selected_file=None):
    print("maya $$$$$$$$$$$$$$$$$$$$ maya")
    subprocess.Popen( "maya", shell=True)

def open_mocha():
    print("mocha $$$$$$$$$$$$$$$$$$$$ mocha")
    subprocess.Popen("mocha20",  shell=True)

def open_sil():
    print("silhouette $$$$$$$$$$$$$$$$$$$$ silhouette")
    subprocess.Popen( "sil21",   shell=True)

def open_timecard():
    print("timecard $$$$$$$$$$$$$$$$$$$$ timecard")
    subprocess.Popen('timecard', shell=True)

def open_resolve():
    print("resolve $$$$$$$$$$$$$$$$$$$$ resolve")
    subprocess.Popen('resolve',  shell=True)

def open_blender():
    print("blender $$$$$$$$$$$$$$$$$$$$ blender")
    subprocess.Popen('blender',  shell=True)

def open_raceview():
    print("raceview $$$$$$$$$$$$$$$$$$$$ raceview")
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QLinearGradient, QColor
import subprocess
from datetime import datetime

            
def color_look(item , task):
    if task["sg_status_list"] in ["apr","cmpt", "fin"]:
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setStart(0, 30)
        gradient.setFinalStop(0, 50)
        gradient.setColorAt(0, QColor("#026773"))
        gradient.setColorAt(1, QColor("#000000"))
        item.setBackground(gradient)
        item.setTextAlignment(Qt.AlignCenter)
    elif task["sg_status_list"] in ["ip","kbk","hld"]:
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setStart(0, 30)
        gradient.setFinalStop(0, 50)
        gradient.setColorAt(0, QColor("#024959"))
        gradient.setColorAt(1, QColor("#000000"))
        item.setBackground(gradient)
        item.setTextAlignment(Qt.AlignCenter)
    else:
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setStart(0, 30)
        gradient.setFinalStop(0, 50)
        gradient.setColorAt(0, QColor("#012E40"))
        gradient.setColorAt(1, QColor("#000000"))
        item.setBackground(gradient)
        item.setTextAlignment(Qt.AlignCenter)

def color_look_notes(item , notes):

    if notes["sg_note_type"] == "Client_Brief":
        item.setBackground(QColor("#595959"))
        item.setTextAlignment(Qt.AlignCenter)

    else:
        item.setBackground(QColor("#262626"))
        item.setTextAlignment(Qt.AlignCenter)



def open_rv(selected_file=None):
    print("rv $$$$$$$$$$$$$$$$$$$$ rv")
    subprocess.Popen( "rv", shell=True)


def open_rv_file(selected_file=None):
    print("rv $$$$$$$$$$$$$$$$$$$$ rv")
    subprocess.Popen( ["rv", selected_file])



def open_3de(selected_file=None):
    print("3de $$$$$$$$$$$$$$$$$$$$ 3de")
    subprocess.Popen( "3dequalizer", shell=True)

def open_houdini(selected_file=None):
    print("houdini $$$$$$$$$$$$$$$$$$$$ houdini")
    subprocess.Popen( "houdini", shell=True)


def open_mari(selected_file=None):
    print("mari $$$$$$$$$$$$$$$$$$$$ mari")
    subprocess.Popen( "mari", shell=True)


def open_nuke_file(selected_file=None):
    print("nuke $$$$$$$$$$$$$$$$$$$$ nuke")
    subprocess.Popen( ["nuke", selected_file])

def open_nuke(selected_file=None):
    print("nuke $$$$$$$$$$$$$$$$$$$$ nuke")
    subprocess.Popen( "nuke", shell=True)

def open_maya(selected_file=None):
    print("maya $$$$$$$$$$$$$$$$$$$$ maya")
    subprocess.Popen( "maya", shell=True)

def open_mocha():
    print("mocha $$$$$$$$$$$$$$$$$$$$ mocha")
    subprocess.Popen("mocha20",  shell=True)

def open_sil():
    print("silhouette $$$$$$$$$$$$$$$$$$$$ silhouette")
    subprocess.Popen( "sil21",   shell=True)

def open_timecard():
    print("timecard $$$$$$$$$$$$$$$$$$$$ timecard")
    subprocess.Popen('timecard', shell=True)

def open_resolve():
    print("resolve $$$$$$$$$$$$$$$$$$$$ resolve")
    subprocess.Popen('resolve',  shell=True)

def open_blender():
    print("blender $$$$$$$$$$$$$$$$$$$$ blender")
    subprocess.Popen('blender',  shell=True)

def open_raceview():
    print("raceview $$$$$$$$$$$$$$$$$$$$ raceview")
    subprocess.Popen('raceview', shell=True)

def open_mozilla():
    print("firefox $$$$$$$$$$$$$$$$$$$$ firefox")
    subprocess.Popen('firefox',   shell=True)

def open_shotgrid():
    print("shotgrid $$$$$$$$$$$$$$$$$$$$ shotgrid")
    subprocess.Popen('shotgrid', shell=True)

def open_dolphin():
    print("dolphin $$$$$$$$$$$$$$$$$$$$ dolphin")
    subprocess.Popen('dolphin',  shell=True)

def get_still_working(result):

    if result["date"] == datetime.now().strftime("%Y:%m:%d") and result['stop_time'] == "Working":
        return "Available"
    else:
        return "Left"




    subprocess.Popen('raceview', shell=True)

def open_mozilla():
    print("firefox $$$$$$$$$$$$$$$$$$$$ firefox")
    subprocess.Popen('firefox',   shell=True)

def open_shotgrid():
    print("shotgrid $$$$$$$$$$$$$$$$$$$$ shotgrid")
    subprocess.Popen('shotgrid', shell=True)

def open_dolphin():
    print("dolphin $$$$$$$$$$$$$$$$$$$$ dolphin")
    subprocess.Popen('dolphin',  shell=True)

def get_still_working(result):

    if result["date"] == datetime.now().strftime("%Y:%m:%d") and result['stop_time'] == "Working":
        return "Available"
    else:
        return "Left"



