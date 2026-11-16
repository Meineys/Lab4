import sys
import sqlite3
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
from PyQt6 import uic

class EditDialog(QDialog):
    def __init__(self, parent=None, film_id=None):
        super().__init__(parent)
        uic.loadUi("task2_dialog.ui", self)
        self.film_id = film_id
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)
        self.load_genres()
        if self.film_id:
            self.load_film()

    def load_genres(self):
        conn = sqlite3.connect("films_db.sqlite")
        c = conn.cursor()
        c.execute("SELECT id, title FROM genres")
        for r in c.fetchall():
            self.genre_cb.addItem(r[1], r[0])
        conn.close()

    def load_film(self):
        conn = sqlite3.connect("films_db.sqlite")
        c = conn.cursor()
        c.execute("SELECT title, year, genre, duration FROM films WHERE id=?", (self.film_id,))
        res = c.fetchone()
        conn.close()
        if res:
            self.title_edit.setText(res[0])
            self.year_spin.setValue(res[1])
            self.duration_spin.setValue(res[3])
            idx = self.genre_cb.findData(res[2])
            if idx >= 0:
                self.genre_cb.setCurrentIndex(idx)

    def save(self):
        t = self.title_edit.text()
        y = self.year_spin.value()
        d = self.duration_spin.value()
        g = self.genre_cb.currentData()
        if not t:
            QMessageBox.warning(self, "Ошибка", "Название пустое!")
            return
        if d < 0:
            QMessageBox.warning(self, "Ошибка", "Отрицательная длина!")
            return
        if y > datetime.datetime.now().year:
            QMessageBox.warning(self, "Ошибка", "Год в будущем!")
            return
        conn = sqlite3.connect("films_db.sqlite")
        c = conn.cursor()
        if self.film_id:
            c.execute("UPDATE films SET title=?, year=?, genre=?, duration=? WHERE id=?", (t, y, g, d, self.film_id))
        else:
            c.execute("INSERT INTO films (title, year, genre, duration) VALUES (?, ?, ?, ?)", (t, y, g, d))
        conn.commit()
        conn.close()
        self.accept()

class Task2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task2.ui", self)
        self.add_btn.clicked.connect(self.add_film)
        self.edit_btn.clicked.connect(self.edit_film)
        self.del_btn.clicked.connect(self.del_film)
        self.update_table()

    def update_table(self):
        conn = sqlite3.connect("films_db.sqlite")
        c = conn.cursor()
        c.execute("SELECT films.id, films.title, films.year, genres.title, films.duration FROM films LEFT JOIN genres ON films.genre = genres.id")
        rows = c.fetchall()
        names = [description[0] for description in c.description]
        self.tableWidget.setColumnCount(len(names))
        self.tableWidget.setHorizontalHeaderLabels(names)
        self.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        conn.close()

    def add_film(self):
        if EditDialog(self).exec():
            self.update_table()

    def edit_film(self):
        r = self.tableWidget.currentRow()
        if r < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись!")
            return
        fid = int(self.tableWidget.item(r, 0).text())
        if EditDialog(self, fid).exec():
            self.update_table()

    def del_film(self):
        r = self.tableWidget.currentRow()
        if r < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись!")
            return
        fid = int(self.tableWidget.item(r, 0).text())
        conn = sqlite3.connect("films_db.sqlite")
        c = conn.cursor()
        c.execute("DELETE FROM films WHERE id=?", (fid,))
        conn.commit()
        conn.close()
        self.update_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Task2()
    ex.show()
    sys.exit(app.exec())
