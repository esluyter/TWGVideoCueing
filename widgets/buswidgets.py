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

from common.publisher import Publisher
from common.util import *
from widgets.fonts import UIFonts
from widgets.littlewidgets import QNumberBox
from model.cuelist import AudioRouting
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QSlider, QLabel,
    QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy, QPushButton)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

#superclass
class BusCueComponent(QWidget, Publisher):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Publisher.__init__(self)

        self.role = 'view'

        self.edited = False
        self.cue_num = None
        self.default_bg = QColor('transparent')
        self.edited_bg = QColor(255, 200, 200)
        self.setAutoFillBackground(True)

    def numStateChanged(self):
        self.setEdited(self.getValue() != self.cue_num)

    def setEdited(self, edited):
        if edited == self.edited:
            return
        self.edited = edited
        p = self.palette()
        p.setColor(QPalette.Background, self.edited_bg if edited else self.default_bg)
        self.setPalette(p)
        self.changed('edited')


class CurrentPosWidget(BusCueComponent):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.locked = False
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        label = QLabel('Current position')
        label.setFont(UIFonts.label_font)
        self.pos_label = QLabel('0%')
        hbox.addWidget(label)
        hbox.addStretch(1)
        hbox.addWidget(self.pos_label)
        vbox.addLayout(hbox)
        self.pos_slider = QSlider(Qt.Horizontal)
        self.pos_slider.setMaximum(100)
        self.pos_slider.setMinimum(0)
        self.pos_slider.sliderMoved.connect(self.slider_moved)
        self.pos_slider.sliderPressed.connect(self.slider_pressed)
        self.pos_slider.sliderReleased.connect(self.slider_released)
        self
        vbox.addWidget(self.pos_slider)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        capturethisbutt = QPushButton('Capture this')
        capturethisbutt.setFont(UIFonts.butt_font)
        capturethisbutt.clicked.connect(self.capture)
        captureallbutt = QPushButton('Capture all')
        captureallbutt.setFont(UIFonts.butt_font)
        captureallbutt.clicked.connect(self.capture_all)
        subvbox.addWidget(capturethisbutt)
        subvbox.addWidget(captureallbutt)
        hbox.addLayout(subvbox)
        self.capture_num = QNumberBox()
        self.capture_num.setFixedWidth(50)
        hbox.addWidget(self.capture_num)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        setcueposbutt = QPushButton('Set cue position')
        setcueposbutt.setFont(UIFonts.butt_font)
        setcueposbutt.clicked.connect(self.set_cue_pos)
        hbox.addWidget(setcueposbutt)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def setValue(self, value):
        self.value = value;
        if not self.locked:
            self.pos_slider.setValue(value)
        self.pos_label.setText('%s%%' % str(round(value, 2)))

    def capture(self):
        self.capture_num.setValue(self.value)
        #ugh hack
        self.capture_num.hide()
        self.capture_num.show()

    def capture_all(self):
        self.changed('capture_all')

    def set_cue_pos(self):
        self.changed('set_cue_pos', self.value)

    def slider_pressed(self):
        self.locked = True
        self.changed('set_bus_pos', self.pos_slider.value())

    def slider_released(self):
        self.locked = False

    def slider_moved(self):
        self.changed('set_bus_pos', self.pos_slider.value())

class CueMediaWidget(BusCueComponent):
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
        self.media_num.currentIndexChanged.connect(self.numStateChanged)

    def refreshMedia(self):
        self.media_num.clear()
        self.media_num.addItems(self.media_items)

    def setValue(self, value):
        self.cue_num = value
        self.setEdited(False)

        if value is None:
            self.setChecked(False)
            self.media_num.setCurrentIndex(0)
        else:
            self.setChecked(True)
            self.media_num.setCurrentIndex(self.media_indexes.index(value))

    def getValue(self):
        if self.check.isChecked():
            return self.media_indexes[self.media_num.currentIndex()]
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
        self.numStateChanged()

class CuePositionWidget(BusCueComponent):
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
        self.pos_num.valueChanged.connect(self.numStateChanged)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.pos_num.setValue(0)
        else:
            self.setChecked(True)
            self.pos_num.setValue(value)

        self.cue_num = self.getValue()
        self.setEdited(False)

    def setValueEdited(self, value):
        if value is None:
            self.setChecked(False)
            self.pos_num.setValue(0)
        else:
            self.setChecked(True)
            self.pos_num.setValue(value)
        self.numStateChanged()
        # ugh hack
        self.hide()
        self.show()

    def getValue(self):
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
        self.numStateChanged()

class CueZoomWidget(BusCueComponent):
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
        self.zoom_num.valueChanged.connect(self.numStateChanged)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.zoom_num.setValue(100)
        else:
            self.setChecked(True)
            self.zoom_num.setValue(value)

        self.cue_num = self.getValue()
        self.setEdited(False)

    def getValue(self):
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
        self.numStateChanged()

class CueSpeedWidget(BusCueComponent):
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
        self.speed_num.valueChanged.connect(self.numStateChanged)
        self.ramp_num.valueChanged.connect(self.numStateChanged)

    def setValue(self, value):
        if value is None:
            self.setChecked(False)
            self.speed_num.setValue(1)
            self.ramp_num.setValue(0)
        else:
            self.setChecked(True)
            self.speed_num.setValue(value[0])
            self.ramp_num.setValue(value[1])

        self.cue_num = self.getValue()
        self.setEdited(False)

    def getValue(self):
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
        self.numStateChanged()

class CueVolumeWidget(BusCueComponent):
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

        self.cue_num = self.getValue()
        self.setEdited(False)

    def getValue(self):
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
        super().numStateChanged()

    def numStateChanged(self):
        self.db_slider.setValue(self.db_num.value)
        super().numStateChanged()

    def sliderStateChanged(self):
        self.db_num.setValue(self.db_slider.value())

class AudioMatrixWidget(QWidget, Publisher):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Publisher.__init__(self)

        self.role = 'view'

        self.edited = False
        self.cue_matrix = make_2d_list(5, 6, False)
        self.default_bg = QColor('transparent')
        self.edited_bg = QColor(255, 200, 200)
        self.setAutoFillBackground(True)

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        for bus, i in zip(['A', 'B', 'C', 'D', 'E'], range(5)):
            label = QLabel(' ' + bus)
            label.setFont(UIFonts.label_font)
            grid.addWidget(label, 0, i)

        for dest, i in zip(['Ear 1', 'Ear 2', 'Ear 3', 'Room', 'Extra',
                'Phones'], range(6)):
            label = QLabel(dest)
            label.setFont(UIFonts.label_font)
            grid.addWidget(label, i + 1, 5)

        self.matrix = []

        for i in range(5):
            self.matrix.append([])
            for j in range(6):
                checkbox = QCheckBox()
                checkbox.stateChanged.connect(self.matrixStateChanged)
                self.matrix[i].append(checkbox)
                grid.addWidget(self.matrix[i][j], j + 1, i)

        self.setLayout(grid)

    def set_cue_routing(self, routing):
        self.cue_matrix = routing.matrix_state
        self.setEdited(False)

        for i, row in enumerate(self.matrix):
            for j, checkbox in enumerate(row):
                checkbox.setChecked(routing.at(i, j))

    def getValue(self):
        temp = make_2d_list(5, 6, False)
        for i, row in enumerate(self.matrix):
            for j, checkbox in enumerate(row):
                if checkbox.isChecked():
                    temp[i][j] = True
        return temp

    def as_audio_routing(self):
        return AudioRouting(self.getValue())

    def matrixStateChanged(self):
        self.setEdited(self.getValue() != self.cue_matrix)

    def setEdited(self, edited):
        if edited == self.edited:
            return
        self.edited = edited
        p = self.palette()
        p.setColor(QPalette.Background, self.edited_bg if edited else self.default_bg)
        self.setPalette(p)
        self.changed('edited')
