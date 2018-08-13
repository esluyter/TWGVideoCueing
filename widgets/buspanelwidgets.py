"""
Custom compound widgets for TWG video cueing lower bus panel

- BusWidget
- SoundPatchWidget

Author: Eric Sluyter
Last edited: July 2018
"""

from common.publisher import Publisher
from widgets.fonts import UIFonts
from widgets.buswidgets import (CuePositionWidget, CueSpeedWidget, CueZoomWidget,
    CueMediaWidget, CueVolumeWidget, AudioMatrixWidget, CurrentPosWidget)
from widgets.littlewidgets import QHLine, QNumberBox
from widgets.painterwidgets import LevelMeter
from model.cuelist import BusCue
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QLabel, QSlider, QHBoxLayout, QVBoxLayout, QCheckBox,
    QSizePolicy, QGridLayout, QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BusWidget(QWidget, Publisher):
    def __init__(self, letter):
        QWidget.__init__(self)
        Publisher.__init__(self)

        self.role = 'view'

        self.letter = letter
        self.initUI()
        self.set_active(False)

    def initUI(self):
        vbox = QVBoxLayout()

        title = QLabel('Bus ' + self.letter)
        title.setFont(UIFonts.title_font)
        vbox.addWidget(title)

        vbox.addWidget(QHLine())

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.media = CueMediaWidget()
        self.media.register(self)
        subvbox.addWidget(self.media)
        vbox.addLayout(subvbox)

        hbox = QHBoxLayout()

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.position = CuePositionWidget()
        self.position.register(self)
        subvbox.addWidget(self.position)
        subvbox.addSpacing(10)
        self.zoom = CueZoomWidget()
        self.zoom.register(self)
        subvbox.addWidget(self.zoom)
        hbox.addLayout(subvbox)

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.speed = CueSpeedWidget()
        self.speed.register(self)
        subvbox.addWidget(self.speed)
        subvbox.addStretch(1)
        hbox.addLayout(subvbox)

        vbox.addLayout(hbox)

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.volume = CueVolumeWidget()
        self.volume.register(self)
        subvbox.addWidget(self.volume)
        vbox.addLayout(subvbox)

        vbox.addSpacing(20)
        vbox.addWidget(QHLine())

        self.current_pos = CurrentPosWidget()
        sp = self.current_pos.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.current_pos.setSizePolicy(sp)
        self.current_pos.register(self)

        vbox.addWidget(self.current_pos)

        line = QHLine()
        vbox.addWidget(line)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        rw = QPushButton('◀◀')
        rw.setFixedWidth(45)
        sp = rw.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        rw.setSizePolicy(sp)
        rw.setFont(QFont('SansSerif', 8))
        rw.clicked.connect(self.rw)
        pause = QPushButton('\u25ae\u25ae')
        pause.setFixedWidth(45)
        pause.setSizePolicy(sp)
        pause.setFont(QFont('SansSerif', 11))
        pause.clicked.connect(self.pause)
        play = QPushButton('▶')
        play.setFixedWidth(45)
        play.setSizePolicy(sp)
        play.clicked.connect(self.play)
        ff = QPushButton('►►')
        ff.setFixedWidth(45)
        ff.setSizePolicy(sp)
        ff.setFont(QFont('SansSerif', 8))
        ff.clicked.connect(self.ff)
        hbox.addWidget(rw)
        hbox.addWidget(pause)
        hbox.addWidget(play)
        hbox.addWidget(ff)
        vbox.addLayout(hbox)

        self.transport = [line, rw, pause, play, ff]

        vbox.addStretch(1)
        self.setLayout(vbox)

    def view_update(self, what, etc):
        if what == 'edited':
            self.changed('edited')
        if what == 'capture_all':
            self.changed('capture_all')
        if what == 'set_cue_pos':
            self.position.setValueEdited(etc)
        if what == 'set_bus_pos':
            self.changed('set_bus_pos', (ord(self.letter) - 65, etc))

    def set_media_info(self, media_info):
        self.media.set_media_info(media_info)

    def set_current_pos(self, pos):
        self.current_pos.setValue(pos)

    def set_current_media(self, media_name):
        self.current_pos.setMedia(media_name)

    def set_active(self, active):
        if active:
            self.current_pos.show()
            for thing in self.transport:
                thing.show()
        else:
            self.current_pos.hide()
            for thing in self.transport:
                thing.hide()

    def set_values(self, bus):
        self.media.setValue(bus.media_index)
        self.position.setValue(bus.pos)
        self.speed.setValue(None if bus.speed is None else (bus.speed, bus.ramp_time))
        self.zoom.setValue(bus.zoom)
        self.volume.setValue(bus.db)

    def rw(self):
        self.changed('rw', ord(self.letter) - 65)

    def ff(self):
        self.changed('ff', ord(self.letter) - 65)

    def play(self):
        self.changed('play', ord(self.letter) - 65)

    def pause(self):
        self.changed('pause', ord(self.letter) - 65)

    def edited(self):
        return (self.media.edited or self.position.edited or self.speed.edited or
            self.zoom.edited or self.volume.edited)

    def as_bus_cue(self):
        media_index = self.media.getValue()
        pos = self.position.getValue()
        speed = self.speed.getValue()
        ramp_time = None if speed is None else speed[1]
        if speed is not None:
            speed = speed[0]
        zoom = self.zoom.getValue()
        db = self.volume.getValue()
        return BusCue(media_index, pos, speed, ramp_time, zoom, db)

class SoundPatchWidget(QWidget, Publisher):
    def __init__(self):
        QWidget.__init__(self)
        Publisher.__init__(self)
        self.role = 'view'
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        title = QLabel('Cue routing')
        title.setFont(UIFonts.title_font)
        vbox.addWidget(title)

        vbox.addWidget(QHLine())

        self.cue_matrix = AudioMatrixWidget()
        self.cue_matrix.register(self)
        vbox.addWidget(self.cue_matrix)

        vbox.addSpacing(40)

        title = QLabel('Current routing')
        title.setFont(UIFonts.title_font)
        vbox.addWidget(title)

        vbox.addWidget(QHLine())

        grid = QGridLayout()

        self.meters = []

        for i in range(5):
            self.meters.append(LevelMeter())
            self.meters[i].setFixedHeight(30)
            self.meters[i].set_gap(2)
            grid.addWidget(self.meters[i], 0, i)

        for bus, i in zip(['A', 'B', 'C', 'D', 'E'], range(5)):
            label = QLabel(' ' + bus)
            label.setFont(UIFonts.label_font)
            grid.addWidget(label, 1, i)

        for dest, i in zip(['Ear 1', 'Ear 2', 'Ear 3', 'Room', 'Extra',
                'Phones'], range(6)):
            label = QLabel(dest)
            label.setFont(UIFonts.label_font)
            grid.addWidget(label, i + 2, 5)

        self.matrix = []

        for i in range(5):
            self.matrix.append([])
            for j in range(6):
                checkbox = QCheckBox()
                checkbox.clicked.connect(self.matrixStateChanged)
                self.matrix[i].append(checkbox)
                grid.addWidget(self.matrix[i][j], j + 2, i)

        vbox.addLayout(grid)

        vbox.addStretch(1)
        self.setLayout(vbox)

    def set_checkbox(self, i, j, checked):
        self.matrix[i][j].setChecked(checked)

    def matrixStateChanged(self):
        data = ['n'] * (7 * 5 + 5)
        str = ''
        for i, row in enumerate(self.matrix):
            for j, checkbox in enumerate(row):
                str += '%d %d ' % (i, j)
                if checkbox.isChecked():
                    str += '1 '
                else:
                    str += '0 '
        data.append(str.strip())
        self.changed('current_matrix', data)

    def view_update(self, what, etc):
        if what == 'edited':
            self.changed('edited')

    def edited(self):
        return self.cue_matrix.edited

    def set_cue_routing(self, routing):
        self.cue_matrix.set_cue_routing(routing)

    def as_audio_routing(self):
        return self.cue_matrix.as_audio_routing()
