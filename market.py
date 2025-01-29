
from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget,  QPushButton,  QCompleter, QHBoxLayout, QTabWidget, QListView, QLabel, QListWidget, QTreeView, QFileSystemModel, QMessageBox, QAbstractItemView, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QModelIndex, Qt
import subprocess
import utils
import sys
from ddshotgrid import DDShotgun
from space import SpaceWidget
import os

class MarketWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.env = {}
        self.shotgrid = DDShotgun()
        self.space_widget = SpaceWidget()
        self.market_space()

    def market_space(self):

        self.work_publish_check = QComboBox()
        self.work_publish_check.setMinimumHeight(35)
        self.work_publish_check.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.work_publish_check.setEditable(True)
        self.work_publish_check.addItems(["work","publish"])
        self.work_publish_check.setInsertPolicy(QComboBox.NoInsert)
        self.work_publish_check.completer().setCompletionMode(QCompleter.PopupCompletion)

        self.software_select = QComboBox()
        self.software_select.setMinimumHeight(35)
        self.software_select.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.software_select.setEditable(True)
        self.software_select.addItems(["nuke","maya","mari","houdini","3de4","silhouette", "ingest"])
        self.software_select.setInsertPolicy(QComboBox.NoInsert)
        self.software_select.completer().setCompletionMode(QCompleter.PopupCompletion)

        self.shot_asset_check = QComboBox()
        self.shot_asset_check.setMinimumHeight(35)
        self.shot_asset_check.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.shot_asset_check.setEditable(True)
        self.shot_asset_check.addItems(["shot","asset"])
        self.shot_asset_check.setInsertPolicy(QComboBox.NoInsert)
        self.shot_asset_check.completer().setCompletionMode(QCompleter.PopupCompletion)

        users = self.shotgrid.sg_users()

        self.shotgrid_user = QComboBox()
        self.shotgrid_user.setMinimumHeight(35)
        self.shotgrid_user.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.shotgrid_user.setEditable(True)
        for user in users:
            self.shotgrid_user.addItem(user["login"])
        self.shotgrid_user.setInsertPolicy(QComboBox.NoInsert)
        self.shotgrid_user.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.shotgrid_user.setCurrentText(self.shotgrid.user)

        self.open_rv_button = QPushButton("rv")
        self.open_rv_button.clicked.connect(self.evt_open_rv)
        self.open_nuke_button = QPushButton("nuke")
        self.open_nuke_button.clicked.connect(self.evt_open_nuke)

        self.files_layout = QHBoxLayout()
        self.files_layout.addWidget(self.software_select)
        self.files_layout.addWidget(self.shot_asset_check)
        self.files_layout.addWidget(self.work_publish_check)
        self.files_layout.addWidget(self.shotgrid_user)


        self.load_files_button = QPushButton("+ L O A D ")
        self.load_files_button.setFont(QFont( "System", 10 , QFont.ExtraLight))
        self.remove_file_button = QPushButton("R E M O V E")
        self.remove_file_button.setFont(QFont( "System", 10 , QFont.ExtraLight))
        self.clear_files_button = QPushButton("C L E A R")
        self.clear_files_button.setFont(QFont( "System", 10 , QFont.ExtraLight))
        self.managing_files_layout = QHBoxLayout()
        self.managing_files_layout.addWidget(self.clear_files_button,10)
        self.managing_files_layout.addWidget(self.remove_file_button,20)
        self.managing_files_layout.addWidget(self.load_files_button,70)


        self.files_list = QListWidget()

        self.model = QFileSystemModel()
        self.model.setNameFilterDisables(0)
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setColumnWidth(0,500)
        self.tree.setDragEnabled(True)
        self.tree.doubleClicked.connect(self.evt_get_value)


        self.files_info_label = QTextEdit()

        self.files_view_layout = QHBoxLayout()
        self.files_view_layout.addWidget(self.files_list,30)
        self.files_view_layout.addWidget(self.tree,70)

        self.files_open_layout = QVBoxLayout()
        self.files_open_layout.addWidget(self.open_nuke_button)
        self.files_open_layout.addWidget(self.open_rv_button)

        self.files_info_layout = QHBoxLayout()
        self.files_info_layout.addWidget(self.files_info_label,80)
        self.files_info_layout.addLayout(self.files_open_layout,20)

        self.main_files_layout = QVBoxLayout()
        self.main_files_layout.addLayout(self.files_layout,10)
        self.main_files_layout.addLayout(self.managing_files_layout,30)
        self.main_files_layout.addLayout(self.files_view_layout,50)
        self.main_files_layout.addLayout(self.files_info_layout,10)

        self.msg = QMessageBox() 
        self.msg.setIcon(QMessageBox.Warning) 
        self.msg.setWindowTitle("Warning") 

        self.files_space = QWidget()
        self.files_space.setLayout(self.main_files_layout)

        self.auto_render_plate_dropdown = QComboBox()
        self.auto_render_plate_dropdown.addItems(["plate01", "dn"])

        self.auto_undist_plate_dropdown = QComboBox()
        self.auto_undist_plate_dropdown.addItems(["plate01", "dn"])

        self.template_auto_render_button = QPushButton("A U T O - R E N D E R ")
        self.template_auto_render_button.clicked.connect(self.run_template_auto_render)
        self.template_auto_render_button.setMinimumHeight(150)

        self.template_auto_render_info  = QTextEdit()
        self.template_auto_render_info.setPlainText(
                """
                    PLATE 
                    

                    PLATE_TYPE



                """
                )
        self.integ_auto_undist_button = QPushButton("A U T O - U N D I S T ")
        self.integ_auto_undist_button.clicked.connect(self.run_integ_auto_undist)
        self.integ_auto_undist_button.setMinimumHeight(150)

        self.integ_auto_undist_info  = QTextEdit()
        self.integ_auto_undist_info.setPlainText(
                """
                    PLATE  
                    
                
                """
                )


        self.auto_render_layout = QHBoxLayout()
        self.auto_render_layout.addWidget(QLabel("P L A T E"),5)
        self.auto_render_layout.addWidget(self.auto_render_plate_dropdown,20)

        self.auto_undist_layout = QHBoxLayout()
        self.auto_undist_layout.addWidget(QLabel("P L A T E"),5)
        self.auto_undist_layout.addWidget(self.auto_undist_plate_dropdown,20)


        self.integ_files_layout = QVBoxLayout()
        self.integ_files_layout.addWidget(self.template_auto_render_button,10)
        self.integ_files_layout.addLayout(self.auto_render_layout,30)
        self.integ_files_layout.addWidget(self.template_auto_render_info,20)
        self.integ_files_layout.addWidget(self.integ_auto_undist_button,10)
        self.integ_files_layout.addLayout(self.auto_undist_layout,30)
        self.integ_files_layout.addWidget(self.integ_auto_undist_info,20)


        self.integ_space = QWidget()
        self.integ_space.setLayout(self.integ_files_layout)

        self.roto_paint_space = QWidget()
        self.comp_space = QWidget()
        self.cg_space = QWidget()

        self.space_tab_widget = QTabWidget()
        self.space_tab_widget.setStyleSheet("QTabBar::tab { height: 100px; width: 348px;}")
        self.space_tab_widget.setUsesScrollButtons(1)
        self.space_tab_widget.setMovable(1)
        self.space_tab_widget.addTab(self.files_space , "F I L E S")
        self.space_tab_widget.addTab(self.integ_space , "I N T E G R A T I O N")
        self.space_tab_widget.addTab(self.roto_paint_space , "R O T O  P A I N T")
        self.space_tab_widget.addTab(self.comp_space , "C O M P O S I T I N G")
        self.space_tab_widget.addTab(self.cg_space , "C G")


        self.market_layout = QVBoxLayout()
        self.market_layout.addWidget(self.space_tab_widget)
        self.setLayout(self.market_layout)

        self.load_files_button.clicked.connect(self.name_creator)
        self.remove_file_button.clicked.connect(self.evt_remove_file)
        self.clear_files_button.clicked.connect(self.evt_remove_files)
        self.files_list.currentTextChanged.connect(self.evt_get_files)


    def name_creator(self):
        try:

            work_type = self.work_publish_check.currentText()
            software_type = self.software_select.currentText()
            shot_asset_type = self.shot_asset_check.currentText()
            shotgrid_user_select = self.shotgrid_user.currentText()


            if work_type == "work":
                template = f"tk-{software_type}_{shot_asset_type}_work_area"
            else:
                template = f"{shot_asset_type}_publish_area"

            shot = self.env["shot"]
            seq = self.env["seq"]
            show = self.env["show"]
            step = self.env["step"]
            user = self.shotgrid_user.currentText()
            files = self.shotgrid.getFiles(template, show, user,  seq, shot, step )
            print("files",files)
            self.files_list.addItems(files)
        except Exception as e :
            self.msg.setText(f"setup show env and select shot , error detals {e}") 
            self.msg.exec_() 

    def template_auto_render_command(self):
        f"template_auto_render -p {self.auto_undist_plate_dropdown.currentText()} --seq {self.space_widget.dd_seq} --shot {self.space_widget.dd_shot} -tan integ_auto_render_template"

    def integ_auto_undist_command(self):
        pass

    def run_template_auto_render(self):
        print("INTEG $$$$$$$$$$$$$$$$$$$$ INTEG")
        print(self.template_auto_render_command())
        print(self.space_widget.folderlocation())
        subprocess.Popen( ["konsole", "--new-tab" ,"--workdir" , f"{self.space_widget.folderlocation()}" ,"-e", self.template_auto_render_command()])

    def run_integ_auto_undist(self):
        print("INTEG $$$$$$$$$$$$$$$$$$$$ INTEG")
        subprocess.Popen( ["konsole", "--new-tab" ,"--workdir" , f"{self.space_widget.folderlocation()}" ,"-e", f"{self.integ_auto_undist_command()}"])


    def evt_get_files(self, value):
        self.model.setRootPath(value)
        self.tree.setRootIndex(self.model.index(value))



    def evt_remove_file(self):
        removeList = self.files_list.selectedItems()
        if not removeList :
            self.msg.setText("nothing is selected") 
            self.msg.exec_() 
        else:
            self.files_list.takeItem(self.files_list.row(removeList[0]))

    def evt_remove_files(self):
        self.files_list.clear()

    def evt_get_value(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        self.fileName = self.model.fileName(indexItem)
        self.filePath = self.model.filePath(indexItem)
        self.files_info_label.setText(self.filePath)

    def evt_open_rv(self):
        try:
            if self.filePath is not None:
                utils.open_rv_file(self.filePath)
        except:
            self.msg.setText("No file selected") 
            self.msg.exec_() 

    def evt_open_nuke(self):
        try:
            if self.filePath is not None:
                utils.open_nuke_file(self.filePath)
        except:
            self.msg.setText("No file selected") 
            self.msg.exec_() 




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarketWidget()
    window.show()
    sys.exit(app.exec_())



