"""
Custom little widgets for TWG video cueing

- QHLine
- QNumberBox

Author: Eric Sluyter
Last edited: July 2018
"""

from PyQt5.QtWidgets import QFrame, QLineEdit
from PyQt5.QtGui import QValidator, QDoubleValidator, QColor, QPalette
from PyQt5.QtCore import pyqtSignal, Qt


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        #self.setFrameShadow(QFrame.Sunken)

class QNumberBox(QLineEdit):
    valueChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.editedTextColor = QColor('red')
        self.normalTextColor = QColor('black')

        self.scroll = True

        self.step = 0.1
        self.dragDist = 1.0

        self.lastPos = 0

        validator = QDoubleValidator(self)
        validator.setDecimals(2)
        self.setValidator(validator)

        self.valueChanged.connect(self.updateText)
        self.editingFinished.connect(self.onEditingFinished)

        self.setValue(0)

    def setValue(self, val):
        validator = self.validator()
        if val > validator.top():
            val = validator.top()
        if val < validator.bottom():
            val = validator.bottom()
        val = self.roundedVal(val)
        if (int(val) == val):
            val = int(val)
        self.value = val
        self.valueChanged.emit()

    def increment(self, factor=1):
        if not self.isReadOnly():
            return
        self.setValue(self.value + (self.step * factor))

    def decrement(self, factor=1):
        if not self.isReadOnly():
            return
        self.setValue(self.value - (self.step * factor))

    def onEditingFinished(self):
        if self.isReadOnly():
            return
        res = self.locale().toDouble(self.text())[0]
        self.setValue(res)

    def setMinimum(self, min):
        self.validator().setBottom(min)
        self.setValue(self.value)

    def setMaximum(self, max):
        self.validator().setTop(max)
        self.setValue(self.value)

    def setDecimals(self, d):
        if d < 0:
            return
        self.validator().setDecimals(d)
        self.setValue(self.value)

    def roundedVal(self, val):
        return round(val, self.validator().decimals())

    def updateText(self):
        self.blockSignals(True)
        self.setText(str(self.value))
        self.setCursorPosition(0)
        self.setLocked(True)
        self.blockSignals(False)

    def setLocked(self, locked):
        if locked:
            self.setReadOnly(True)
            self.setSelection(0, 0)
        else:
            self.setReadOnly(False)
        self.updateTextColor()

    def setTextColor(self, c):
        if (c.isValid()):
            self.normalTextColor = c
            self.updateTextColor()

    def setEditedTextColor(self, c):
        if (c.isValid()):
            self.editedTextColor = c
            self.updateTextColor()

    def updateTextColor(self):
        p = self.palette()
        p.setColor(QPalette.Text, self.normalTextColor if self.isReadOnly() else
            self.editedTextColor)
        self.setPalette(p)

    def keyPressEvent(self, event):
        if not self.isReadOnly():
            return QLineEdit.keyPressEvent(self, event)

        key = event.key()

        if key == Qt.Key_Up:
            self.increment()
            return
        elif key == Qt.Key_Down:
            self.decrement()
            return
        else:
            t = event.text()
            i = 0
            if t != '' and self.validator().validate(t, i)[0] != QValidator.Invalid:
                self.blockSignals(True)
                self.clear()
                self.blockSignals(False)
                self.setLocked(False)

        QLineEdit.keyPressEvent(self, event)

    def mousePressEvent(self, event):
        self.lastPos = event.globalY()
        if self.isReadOnly():
            return
        QLineEdit.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.scroll and self.isReadOnly() and (event.buttons() & Qt.LeftButton):
            steps = (event.globalY() - self.lastPos) / self.dragDist
            if steps != 0:
                self.lastPos = self.lastPos + (steps * self.dragDist)
                self.increment(-steps)
        else:
            QLineEdit.mouseMoveEvent(self, event)
