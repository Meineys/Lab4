import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QColor, QPolygonF
from PyQt6.QtCore import Qt, QPointF
from PyQt6 import uic

class Task3(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("task3.ui", self)
        self.shapes = []
        self.cursor_pos = None

    def mousePressEvent(self, event):
        color = QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        size = random.randint(20, 100)
        if event.button() == Qt.MouseButton.LeftButton:
            self.shapes.append(('circle', event.pos().x(), event.pos().y(), size, color))
        elif event.button() == Qt.MouseButton.RightButton:
            self.shapes.append(('square', event.pos().x(), event.pos().y(), size, color))
        self.update()

    def mouseMoveEvent(self, event):
        self.cursor_pos = event.pos()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space and self.cursor_pos:
            color = QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            size = random.randint(20, 100)
            self.shapes.append(('triangle', self.cursor_pos.x(), self.cursor_pos.y(), size, color))
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for shape, x, y, size, color in self.shapes:
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            if shape == 'circle':
                painter.drawEllipse(x - size//2, y - size//2, size, size)
            elif shape == 'square':
                painter.drawRect(x - size//2, y - size//2, size, size)
            elif shape == 'triangle':
                points = [(x, y - size//2), (x - size//2, y + size//2), (x + size//2, y + size//2)]
                poly = QPolygonF([QPointF(px, py) for px, py in points])
                painter.drawPolygon(poly)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Task3()
    w.setMouseTracking(True)
    w.centralwidget.setMouseTracking(True)
    w.show()
    sys.exit(app.exec())
