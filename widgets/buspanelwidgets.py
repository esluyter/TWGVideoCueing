"""
Custom compound widgets for TWG video cueing lower bus panel

- BusWidget
- SoundPatchWidget

Author: Eric Sluyter
Last edited: July 2018
"""

from widgets.buswidgets import (CuePositionWidget, CueSpeedWidget, CueZoomWidget,
    CueMediaWidget, CueVolumeWidget)
from widgets.littlewidgets import QHLine, QNumberBox
from widgets.painterwidgets import LevelMeter
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QLabel, QSlider, QHBoxLayout, QVBoxLayout, QCheckBox,
    QSizePolicy, QGridLayout, QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BusWidget(QWidget):
    title_font = QFont('SansSerif', 20)
    label_font = QFont('SansSerif', 10, 100)
    butt_font = QFont('SansSerif', 10)


    def __init__(self, letter):
        super().__init__()
        self.letter = letter
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        title = QLabel('Bus ' + self.letter)
        title.setFont(self.title_font)
        vbox.addWidget(title)

        vbox.addWidget(QHLine())

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.media = CueMediaWidget()
        subvbox.addWidget(self.media)
        vbox.addLayout(subvbox)

        hbox = QHBoxLayout()

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.position = CuePositionWidget()
        subvbox.addWidget(self.position)
        subvbox.addSpacing(10)
        self.zoom = CueZoomWidget()
        subvbox.addWidget(self.zoom)
        hbox.addLayout(subvbox)

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.speed = CueSpeedWidget()
        subvbox.addWidget(self.speed)
        subvbox.addStretch(1)
        hbox.addLayout(subvbox)

        vbox.addLayout(hbox)

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        self.volume = CueVolumeWidget()
        subvbox.addWidget(self.volume)
        vbox.addLayout(subvbox)

        vbox.addWidget(QHLine())

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        label = QLabel('Current play position')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.current_pos_slider = QSlider(Qt.Horizontal)
        self.current_pos_label = QLabel('0%')
        subhbox.addWidget(self.current_pos_slider)
        subhbox.addWidget(self.current_pos_label)
        subvbox.addLayout(subhbox)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(0)
        subsubvbox = QVBoxLayout()
        subsubvbox.setSpacing(0)
        capturethisbutt = QPushButton('Capture this')
        capturethisbutt.setFont(self.butt_font)
        captureallbutt = QPushButton('Capture all')
        captureallbutt.setFont(self.butt_font)
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
        setcueposbutt.setFont(self.butt_font)
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

    def set_media_info(self, media_info):
        self.media.set_media_info(media_info)

    def set_values(self, bus):
        self.media.setValue(bus.media_index)
        self.position.setValue(bus.pos)
        self.speed.setValue(None if bus.speed is None else (bus.speed, bus.ramp_time))
        self.zoom.setValue(bus.zoom)
        self.volume.setValue(bus.db)

class SoundPatchWidget(QWidget):
    title_font = QFont('SansSerif', 20)
    label_font = QFont('SansSerif', 10, 100)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        title = QLabel('Cue routing')
        title.setFont(self.title_font)
        vbox.addWidget(title)

        vbox.addWidget(QHLine())

        grid = QGridLayout()

        for bus, i in zip(['A', 'B', 'C', 'D', 'E'], range(5)):
            label = QLabel(' ' + bus)
            label.setFont(self.label_font)
            grid.addWidget(label, 0, i)

        for dest, i in zip(['Ear 1', 'Ear 2', 'Ear 3', 'Room', 'Extra',
                'Phones'], range(6)):
            label = QLabel(dest)
            label.setFont(self.label_font)
            grid.addWidget(label, i + 1, 5)

        self.cue_matrix = []

        for i in range(5):
            self.cue_matrix.append([])
            for j in range(6):
                self.cue_matrix[i].append(QCheckBox())
                grid.addWidget(self.cue_matrix[i][j], j + 1, i)

        vbox.addLayout(grid)

        vbox.addSpacing(40)

        title = QLabel('Current routing')
        title.setFont(self.title_font)
        vbox.addWidget(title)

        vbox.addWidget(QHLine())

        grid = QGridLayout()

        for i in range(5):
            meter = LevelMeter()
            meter.setFixedHeight(30)
            meter.set_gap(2)
            grid.addWidget(meter, 0, i)

        for bus, i in zip(['A', 'B', 'C', 'D', 'E'], range(5)):
            label = QLabel(' ' + bus)
            label.setFont(self.label_font)
            grid.addWidget(label, 1, i)

        for dest, i in zip(['Ear 1', 'Ear 2', 'Ear 3', 'Room', 'Extra',
                'Phones'], range(6)):
            label = QLabel(dest)
            label.setFont(self.label_font)
            grid.addWidget(label, i + 2, 5)

        for i, j in [(i, j) for i in range(6) for j in range(5)]:
            box = QCheckBox()
            grid.addWidget(box, i + 2, j)

        vbox.addLayout(grid)

        vbox.addStretch(1)
        self.setLayout(vbox)

    def set_cue_routing(self, routing):
        for i, row in enumerate(self.cue_matrix):
            for j, checkbox in enumerate(row):
                checkbox.setChecked(routing.at(i, j))
