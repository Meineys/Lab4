import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.QtGui import QColor
from PyQt6 import uic

class Task1(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task1.ui", self)
        self.data = []
        self.schools = set()
        self.classes = set()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Логин", "ФИО", "Суммарный балл"])
        self.load_data()
        self.school_cb.currentTextChanged.connect(self.update_table)
        self.class_cb.currentTextChanged.connect(self.update_table)
        self.update_table()

    def load_data(self):
        try:
            with open('rez.csv', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 8:
                        login = row[2]
                        parts = login.split('-')
                        school = parts[2] if len(parts) > 2 else ""
                        cls = parts[3] if len(parts) > 3 else ""
                        self.data.append({'login': login, 'name': row[1], 'score': int(row[7]), 'school': school, 'cls': cls})
                        self.schools.add(school)
                        self.classes.add(cls)
        except:
            pass
        self.school_cb.addItem("Все")
        self.school_cb.addItems(sorted(list(self.schools)))
        self.class_cb.addItem("Все")
        self.class_cb.addItems(sorted(list(self.classes)))

    def update_table(self):
        s_filter = self.school_cb.currentText()
        c_filter = self.class_cb.currentText()
        filtered = []
        for d in self.data:
            if s_filter != "Все" and d['school'] != s_filter: continue
            if c_filter != "Все" and d['cls'] != c_filter: continue
            filtered.append(d)
        scores = sorted(list(set([d['score'] for d in filtered])), reverse=True)
        top3 = scores[:3]
        colors = {0: QColor(255, 215, 0), 1: QColor(192, 192, 192), 2: QColor(205, 127, 50)}
        self.tableWidget.setRowCount(len(filtered))
        for i, d in enumerate(filtered):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(d['login']))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(d['name']))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(d['score'])))
            if d['score'] in top3:
                c = colors[top3.index(d['score'])]
                for j in range(3):
                    self.tableWidget.item(i, j).setBackground(c)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Task1()
    ex.show()
    sys.exit(app.exec())
