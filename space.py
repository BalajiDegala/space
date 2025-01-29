
from PyQt5.QtWidgets import QApplication, QLabel, QComboBox, QVBoxLayout, QGridLayout, QWidget, QTableWidget, QAbstractItemView,\
    QTableWidgetItem, QScrollArea, QPushButton, QCompleter, QHBoxLayout, QTextEdit, QCheckBox, QHeaderView 
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon

import subprocess
import sys
import os
from datetime import datetime
from time import sleep
import utils
from ddshotgrid import DDShotgun

show = os.environ["DD_SHOW"]

class SpaceWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.shot_id = None
        self.seq_id = None
        self.show_id = None

        self.dd_shot = None
        self.dd_seq = None
        self.dd_show = None

        self.task_id = None

        self.shotgrid = DDShotgun()
        self.user = self.shotgrid.user
        self.selected_task_details = {}
        self.ui_elements()
        self.populate_users()
        self.populate_projects()

    def ui_elements(self):

        self.space_elements()
        self.task_space()
        self.info_space()
        self.app_space()

    def space_elements(self):

        self.space_button = QPushButton("D D  S P A C E")
        self.space_button.setMinimumHeight(80)
        self.space_button.clicked.connect(self.reset_filters)

        self.font = QFont()
        self.font.setPointSize(40)
        self.font.setFamily("Segoe UI")
        self.space_button.setFont(self.font)
        self.space_button.setShortcut("F2")

        self.user_combo = QComboBox()
        self.user_combo.setMinimumHeight(35)
        self.user_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.user_combo.setEditable(True)
        self.user_combo.setInsertPolicy(QComboBox.NoInsert)
        self.user_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.user_combo.setCurrentText(self.user)
        self.user_combo.setToolTip("select the User ")

        self.project_combo = QComboBox()
        self.project_combo.setMinimumHeight(35)
        self.project_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.project_combo.setEditable(True)
        self.project_combo.setInsertPolicy(QComboBox.NoInsert)
        self.project_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.project_combo.currentIndexChanged.connect(self.populate_sequences)
        self.project_combo.currentIndexChanged.connect(self.populate_assets)
        self.project_combo.setToolTip("select the Project ")

        self.sequence_combo = QComboBox()
        self.sequence_combo.setMinimumHeight(35)
        self.sequence_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.sequence_combo.setEditable(True)
        self.sequence_combo.setInsertPolicy(QComboBox.NoInsert)
        self.sequence_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.sequence_combo.currentIndexChanged.connect(self.populate_shots)
        self.sequence_combo.setToolTip("select the Sequence ")

        self.assets_combo = QComboBox()
        self.assets_combo.setMinimumHeight(35)
        self.assets_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.assets_combo.setEditable(True)
        self.assets_combo.setInsertPolicy(QComboBox.NoInsert)
        self.assets_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.assets_combo.setToolTip("select the Asset ")

        self.shot_combo = QComboBox()
        self.shot_combo.setMinimumHeight(35)
        self.shot_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.shot_combo.setEditable(True)
        self.shot_combo.setInsertPolicy(QComboBox.NoInsert)
        self.shot_combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.shot_combo.setToolTip("select the Shot ")

        self.status_combo = QComboBox()
        self.status_combo.setMinimumHeight(35)
        self.status_combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.status_combo.clear()
        self.status_combo.setEditable(True)
        self.status_combo.addItem("")
        status_list = ['cbb', 'kbk', 'rev', 'pin', 'apr', 'ip', 'bid', 'wtg', 'rts', 'omt', 'plsh', 'hld', 'fin', 'pndng', "cmpt", "space"]
        self.status_combo.addItems(status_list)
        self.status_combo.setCurrentText("space")
        self.status_combo.completer().setCompletionMode(QCompleter.PopupCompletion)

        self.load_button = QPushButton("+ L O A D ")
        self.load_button.setShortcut("F3")
        self.load_button.clicked.connect(self.load_tasks)

        self.smart_search = QCheckBox()
        self.smart_search.setText("Smart search")

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(7)
        self.task_table.setHorizontalHeaderLabels(["Project", "Sequence", "Shot/Asset","Task Name", "Status", "Start Date", "End Date" ])
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.grid = QGridLayout()
        self.grid.addWidget(self.space_button,1,0,1,3)
        self.grid.addWidget(self.user_combo,2,0)
        self.grid.addWidget(self.project_combo,2,1)
        self.grid.addWidget(self.status_combo,2,2)
        self.grid.addWidget(self.sequence_combo,3,0)
        self.grid.addWidget(self.assets_combo,3,1)
        self.grid.addWidget(self.shot_combo,3,2)
        self.grid.addWidget(self.smart_search,4,0)
        self.grid.addWidget(self.load_button,4,2)
        self.grid.addWidget(self.task_table,5,0,5,3)

    
    def task_space(self):

        self.project_label = QLabel()
        self.seq_id_label = QLabel()
        self.shot_id_label = QLabel()
        self.task_type_label = QLabel()
        self.assigned_to_label = QComboBox()
        self.image_label = QLabel()
        self.image_label.setFixedSize(600,300)
        self.summary = QLabel()
        self.duration = QLabel()

        self.description_label = QTextEdit()
        self.description_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.description_label.setFixedSize(600,300)

    def info_space(self):
        
        self.team_task_table = QTableWidget()
        self.team_task_table.setColumnCount(4)
        self.team_task_table.setHorizontalHeaderLabels(["Task Name","Department","Status","Artist"])
        self.team_task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.team_task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.task_main_layout = QHBoxLayout()
        self.task_main_layout.addWidget(self.project_label)
        self.task_main_layout.addWidget(self.seq_id_label)
        self.task_main_layout.addWidget(self.shot_id_label)
        self.task_main_layout.addWidget(self.task_type_label)
        self.task_main_layout.addWidget(self.assigned_to_label)

        self.image_layout = QHBoxLayout()
        self.image_layout.addWidget(self.image_label)
        self.image_layout.addWidget(self.description_label)

        self.task_info_layout = QHBoxLayout()
        self.task_info_layout.addWidget(self.duration)
        self.task_info_layout.addWidget(self.summary)

        self.shot_layout = QVBoxLayout()
        self.shot_layout.addWidget(self.team_task_table)

        self.details_layout = QVBoxLayout()
        self.details_layout.addLayout(self.task_main_layout)
        self.details_layout.addLayout(self.image_layout)
        self.details_layout.addLayout(self.task_info_layout)
        self.details_layout.addLayout(self.shot_layout)

        self.task_layout = QHBoxLayout()
        self.task_layout.addLayout(self.grid,4)
        self.task_layout.addLayout(self.details_layout,6)

    def app_space(self):

        app_layout = QHBoxLayout()

        rv = QPushButton()
        rv.setFixedSize(100,100)
        rv.setIcon(QIcon('resources/rv.png'))
        rv.setIconSize(QSize(80,80))
        rv.clicked.connect(self.open_app(utils.open_rv))
        rv.setToolTip("sg RV")

        threede = QPushButton()
        threede.setFixedSize(100,100)
        threede.setIcon(QIcon('resources/3dequalizer.png'))
        threede.setIconSize(QSize(80,80))
        threede.clicked.connect(self.open_3de)
        threede.setToolTip("sg 3dequalizer")

        houdini = QPushButton()
        houdini.setFixedSize(100,100)
        houdini.setIcon(QIcon('resources/publish_houdini_main.png'))
        houdini.setIconSize(QSize(80,80))
        houdini.clicked.connect(self.open_app(utils.open_houdini))
        houdini.setToolTip("sg HOUDINI")

        mari = QPushButton()
        mari.setFixedSize(100,100)
        mari.setIcon(QIcon('resources/publish_mari_main.png'))
        mari.setIconSize(QSize(80,80))
        mari.clicked.connect(self.open_app(utils.open_mari))
        mari.setToolTip("sg MARI")

        nuke = QPushButton()
        nuke.setFixedSize(100,100)
        nuke.setIcon(QIcon('resources/publish_nuke_main.png'))
        nuke.clicked.connect(self.open_nuke)
        nuke.setIconSize(QSize(80,80))
        nuke.setToolTip("sg NUKE")

        maya = QPushButton()
        maya.setFixedSize(100,100)
        maya.setIcon(QIcon('resources/publish_maya_main.png'))
        maya.setIconSize(QSize(80,80))
        maya.clicked.connect(self.open_maya)
        maya.setToolTip("sg MAYA")

        mocha = QPushButton()
        mocha.setFixedSize(100,100)
        mocha.setIcon(QIcon('resources/mochaproIcon.jpeg'))
        mocha.setIconSize(QSize(80,80))
        mocha.clicked.connect(self.open_app(utils.open_mocha))
        mocha.setToolTip("MOCHA PRO")

        sil = QPushButton()
        sil.setFixedSize(100,100)
        sil.setIcon(QIcon('resources/sfx.png'))
        sil.setIconSize(QSize(80,80))
        sil.clicked.connect(self.open_sil)
        sil.setToolTip("SILHOUETTE")

        timecard = QPushButton()
        timecard.setFixedSize(100,100)
        timecard.setIcon(QIcon('resources/timecard.png'))
        timecard.setIconSize(QSize(80,80))
        timecard.clicked.connect(self.open_app(utils.open_timecard))
        timecard.setToolTip("TIMECARD")

        resolve = QPushButton()
        resolve.setFixedSize(100,100)
        resolve.setIcon(QIcon('resources/DV_Resolve.png'))
        resolve.setIconSize(QSize(80,80))
        resolve.clicked.connect(self.open_app(utils.open_resolve))
        resolve.setToolTip("RESOLVE")

        blender = QPushButton()
        blender.setFixedSize(100,100)
        blender.setIcon(QIcon('resources/blender.png'))
        blender.setIconSize(QSize(80,80))
        blender.clicked.connect(self.open_app(utils.open_blender))
        blender.setToolTip("BLENDER")


        raceview = QPushButton()
        raceview.setFixedSize(100,100)
        raceview.setIcon(QIcon('resources/raceview_icon.jpeg'))
        raceview.setIconSize(QSize(80,80))
        raceview.clicked.connect(self.open_app(utils.open_raceview))
        raceview.setToolTip("RAVIEW")


        rotoart = QPushButton()
        rotoart.setFixedSize(100,100)
        rotoart.setIcon(QIcon('resources/rotoart.png'))
        rotoart.setIconSize(QSize(80,80))
        rotoart.clicked.connect(self.open_rotoart)
        rotoart.setToolTip("ROTOART")


        firefox = QPushButton()
        firefox.setFixedSize(100,100)
        firefox.setIcon(QIcon('resources/mozicon128.png'))
        firefox.setIconSize(QSize(80,80))
        firefox.clicked.connect(self.open_app(utils.open_mozilla))
        firefox.setToolTip("FIREFOX")


        ddpipe = QPushButton()
        ddpipe.setFixedSize(100,100)
        ddpipe.setIcon(QIcon('resources/ddpipe.png'))
        ddpipe.setIconSize(QSize(80,80))
        ddpipe.clicked.connect(self.open_ddpipe)
        ddpipe.setToolTip("DD-PIPE")

        dolphin = QPushButton()
        dolphin.setFixedSize(100,100)
        dolphin.setIcon(QIcon('resources/dolphin.png'))
        dolphin.setIconSize(QSize(80,80))
        dolphin.clicked.connect(self.open_dolphin)
        dolphin.setToolTip("DOLPHIN")


        goto_layout_addons = QHBoxLayout()
        goto_layout_addons.addWidget(rv)
        goto_layout_addons.addWidget(threede)
        goto_layout_addons.addWidget(houdini)
        goto_layout_addons.addWidget(mari)
        goto_layout_addons.addWidget(nuke)
        goto_layout_addons.addWidget(maya)
        goto_layout_addons.addWidget(mocha)
        goto_layout_addons.addWidget(sil)
        goto_layout_addons.addWidget(timecard)
        goto_layout_addons.addWidget(resolve)
        goto_layout_addons.addWidget(blender)
        goto_layout_addons.addWidget(raceview)
        goto_layout_addons.addWidget(rotoart)
        goto_layout_addons.addWidget(firefox)
        goto_layout_addons.addWidget(ddpipe)
        goto_layout_addons.addWidget(dolphin)

        goto_layout_with_render = QVBoxLayout()
        goto_layout_with_render.addLayout(goto_layout_addons)

        scroll_widget1 = QWidget(self)
        scroll_widget1.setLayout(goto_layout_with_render)

        scroll = QScrollArea(self)
        scroll.setWidget(scroll_widget1)
        scroll.setAlignment(Qt.AlignCenter)
        app_layout.addWidget(scroll)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.task_layout,812)
        main_layout.addLayout(app_layout,188)

        self.setLayout(main_layout)

    def folderlocation(self):
        try:
            folder_path = f"/shotgrid/{self.dd_show}/{self.dd_seq}/{self.dd_shot}" # change to yor shotgrid folder
            return folder_path
        except  Exception as e:
            print(e)

    def open_dolphin(self):
        print("dolphin $$$$$$$$$$$$$$$$$$$$ dolphin")
        if self.dd_show is not None:
            subprocess.Popen(["dolphin", f"{self.folderlocation()}" ]) 
        else :
            subprocess.Popen(["dolphin", f"/home/{self.user}" ]) # change to yor home folder
    def open_nuke(self):
        print("nuke $$$$$$$$$$$$$$$$$$$$ nuke")
        subprocess.Popen( ["konsole", "--new-tab" ,"--workdir" , f"{self.folderlocation()}" ,"-e", "nuke &"])

    def open_maya(self):
        print("maya $$$$$$$$$$$$$$$$$$$$ maya")
        subprocess.Popen( ["konsole", "--new-tab" ,"--workdir" , f"{self.folderlocation()}" ,"-e", "maya"])

    def open_3de(self):
        print("3de $$$$$$$$$$$$$$$$$$$$ 3de")
        subprocess.Popen( ["konsole", "--new-tab" ,"--workdir" , f"{self.folderlocation()}" ,"-e", "3dequalizer"])

    def open_sil(self):
        print("silhouette $$$$$$$$$$$$$$$$$$$$ silhouette")
        subprocess.Popen( "sil21",   shell=True)

    def open_ddpipe(self):
        print("ddpipe $$$$$$$$$$$$$$$$$$$$ ddpipe")
        subprocess.Popen( "ddpipe",   shell=True)

    def open_rotoart(self):
        print("rotoArt $$$$$$$$$$$$$$$$$$$$ rotoArt")
        subprocess.Popen( "rotoArt",   shell=True)


    def populate_users(self):
        users = self.shotgrid.sg_users()
        for user in users:
            self.user_combo.addItem(user["login"])
        self.user_combo.setCurrentText(self.user)

    def populate_projects(self):

        user_id = self.user_combo.currentText()
        if user_id is not None:
            projects = self.shotgrid.sg_projects()
            self.project_combo.clear()
            self.project_combo.addItem("All Projects")
            for project in projects:
                self.project_combo.addItem(project["name"])
        if show != "":
            self.project_combo.setCurrentText(show)


    def populate_assets(self):
        project_id = self.project_combo.currentText()
        if  project_id is not None:
            assets = self.shotgrid.sg_assets(project_id)
            self.assets_combo.clear()
            self.assets_combo.addItem("All Assets")
            for asset in assets:
                self.assets_combo.addItem(asset["code"])

    def populate_sequences(self):
        project_id = self.project_combo.currentText()
        if  project_id is not None:
            sequences = self.shotgrid.sg_sequences(project_id)
            self.sequence_combo.clear()
            self.sequence_combo.addItem("All Sequences")
            for sequence in sequences:
                self.sequence_combo.addItem(sequence["code"])

    def populate_shots(self):
        project_id = self.project_combo.currentText()
        sequence_id = self.sequence_combo.currentText()
        if  sequence_id is not None:
            shots = self.shotgrid.sg_shots(project_id,sequence_id)
            self.shot_combo.clear()
            self.shot_combo.addItem("All Shots")
            for shot in shots:
                self.shot_combo.addItem(shot["code"], shot["id"])

    def reset_filters(self):
        self.user_combo.setCurrentText(self.user)
        self.project_combo.setCurrentText("All Projects")
        self.assets_combo.setCurrentText("All Assets")
        self.sequence_combo.setCurrentText("All Sequences")
        self.shot_combo.setCurrentText("All Shots")
        self.load_tasks()

    def load_filters(self):

        if self.user_combo.currentText() != self.user :
            user_id = self.user_combo.currentText()
        else :
            user_id = self.user
        id_user = self.shotgrid.sg_user(user_id)
        project_id = self.project_combo.currentText()
        sequence_id = self.sequence_combo.currentText()
        shot_id = self.shot_combo.currentText()
        asset_id = self.assets_combo.currentText()
        status_id = str(self.status_combo.currentText())

        self.filters = []
        if id_user:
            self.filters.append(["task_assignees", "is", {"type": "HumanUser", "id": id_user}])
        if project_id  != "All Projects":
            self.filters.append(["project.Project.name", "is", project_id ])
        if sequence_id != "All Sequences":
            self.filters.append(["entity.Shot.sg_sequence.Sequence.code", "is", sequence_id])
        if shot_id  != 'All Shots':
            self.filters.append(["entity.Shot.code", "is", shot_id])
        if asset_id != 'All Assets':
            self.filters.append(["entity.Asset.code", "is", asset_id])
        if status_id:
            if status_id == "space":
                self.filters.append({"filter_operator" : "any", "filters" : [["sg_status_list", "is", "ip"],["sg_status_list", "is", "kbk"], ["sg_status_list", "is", "rts"]]})
            else : 
                self.filters.append(["sg_status_list", "is", status_id])
        return self.filters

    def load_tasks(self):
        filters = self.load_filters()
        if self.smart_search.isChecked():
            if len(filters) >= 3:
                filters = filters[1:]

        fields = ["content", "sg_status_list", "start_date", "due_date", "entity", "step", "entity.Shot.sg_sequence" ,  "project", "id", "image", "step.Step.short_name"]

        self.task_assigned = self.shotgrid.sg.find("Task", filters, fields)
        self.task_assigned = self.task_assigned[::-1]
        self.task_table.setRowCount(len(self.task_assigned))

        for i, task in enumerate(self.task_assigned):

            self.task_table.setItem(i, 0, QTableWidgetItem(str(task["project"]["name"])))
            if task["entity.Shot.sg_sequence"] is not None:
                getTask = task["entity.Shot.sg_sequence"]["name"]
            else :
                getTask = "N/a"
            self.task_table.setItem(i, 1, QTableWidgetItem(str(getTask)))
            self.task_table.setItem(i, 2, QTableWidgetItem(str(task["entity"]["name"])))
            self.task_table.setItem(i, 3, QTableWidgetItem(task["content"]))
            item = QTableWidgetItem(task["sg_status_list"])
            utils.color_look(item, task)
            self.task_table.setItem(i, 4, item)
            self.task_table.setItem(i, 5, QTableWidgetItem(str(task["start_date"])))
            self.task_table.setItem(i, 6, QTableWidgetItem(str(task["due_date"])))
        print("jobs loaded")

    def open_app(self, app):
        return app


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpaceWidget()
    window.show()
    sys.exit(app.exec_())
