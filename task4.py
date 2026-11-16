import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6 import uic

class HoverButton(QPushButton):
    def enterEvent(self, event):
        super().enterEvent(event)
        pw = self.parentWidget().width() - self.width()
        ph = self.parentWidget().height() - self.height()
        if pw > 0 and ph > 0:
            self.move(random.randint(0, pw), random.randint(0, ph))

class Task4(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task4.ui", self)
        self.new_btn = HoverButton(self.btn.text(), self.centralwidget)
        self.new_btn.setGeometry(self.btn.geometry())
        self.btn.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Task4()
    w.show()
    sys.exit(app.exec())
