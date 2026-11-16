import sys
import sqlite3
import hashlib
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6 import uic

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("task6_login.ui", self)
        self.login_btn.clicked.connect(self.login)
        self.reg_btn.clicked.connect(self.register)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect("library.sqlite")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, login TEXT UNIQUE, pwd TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, genre TEXT, img TEXT)")
        conn.commit()
        conn.close()

    def login(self):
        l = self.login_edit.text()
        p = self.pass_edit.text()
        conn = sqlite3.connect("library.sqlite")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE login=? AND pwd=?", (l, hash_pw(p)))
        if c.fetchone():
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные данные")
        conn.close()

    def register(self):
        l = self.login_edit.text()
        p = self.pass_edit.text()
        if not l or not p: return
        conn = sqlite3.connect("library.sqlite")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (login, pwd) VALUES (?, ?)", (l, hash_pw(p)))
            conn.commit()
            QMessageBox.information(self, "Успех", "Зарегистрирован")
        except:
            QMessageBox.warning(self, "Ошибка", "Логин занят")
        conn.close()

class BookDialog(QDialog):
    def __init__(self, parent=None, bid=None):
        super().__init__(parent)
        uic.loadUi("task6_dialog.ui", self)
        self.bid = bid
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)
        if self.bid:
            self.load_data()

    def load_data(self):
        conn = sqlite3.connect("library.sqlite")
        c = conn.cursor()
        c.execute("SELECT title, author, year, genre, img FROM books WHERE id=?", (self.bid,))
        res = c.fetchone()
        if res:
            self.title_edit.setText(res[0])
            self.author_edit.setText(res[1])
            self.year_spin.setValue(res[2])
            self.genre_edit.setText(res[3])
            self.img_edit.setText(res[4])
        conn.close()

    def save(self):
        t = self.title_edit.text()
        a = self.author_edit.text()
        y = self.year_spin.value()
        g = self.genre_edit.text()
        i = self.img_edit.text()
        conn = sqlite3.connect("library.sqlite")
        c = conn.cursor()
        if self.bid:
            c.execute("UPDATE books SET title=?, author=?, year=?, genre=?, img=? WHERE id=?", (t, a, y, g, i, self.bid))
        else:
            c.execute("INSERT INTO books (title, author, year, genre, img) VALUES (?, ?, ?, ?, ?)", (t, a, y, g, i))
        conn.commit()
        conn.close()
        self.accept()

class Task6(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task6_main.ui", self)
        self.add_btn.clicked.connect(self.add_b)
        self.edit_btn.clicked.connect(self.edit_b)
        self.del_btn.clicked.connect(self.del_b)
        self.search_edit.textChanged.connect(self.update_table)
        self.search_cb.currentTextChanged.connect(self.update_table)
        self.tableWidget.itemSelectionChanged.connect(self.show_img)
        self.update_table()

    def update_table(self):
        st = self.search_edit.text()
        mode = self.search_cb.currentText()
        conn = sqlite3.connect("library.sqlite")
        c = conn.cursor()
        if mode == "По автору":
            c.execute("SELECT id, title, author, year, genre, img FROM books WHERE author LIKE ?", (f"%{st}%",))
        else:
            c.execute("SELECT id, title, author, year, genre, img FROM books WHERE title LIKE ?", (f"%{st}%",))
        self.rows = c.fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Автор", "Год", "Жанр"])
        self.tableWidget.setRowCount(len(self.rows))
        for i, row in enumerate(self.rows):
            for j in range(5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row[j])))
        conn.close()

    def show_img(self):
        r = self.tableWidget.currentRow()
        if r >= 0 and r < len(self.rows):
            img_path = self.rows[r][5]
            pix = QPixmap(img_path)
            if pix.isNull():
                pix = QPixmap("default.png")
            self.img_label.setPixmap(pix)

    def add_b(self):
        if BookDialog(self).exec(): self.update_table()

    def edit_b(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        bid = int(self.tableWidget.item(r, 0).text())
        if BookDialog(self, bid).exec(): self.update_table()

    def del_b(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        bid = int(self.tableWidget.item(r, 0).text())
        conn = sqlite3.connect("library.sqlite")
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id=?", (bid,))
        conn.commit()
        conn.close()
        self.update_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth = AuthDialog()
    if auth.exec():
        ex = Task6()
        ex.show()
        sys.exit(app.exec())
