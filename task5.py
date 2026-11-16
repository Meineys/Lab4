import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6 import uic

class Task5(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task5.ui", self)
        self.step = 10

    def keyPressEvent(self, event):
        x = self.ufo.x()
        y = self.ufo.y()
        w = self.centralwidget.width()
        h = self.centralwidget.height()
        if event.key() == Qt.Key.Key_Left: x -= self.step
        elif event.key() == Qt.Key.Key_Right: x += self.step
        elif event.key() == Qt.Key.Key_Up: y -= self.step
        elif event.key() == Qt.Key.Key_Down: y += self.step
        
        if x < -self.ufo.width(): x = w
        elif x > w: x = -self.ufo.width()
        if y < -self.ufo.height(): y = h
        elif y > h: y = -self.ufo.height()
        
        self.ufo.move(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Task5()
    w.show()
    sys.exit(app.exec())
