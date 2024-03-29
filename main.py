import json
import os
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QGroupBox, QRadioButton,
    QPushButton, QLabel, QListWidget, QLineEdit, QColorDialog, QMessageBox)
from instr import *


path_json_records = "record.json"


class MainWin(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.set_appear()

        self.show()

        self.first_power()

        self.setAllrecords()

    def initUI(self):
        self.layout_line = QVBoxLayout()
        self.label_date = QLabel()
        self.line_search = QLineEdit()

        self.line_name = QLineEdit()
        self.layout_line.addWidget(self.line_name)
        self.line_name.setPlaceholderText("Введите текст сюда")
        
        self.list_widget = QListWidget() 
        self.layout_line.addWidget(self.list_widget)

        self.btn_record_add = QPushButton('Добавить запись')
        self.btn_record_add.clicked.connect(self.add_record)

        self.btn_record_rem = QPushButton('Удалить запись')
        self.btn_record_rem.clicked.connect(self.rem_record)

        self.btn_list_clear = QPushButton('Очистить список')
        self.btn_list_clear.clicked.connect(self.list_clear)

        self.btn_color = QPushButton('Выбрать цвет')
        self.btn_color.clicked.connect(self.choose_color)
        
        self.line_search.setPlaceholderText("Поиск записи")


        self.layout_line.addWidget(self.btn_record_add)
        self.layout_line.addWidget(self.btn_record_rem)
        self.layout_line.addWidget(self.btn_list_clear)
        self.layout_line.addWidget(self.label_date)
        self.layout_line.addWidget(self.line_search)
        self.layout_line.addWidget(self.btn_color)

        self.setLayout(self.layout_line)

    def setAllrecords(self):
        records = self.load_records(path_json_records)
        for record in records:
            self.list_widget.addItem(record)


    def choose_color(self):
        try:
            color = QColorDialog.getColor()
            if color.isValid():
                self.list_widget.currentItem().setBackground(QColor(color))
        except:
            pass

    def list_clear(self):

        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Warning)
        # setting message for Message Box 
        msg.setText("Внимание!!!\nВы точно хотите удалить все заметки?")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # start the app 
        msg.exec_()
        if msg.clickedButton().text() == 'OK':
            self.list_widget.clear()
            session = []
            with open(path_json_records, "w") as file:
                json.dump(session, file)


    def search_record(self):
        search_text = self.line_search.text()
        items = self.list_widget.findItems(search_text, Qt.MatchContains)
        if items:
            item = items[0]
            self.list_widget.setCurrentItem(item)

    def add_record(self):
        record_text = self.line_name.text()
        if record_text:
            current_datetime = QDateTime.currentDateTime()
            record_with_date = f"{record_text} ({current_datetime.toString(Qt.ISODate)})"
            self.list_widget.addItem(record_with_date)
            self.line_name.clear()

            records = self.load_records(path_json_records)
            records.append(record_with_date)
            self.save_records(path_json_records, records)

    def rem_record(self):
        try:
            remove_item = self.list_widget.currentItem()
            confirmation = ("Вы точно хотите удалить запись?")
            if confirmation:
                self.list_widget.takeItem(self.list_widget.row(remove_item))
                records = self.load_records(path_json_records)
                records.remove(remove_item.text())
                self.save_records(path_json_records, records)
        except:
            pass

    def set_appear(self):
        self.setWindowTitle(title)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)



    def first_power(self):
        if os.path.isfile(path_json_records):
            print("файл есть")
        else:
            session = []
            with open(path_json_records, "w") as file:
                json.dump(session, file)



    def load_records(self, filename):
        with open(filename, "r") as file:
            records = json.load(file)
        return records

    def save_records(self, filename, records):
        with open(path_json_records, "w") as file:
            json.dump(records, file)

records = [
  {
    "question":"Сам вопрос непосредственно",
    "answer_right": "Правельный ответ",
    "answer_1": "Не правельный ответ"
  },
  {
    "question":"Сам вопрос непосредственно",
    "answer_right": "Правельный ответ",
    "answer_1": "Не правельный ответ"
  },
  {
    "question":"Сам вопрос непосредственно",
    "answer_right": "Правельный ответ",
    "answer_1": "Не правельный ответ"
  },
  {
    "question":"Сам вопрос непосредственно",
    "answer_right": "Правельный ответ",
    "answer_1": "Не правельный ответ"
  }
]



app = QApplication([])
mw = MainWin()
app.exec_()