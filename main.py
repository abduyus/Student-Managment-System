from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        self.setFixedWidth(500)
        self.setFixedHeight(400)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)
        
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_action = QAction("Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().hide()
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
    
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(400)

        layout = QVBoxLayout()

        # Add search name box widget
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Name:")
        layout.addWidget(self.search_box)

        # Add search button
        search_button = QPushButton("Search")
        # search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Computing" , "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        self.setLayout(layout)

        # Add mobile number widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = Mainwindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())