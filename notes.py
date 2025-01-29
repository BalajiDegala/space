
from PyQt5.QtWidgets import QApplication,QSizePolicy,QScrollArea, QLabel,QHBoxLayout, QVBoxLayout, QWidget, QTableWidget, QAbstractItemView , QTableWidgetItem, QPushButton , QTextEdit
from PyQt5.QtGui import QFont,QIcon,QPixmap
from PyQt5.QtCore import QSize,Qt
import sys
import utils 
import subprocess
from ddshotgrid import DDShotgun
import os
import fnmatch

class NotesWidget(QWidget):
    def __init__(self, shot_id= None):
        super().__init__()
        self.shot_id = shot_id
        self.shotgrid = DDShotgun()
        self.notes_table = QTableWidget()
        self.notes_table.setColumnCount(6)
        self.notes_table.setHorizontalHeaderLabels(["Subject", "Review", "Annotations", "Type", "Project", "Date Updated"])

        self.notes_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.notes_table.horizontalHeader().setStretchLastSection(True)

        self.load_notes_button = QPushButton("+ A N N O T A T I O N S")
        self.load_notes_button.setFont(QFont( "System", 10 , QFont.ExtraLight))
        self.load_notes_button.setShortcut("F5")
        self.load_notes_button.clicked.connect(self.load_notes)

        notes_layout = QVBoxLayout()
        notes_layout.addWidget(self.load_notes_button)
        notes_layout.addWidget(self.notes_table)


        self.setLayout(notes_layout)


    def load_notes(self):
        try:
            if self.shot_id is not None:
                filters = [["note_links", "is", {"type": "Shot", "id": self.shot_id}],["sg_client_note_id",'is_not',None]]
                fields = ["tasks", "content", "sg_note_type",  "attachments", "updated_at", "project"]
                notes_assigned = self.shotgrid.sg.find("Note", filters, fields)
                notes_assigned = notes_assigned[::-1]
                self.notes_table.setRowCount(len(notes_assigned))

                for i, notes in enumerate(notes_assigned):
                    if notes["project"] != []:
                        self.show = notes["project"]["name"]

                    if notes["tasks"] != []:
                        self.notes_table.setItem(i,0,QTableWidgetItem(str(notes["tasks"][0]["name"])))
                    annotation_subject = QTextEdit()
                    annotation_subject.setText(notes["content"])
                    self.notes_table.setCellWidget(i, 1, annotation_subject)
                    if notes["attachments"] != []:
                        label_widget = QWidget(self)
                        label_layout = QVBoxLayout(label_widget)
                        for j in range(len(notes["attachments"])):
                            self.getTask_name = notes["attachments"][j]['name']
                            self.img = self.get_file()
                            j = QLabel()
                            piximg = QPixmap(self.img)
                            piximg = piximg.scaled(1300,1000,Qt.KeepAspectRatio)
                            j.setPixmap(piximg)
                            label_layout.addWidget(j)
                            scroll_area = QScrollArea(self) 
                            scroll_area.setWidgetResizable(True) 
                            scroll_area.setWidget(label_widget) 
                            scroll_area.setMinimumSize(1350,1000)

                    else :
                        scroll_area = QWidget()
                        labeling = QLabel()
                        labeling.setText("N/A")
                        label_layout = QVBoxLayout()
                        label_layout.addWidget(labeling)
                        scroll_area.setLayout(label_layout)
                    self.notes_table.setCellWidget(i, 2, scroll_area)

                    item = QTableWidgetItem(str(notes["sg_note_type"]))
                    utils.color_look_notes(item, notes )
                    self.notes_table.setItem(i, 3, item)
                    self.notes_table.setItem(i, 4, QTableWidgetItem(str(notes["project"]["name"])))

                    date = notes["updated_at"]

                    self.notes_table.setItem(i, 5, QTableWidgetItem(str(date)[:10]))

                    self.notes_table.resizeRowsToContents()
                    self.notes_table.resizeColumnsToContents()
        except Exception as e:
            print("error in task selection or ", e)
    

    
    def get_file(self):
        path = f"" # change as per you dir
        try:
            # This is my path
            val = ""
            for dirpath, dirnames, filenames in os.walk(path):
                for name in filenames:
                    if fnmatch.fnmatch(name, self.getTask_name):
                        val = dirpath +"/"+ name
            return val
        except Exception as e:
            print(e)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotesWidget()
    window.show()
    sys.exit(app.exec_())

        
