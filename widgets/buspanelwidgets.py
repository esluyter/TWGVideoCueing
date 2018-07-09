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

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.current_pos = CurrentPosWidget()
        self.current_pos.register(self)
        subvbox.addWidget(self.current_pos)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(0)
        subsubvbox = QVBoxLayout()
        subsubvbox.setSpacing(0)
        capturethisbutt = QPushButton('Capture this')
        capturethisbutt.setFont(UIFonts.butt_font)
        captureallbutt = QPushButton('Capture all')
        captureallbutt.setFont(UIFonts.butt_font)
        subsubvbox.addWidget(capturethisbutt)
        subsubvbox.addWidget(captureallbutt)
        subhbox.addLayout(subsubvbox)
        self.capture_num = QNumberBox()
        self.capture_num.setFixedWidth(50)
        subhbox.addWidget(self.capture_num)
        subvbox.addLayout(subhbox)
        subhbox = QHBoxLayout()
        subhbox.addStretch(1)
        setcueposbutt = QPushButton('Set cue position')
        setcueposbutt.setFont(UIFonts.butt_font)
        subhbox.addWidget(setcueposbutt)
        subvbox.addLayout(subhbox)
        vbox.addLayout(subvbox)

        vbox.addWidget(QHLine())

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        rw = QPushButton('◀◀')
        rw.setFont(QFont('SansSerif', 8))
        pause = QPushButton('\u25ae\u25ae')
        pause.setFont(QFont('SansSerif', 11))
        play = QPushButton('▶')
        ff = QPushButton('►►')
        ff.setFont(QFont('SansSerif', 8))
        hbox.addWidget(rw)
        hbox.addWidget(pause)
        hbox.addWidget(play)
        hbox.addWidget(ff)
        vbox.addLayout(hbox)

        vbox.addStretch(1)
        self.setLayout(vbox)

    def view_update(self, what, etc):
        if what == 'edited':
            self.changed('edited')

    def set_media_info(self, media_info):
        self.media.set_media_info(media_info)

    def set_current_pos(self, pos):
        self.current_pos.setValue(pos)

    def set_values(self, bus):
        self.media.setValue(bus.media_index)
        self.position.setValue(bus.pos)
        self.speed.setValue(None if bus.speed is None else (bus.speed, bus.ramp_time))
        self.zoom.setValue(bus.zoom)
        self.volume.setValue(bus.db)

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

        for i, j in [(i, j) for i in range(6) for j in range(5)]:
            box = QCheckBox()
            grid.addWidget(box, i + 2, j)

        vbox.addLayout(grid)

        vbox.addStretch(1)
        self.setLayout(vbox)

    def view_update(self, what, etc):
        if what == 'edited':
            self.changed('edited')

    def edited(self):
        return self.cue_matrix.edited

    def set_cue_routing(self, routing):
        self.cue_matrix.set_cue_routing(routing)

    def as_audio_routing(self):
        return self.cue_matrix.as_audio_routing()
