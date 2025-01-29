
api.load("pymongo")

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QCompleter
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QLinearGradient

from pymongo import MongoClient, DESCENDING, ASCENDING
from datetime import datetime, timedelta
import utils

# Pagination parameters
items_per_page = 20
current_page = 1
## ==> GLOBALS
counter = 0
show = os.environ["DD_SHOW"]

class Timesheet(QWidget):
    def __init__(self):
        super().__init__()

        self.connection = MongoClient("",) # chnage to your client
        self.database = self.connection['ddConnect']
        self.collection = self.database['time_data']
        self.initUI()

    def initUI(self):


        self.user = self.database['users']
        self.project = self.database["projects"]
        self.department = self.database["departments"]
        self.use_list = self.user.distinct("login", {})

        users_list = self.user.distinct("login", {})
        projects_list = self.project.distinct("name", {})
        departments_list = self.department.distinct("name", {})

        self.projectLabel = QLabel('Project:')
        self.projectLabel.setMinimumSize(100, 50)
        self.projectLabel.setAlignment(Qt.AlignCenter)
        self.projectLineEdit = QComboBox()
        self.projectLineEdit.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.projectLineEdit.setEditable(True)
        self.projectLineEdit.setInsertPolicy(QComboBox.NoInsert)
        self.projectLineEdit.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.projectLineEdit.clear()
        self.projectLineEdit.addItem("")
        self.projectLineEdit.setMinimumSize(200, 50)
        self.projectLineEdit.addItems(projects_list)
        self.projectLineEdit.setCurrentText(show)

        self.taskLabel = QLabel('Task:')
        self.taskLabel.setMinimumSize(100, 50)
        self.taskLabel.setAlignment(Qt.AlignCenter)

        self.departmentLabel = QLabel('Department:')
        self.departmentLabel.setMinimumSize(100, 50)
        self.departmentLabel.setAlignment(Qt.AlignCenter)

        self.departmentLineEdit = QComboBox()
        self.departmentLineEdit.setStyleSheet(
            "QComboBox { combobox-popup: 0; }")
        self.departmentLineEdit.setEditable(True)
        self.departmentLineEdit.setInsertPolicy(QComboBox.NoInsert)
        self.departmentLineEdit.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.departmentLineEdit.clear()
        self.departmentLineEdit.addItem("")
        self.departmentLineEdit.setMinimumSize(200, 50)
        self.departmentLineEdit.addItems(departments_list)

        self.userLabel = QLabel('User:')
        self.userLabel.setMinimumSize(100, 50)
        self.userLabel.setAlignment(Qt.AlignCenter)

        self.userLineEdit = QComboBox()
        self.userLineEdit.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.userLineEdit.setEditable(True)
        self.userLineEdit.setInsertPolicy(QComboBox.NoInsert)
        self.userLineEdit.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.userLineEdit.clear()
        self.userLineEdit.addItem("")
        self.userLineEdit.setMinimumSize(200, 50)
        self.userLineEdit.addItems(users_list)

        self.current_day = datetime.now().strftime("%Y:%m:%d")

        self.dateLabel = QLabel('Date:')
        self.dateLabel.setMinimumSize(100, 50)
        self.dateLabel.setAlignment(Qt.AlignCenter)

        self.dateLineEdit = QLineEdit()
        self.dateLineEdit.setText(self.current_day)
        self.dateLineEdit.setMinimumSize(100, 50)

        self.dateLineEdit.returnPressed.connect(self.search)
        self.userLineEdit.activated.connect(self.search)
        self.projectLineEdit.activated.connect(self.search)
        self.departmentLineEdit.activated.connect(self.search)

        self.refresh = QPushButton('Refresh')
        self.refresh.pressed.connect(self.search_all)

        self.next_button = QPushButton("Next")
        self.next_button.setShortcut(Qt.Key_Right)
        self.prev_button = QPushButton("Previous")
        self.prev_button.setShortcut(Qt.Key_Left)
        self.page_button = QPushButton(str(current_page))
        self.page_button.clicked.connect(self.show_first_page)

        self.next_button.clicked.connect(self.show_next_page)
        self.prev_button.clicked.connect(self.show_previous_page)

        self.tableWidget = QTableWidget()

        self.tableWidget.setColumnCount(8)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 276)
        self.tableWidget.setColumnWidth(5, 400)
        self.tableWidget.setColumnWidth(6, 150)
        self.tableWidget.setColumnWidth(7, 276)

        self.tableWidget.setHorizontalHeaderLabels(
            ['Name', 'Date', 'Day', 'Projects', 'Tasks', 'Department', 'System Id', 'Status'])


        # Create the layout
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.projectLabel)
        hbox1.addWidget(self.projectLineEdit)
        hbox1.addWidget(self.departmentLabel)
        hbox1.addWidget(self.departmentLineEdit)
        hbox1.addWidget(self.userLabel)
        hbox1.addWidget(self.userLineEdit)
        hbox1.addWidget(self.dateLabel)
        hbox1.addWidget(self.dateLineEdit)
        hbox1.addWidget(self.refresh)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.tableWidget)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.prev_button)
        hbox3.addWidget(self.page_button)
        hbox3.addWidget(self.next_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)
        self.results_data(current_page)
        self.show()

    def results_data(self, page_num, query={}):
        # Execute the search query
        skip_items = (page_num - 1) * items_per_page
        
        self.data = []
        self.results = self.collection.find(query)

        for document in self.results:
            self.data.append(document)

        # self.results = self.collection.find(query).sort("date", DESCENDING)
        self.results = self.collection.find(query).skip(
            skip_items).limit(items_per_page).sort([("date", DESCENDING), ("login", 1)])

        # Display the results in the table widget
        self.tableWidget.setRowCount(0)
        for row, result in enumerate(self.results):

            projects = '\n'.join(result['project'])
            x = utils.get_still_working(result)
            task_data = str()
            for key in result['task']:
                task_data += key + ":" + result['task'][key] + "\n"
            self.tableWidget.insertRow(row)
            self.tableWidget.setRowHeight(row, 70)
            department_align = QTableWidgetItem(
                result['department'])
            department_align.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(
                row, 5, QTableWidgetItem(department_align))

            user_id_align = QTableWidgetItem(result['login'])
            user_id_align.setTextAlignment(Qt.AlignCenter)

            self.tableWidget.setItem(row, 0, user_id_align)

            date_align = QTableWidgetItem(result['date'])
            date_align.setTextAlignment(Qt.AlignCenter)

            self.tableWidget.setItem(
                row, 1, QTableWidgetItem(date_align))

            day_align = QTableWidgetItem(result['day'])
            day_align.setTextAlignment(Qt.AlignCenter)

            self.tableWidget.setItem(
                row, 2, QTableWidgetItem(day_align))

            self.tableWidget.setItem(row, 3, QTableWidgetItem(projects))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(task_data))

            system_id_align = QTableWidgetItem(result['system_id'])
            system_id_align.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(
                row, 6, system_id_align)

            self.tableWidget.setItem(
                row, 7, QTableWidgetItem(x))
            item = QTableWidgetItem(x)
            if x == 'Available':
                gradient = QLinearGradient(0, 0, 0, 1)
                gradient.setStart(0, 10)
                gradient.setFinalStop(0, 90)
                gradient.setColorAt(0, QColor(33, 188, 86))
                gradient.setColorAt(1, QColor(164, 216, 158))
                item.setBackground(gradient)
                item.setTextAlignment(Qt.AlignCenter)
            else:
                gradient = QLinearGradient(0, 0, 0, 1)
                gradient.setStart(0, 10)
                gradient.setFinalStop(0, 90)
                gradient.setColorAt(0, QColor(188, 98, 86))
                gradient.setColorAt(1, QColor(216, 164, 158))
                item.setBackground(gradient)
                item.setTextAlignment(Qt.AlignCenter)

            self.tableWidget.setItem(row, 7, item)

    def show_first_page(self):
        global current_page
        current_page = 1
        self.page_button.setText(str(current_page))
        self.search()

    def show_next_page(self):
        global current_page
        current_page += 1
        self.page_button.setText(str(current_page))
        self.search()

    def show_previous_page(self):
        global current_page
        if current_page > 1:
            current_page -= 1
            self.page_button.setText(str(current_page))
            self.search()

    def search_all(self):

        self.projectLineEdit.setCurrentIndex(0)
        self.userLineEdit.setCurrentIndex(0)
        self.departmentLineEdit.setCurrentIndex(0)
        query = {}
        self.results_data(current_page, query)

    def search(self):
        # Get the search criteria
        project = self.projectLineEdit.currentText()
        user = self.userLineEdit.currentText()
        date_str = self.dateLineEdit.text()
        department = self.departmentLineEdit.currentText()

        # Build the search query
        query = {}
        if project:
            query['project'] = project
        if user:
            query['login'] = user
        if date_str:
            query['date'] = date_str
        if department:
            query['department'] = department

        self.results_data(current_page, query)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Timesheet()
    ex.show()
    sys.exit(app.exec_())
