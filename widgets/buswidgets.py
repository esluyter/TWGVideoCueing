"""
Custom compound widgets for bus panel

- CueMediaWidget
- CuePositionWidget
- CueZoomWidget
- CueSpeedWidget
- CueVolumeWidget

Author: Eric Sluyter
Last edited: July 2018
"""

from widgets.fonts import UIFonts
from widgets.littlewidgets import QNumberBox
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QSlider, QLabel,
    QHBoxLayout, QVBoxLayout, QSizePolicy)
from PyQt5.QtCore import Qt


class CueMediaWidget(QWidget):
    def set_media_info(self, media_info):
        self.media_items = [str(k) + ' - ' + v.name for k, v in media_info.items()]
        self.media_indexes = list(media_info.keys())
        self.refreshMedia()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.media_items = ['0 - BLANK']
        self.media_indexes = [0]

        self.initUI()
        self.setValue(None)

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Media')
        label.setFont(UIFonts.label_font)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        self.check = QCheckBox()
        self.media_num = QComboBox()
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sp.setRetainSizeWhenHidden(True)
        self.media_num.setSizePolicy(sp)
        hbox.addWidget(self.check)
        hbox.addWidget(self.media_num)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.refreshMedia()

        self.check.stateChanged.connect(self.showNumBox)

    def refreshMedia(self):
        self.media_num.clear()
        self.media_num.addItems(self.media_items)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.media_num.setCurrentIndex(0)
        else:
            self.setChecked(True)
            self.media_num.setCurrentIndex(self.media_indexes.index(value))

    def getValue(self, value):
        if self.check.isChecked():
            return self.media_num.currentIndex()
        else:
            return None

    def setChecked(self, checked):
        self.check.setChecked(checked)
        self.showNumBox()

    def showNumBox(self):
        checked = self.check.isChecked()
        if checked:
            self.media_num.show()
        else:
            self.media_num.hide()

class CuePositionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.setValue(None)

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Position (%)')
        label.setFont(UIFonts.label_font)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        self.check = QCheckBox()
        self.pos_num = QNumberBox()
        self.pos_num.setMinimum(0)
        self.pos_num.setMaximum(100)
        self.pos_num.setDecimals(3)
        sp = self.pos_num.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.pos_num.setSizePolicy(sp)
        hbox.addWidget(self.check)
        hbox.addWidget(self.pos_num)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.check.stateChanged.connect(self.showNumBox)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.pos_num.setValue(0)
        else:
            self.setChecked(True)
            self.pos_num.setValue(value)

    def getValue(self, value):
        if self.check.isChecked():
            return self.pos_num.value
        else:
            return None

    def setChecked(self, checked):
        self.check.setChecked(checked)
        self.showNumBox()

    def showNumBox(self):
        checked = self.check.isChecked()
        if checked:
            self.pos_num.show()
        else:
            self.pos_num.hide()

class CueZoomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.setValue(None)

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Zoom (%)')
        label.setFont(UIFonts.label_font)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        self.check = QCheckBox()
        self.zoom_num = QNumberBox()
        self.zoom_num.setMinimum(0)
        sp = self.zoom_num.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.zoom_num.setSizePolicy(sp)
        hbox.addWidget(self.check)
        hbox.addWidget(self.zoom_num)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.check.stateChanged.connect(self.showNumBox)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.zoom_num.setValue(0)
        else:
            self.setChecked(True)
            self.zoom_num.setValue(value)

    def getValue(self, value):
        if self.check.isChecked():
            return self.zoom_num.value
        else:
            return None

    def setChecked(self, checked):
        self.check.setChecked(checked)
        self.showNumBox()

    def showNumBox(self):
        checked = self.check.isChecked()
        if checked:
            self.zoom_num.show()
        else:
            self.zoom_num.hide()

class CueSpeedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.setValue(None)

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Speed')
        label.setFont(UIFonts.label_font)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        self.check = QCheckBox()
        self.speed_num = QNumberBox()
        sp = self.speed_num.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.speed_num.setSizePolicy(sp)
        hbox.addWidget(self.check)
        hbox.addWidget(self.speed_num)

        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        subvbox = QVBoxLayout()
        self.ramp_num = QNumberBox()
        self.ramp_num.setMinimum(0)
        self.ramp_num.setFixedWidth(50)
        sp = self.ramp_num.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.ramp_num.setSizePolicy(sp)
        subvbox.addWidget(self.ramp_num)
        self.ramp_label = QLabel('ramp (s.)')
        self.ramp_label.setFont(UIFonts.sm_label_font)
        sp = self.ramp_label.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.ramp_label.setSizePolicy(sp)
        subvbox.addWidget(self.ramp_label)
        hbox.addStretch(1)
        hbox.addLayout(subvbox)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.check.stateChanged.connect(self.showNumBox)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.speed_num.setValue(0)
            self.ramp_num.setValue(0)
        else:
            self.setChecked(True)
            self.speed_num.setValue(value[0])
            self.ramp_num.setValue(value[1])

    def getValue(self, value):
        if self.check.isChecked():
            return (self.speed_num.value, self.ramp_num.value)
        else:
            return None

    def setChecked(self, checked):
        self.check.setChecked(checked)
        self.showNumBox()

    def showNumBox(self):
        checked = self.check.isChecked()
        if checked:
            self.speed_num.show()
            self.ramp_num.show()
            self.ramp_label.show()
        else:
            self.speed_num.hide()
            self.ramp_num.hide()
            self.ramp_label.hide()

class CueVolumeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.setValue(None)

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Volume (db)')
        label.setFont(UIFonts.label_font)
        vbox.addWidget(label)

        hbox = QHBoxLayout()
        hbox.setSpacing(10)
        self.check = QCheckBox()
        self.db_slider = QSlider(Qt.Horizontal)
        self.db_slider.setMinimum(-40)
        self.db_slider.setMaximum(12)
        sp = self.db_slider.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.db_slider.setSizePolicy(sp)
        hbox.addWidget(self.check)
        hbox.addWidget(self.db_slider)
        vbox.addLayout(hbox)


        hbox = QHBoxLayout()
        hbox.addStretch(1)
        self.db_num = QNumberBox()
        self.db_num.setMinimum(-40)
        self.db_num.setMaximum(12)
        sp = self.db_num.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.db_num.setSizePolicy(sp)
        self.db_num.setFixedWidth(50)
        hbox.addWidget(self.db_num)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.check.stateChanged.connect(self.showNumBox)
        self.db_num.valueChanged.connect(self.numStateChanged)
        self.db_slider.valueChanged.connect(self.sliderStateChanged)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.db_num.setValue(0)
            self.db_slider.setValue(0)
        else:
            self.setChecked(True)
            self.db_num.setValue(value)
            self.db_slider.setValue(value)

    def getValue(self, value):
        if self.check.isChecked():
            return self.db_num.value
        else:
            return None

    def setChecked(self, checked):
        self.check.setChecked(checked)
        self.showNumBox()

    def showNumBox(self):
        checked = self.check.isChecked()
        if checked:
            self.db_num.show()
            self.db_slider.show()
        else:
            self.db_num.hide()
            self.db_slider.hide()

    def numStateChanged(self):
        self.db_slider.setValue(self.db_num.value)

    def sliderStateChanged(self):
        self.db_num.setValue(self.db_slider.value())
