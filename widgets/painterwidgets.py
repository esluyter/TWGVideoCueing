"""
Custom painter widgets for TWG video cueing

- LevelMeter

Author: Eric Sluyter
Last edited: July 2018
"""

import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import QPoint, QSize, QRect


class LevelMeter(QWidget):
    def __init__(self):
        super().__init__()
        self.pen = QPen(QColor(0, 0, 0, 0))
        self.pen.setWidth(0)
        self.left_db = -60
        self.right_db = -60
        self.gap = 5

    def set_dbs(self, l, r):
        self.left_db = l
        self.right_db = r
        self.update()

    def set_left_db(self, db):
        self.left_db = db
        self.update()

    def set_right_db(self, db):
        self.right_db = db
        self.update()

    def set_gap(self, gap):
        self.gap = gap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)

        left_height = ((self.left_db + 60) / 70) * self.height()
        right_height = ((self.right_db + 60) / 70) * self.height()

        left = QRect(QPoint(0, self.height() - left_height),
            QSize((self.width() - self.gap) / 2, left_height))
        right = QRect(QPoint((self.width() + self.gap) / 2, self.height() - right_height),
            QSize((self.width() - self.gap) / 2, right_height))

        painter.setBrush(QBrush(QColor(0, 200, 100, 255)))
        painter.drawRect(left)
        painter.drawRect(right)
