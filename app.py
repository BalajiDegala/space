
api.load("urllib3")

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QVBoxLayout, QGridLayout, QWidget, QTableWidget, QAbstractItemView,QDockWidget, \
    QTableWidgetItem, QScrollArea, QPushButton,QLineEdit, QCompleter, QHBoxLayout, QTextEdit,QProgressBar, QFrame, QGraphicsDropShadowEffect, QStatusBar,QTableView, QCheckBox, QHeaderView , QRadioButton , QListView, QTabWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QAbstractTableModel, QSize, QTimer, QRect
from PyQt5.QtGui import QPixmap, QStandardItemModel, QFont, QLinearGradient, QColor , QIcon
from PyQt5.QtNetwork import  QNetworkProxy

import sys,os
import utils
from ddshotgrid import DDShotgun
from timecard import Timesheet
from notes import NotesWidget
from market import MarketWidget
from space import SpaceWidget
from urllib import request

class TaskViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S P A C E ")

        self.space_widget = SpaceWidget()
        self.market_widget = MarketWidget()
        self.timecard_widget = Timesheet()
        self.notes_widget = NotesWidget()


        tab_widget = QTabWidget()
        tab_widget.setUsesScrollButtons(1)
        tab_widget.setMovable(1)
        tab_widget.addTab(self.space_widget , "S P A C E")
        tab_widget.addTab(self.market_widget, "M A R K E T")
        tab_widget.addTab(self.timecard_widget, "T I M E C A R D")
        tab_widget.addTab(self.notes_widget, "N O T E S")
        self.space_widget.task_table.itemSelectionChanged.connect(self.on_task_selected)
        self.setCentralWidget(tab_widget)


    def on_task_selected(self):
        try:
            env_dict = {}
            selected_rows = self.space_widget.task_table.selectionModel().selectedRows()
            if len(selected_rows) > 0:
                selected_task = self.space_widget.task_assigned[selected_rows[0].row()]
                self.space_widget.current_task = self.space_widget.task_assigned[selected_rows[0].row()]
                self.space_widget.task_id = selected_task["id"]

                self.space_widget.show_id = selected_task['project']['id']
                if selected_task['entity.Shot.sg_sequence'] is not None:
                    self.space_widget.seq_id  = selected_task['entity.Shot.sg_sequence']['id']
                self.space_widget.shot_id = selected_task['entity']['id']

                self.space_widget.dd_show = selected_task['project']['name']

                if selected_task['entity.Shot.sg_sequence'] is not None:
                    self.space_widget.dd_seq  = selected_task['entity.Shot.sg_sequence']['name']
                self.space_widget.dd_shot = selected_task['entity']['name']
                self.space_widget.dd_step = selected_task['step']['name']
                self.space_widget.dd_short_step = selected_task['step.Step.short_name']

                os.environ["DD_SHOW"] = self.space_widget.dd_show
                os.environ["DD_ROLE"] = self.space_widget.dd_short_step
                self.notes_widget.shot_id = self.space_widget.shot_id
                env_dict.update({"shot": self.space_widget.dd_shot, "seq": self.space_widget.dd_seq , "show": self.space_widget.dd_show , "step": self.space_widget.dd_step})
                self.market_widget.env = env_dict
                fields = ["content", "step", "sg_status_list", "start_date", "due_date", "id","entity", "image", "entity.Shot.sg_sequence" ,  "sg_description" , "entity.Shot.sg_dd_client_name", "smart_cut_summary_display", "sg_task_type",  "task_assignees", "sg_status_list","project", "est_in_mins", "duration", "sg_head_in", "sg_tail_out" , "sg_cut_in", "sg_cut_out"]
                task_details = self.space_widget.shotgrid.sg.find('Task' , [['id' , 'is', self.space_widget.task_id ]] , fields)
                task_details = task_details[0]
                self.space_widget.current_task_details = task_details

                self.space_widget.shot_details = self.space_widget.shotgrid.sg.find('Shot' , [['id' ,'is', self.space_widget.shot_id]] , fields)
                if self.space_widget.shot_details == []:
                    self.space_widget.shot_details = self.space_widget.shot_details
                else :
                    self.space_widget.shot_details = self.space_widget.shot_details[0]
                    self.space_widget.duration.setText("Summary :  " + str(self.space_widget.shot_details['smart_cut_summary_display']))
                if self.space_widget.task_id:
                    self.space_widget.associated_tasks = self.space_widget.shotgrid.sg.find("Task", [['entity', 'is', {'type': 'Shot', 'id': self.space_widget.shot_id}]],["content", "step", "sg_status_list", "task_assignees"])
                    self.space_widget.team_task_table.setRowCount(len(self.space_widget.associated_tasks))

                    for i, task in enumerate(self.space_widget.associated_tasks):
                        self.space_widget.team_task_table.setItem(i, 0, QTableWidgetItem(task["content"]))
                        self.space_widget.team_task_table.setItem(i, 1, QTableWidgetItem(task["step"]["name"]))
                        item = QTableWidgetItem(task["sg_status_list"])
                        utils.color_look(item, task)
                        self.space_widget.team_task_table.setItem(i, 2, item)
                        separator = ","
                        artists = [k["name"] for k in task["task_assignees"]]
                        artists =  separator.join(artists)
                        self.space_widget.team_task_table.setItem(i, 3, QTableWidgetItem(artists))
                      
                if selected_task.get("image") is not None:
                    try:
                        thumb_url = selected_task["image"]
                        thumb_data = request.urlopen(thumb_url).read()
                        thumb_pixmap = QPixmap()
                        thumb_pixmap.loadFromData(thumb_data)
                        self.space_widget.image_label.setPixmap(thumb_pixmap)
                        self.space_widget.image_label.setAlignment(Qt.AlignCenter)
                    except :
                        print("URL issue , Image cannot be shown")
                else :
                    self.space_widget.image_label.setText("D D H B")
                    self.space_widget.image_label.setAlignment(Qt.AlignCenter)
                    print("No Thumbnail")

                self.space_widget.dd_role = selected_task['step']['name']
                self.space_widget.project_label.setText(self.space_widget.dd_show)
                self.space_widget.shot_id_label.setText(self.space_widget.dd_shot)
                self.space_widget.seq_id_label.setText(self.space_widget.dd_seq)
                self.space_widget.description_label.setText(task_details['sg_description'])
                self.space_widget.task_type_label.setText(selected_task.get('content', 'N/A'))
                task_duration = None
                if task_details['duration'] is not None : 
                    task_duration = task_details['duration']/480
                self.space_widget.summary.setText("Bid: %s " % (task_duration))

                self.space_widget.assigned_to_label.clear()
                shot_assigned_users = [user['name'] for user in task_details.get("task_assignees",[])]
                for artist in shot_assigned_users:
                    self.space_widget.assigned_to_label.addItem(artist)

        except Exception as e :
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SplashScreen()
    window.show()
    sys.exit(app.exec_())
