"""
Custom compound widgets for TWG video cueing lower bus panel

- BusWidget
- SoundPatchWidget

Author: Eric Sluyter
Last edited: July 2018
"""

from littlewidgets import QHLine, QNumberBox
from painterwidgets import LevelMeter
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QLabel, QSlider, QHBoxLayout, QVBoxLayout, QCheckBox,
    QSizePolicy, QGridLayout, QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BusWidget(QWidget):
    title_font = QFont('SansSerif', 20)
    label_font = QFont('SansSerif', 10, 100)
    butt_font = QFont('SansSerif', 10)
    media_items = ['0 - BLACK', '1 - ISNR', '2 - TBH', '3 - TOKYO']

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
        label = QLabel('Media number')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.media_check = QCheckBox()
        self.media_num = QComboBox()
        self.media_num.addItems(self.media_items)
        self.media_num.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
        subhbox.addWidget(self.media_check)
        subhbox.addWidget(self.media_num)
        subvbox.addLayout(subhbox)
        vbox.addLayout(subvbox)

        hbox = QHBoxLayout()

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        label = QLabel('Position (%)')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.pos_check = QCheckBox()
        self.pos_num = QNumberBox()
        subhbox.addWidget(self.pos_check)
        subhbox.addWidget(self.pos_num)
        subvbox.addLayout(subhbox)
        subvbox.addSpacing(10)
        label = QLabel('Zoom')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.zoom_check = QCheckBox()
        self.zoom_num = QNumberBox()
        subhbox.addWidget(self.zoom_check)
        subhbox.addWidget(self.zoom_num)
        subvbox.addLayout(subhbox)
        hbox.addLayout(subvbox)

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        label = QLabel('Speed')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.speed_check = QCheckBox()
        self.speed_num = QNumberBox()
        subhbox.addWidget(self.speed_check)
        subhbox.addWidget(self.speed_num)
        subvbox.addLayout(subhbox)
        subhbox = QHBoxLayout()
        subsubvbox = QVBoxLayout()
        self.ramp_num = QNumberBox()
        self.ramp_num.setFixedWidth(50)
        subsubvbox.addWidget(self.ramp_num)
        label = QLabel('ramp (s.)')
        label.setFont(QFont('SansSerif', 10, -1, True))
        subsubvbox.addWidget(label)
        subhbox.addStretch(1)
        subhbox.addLayout(subsubvbox)
        subvbox.addLayout(subhbox)
        subvbox.addStretch(1)
        hbox.addLayout(subvbox)

        vbox.addLayout(hbox)

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        label = QLabel('Volume (db)')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.db_check = QCheckBox()
        self.db_slider = QSlider(Qt.Horizontal)
        subhbox.addWidget(self.db_check)
        subhbox.addWidget(self.db_slider)
        subvbox.addLayout(subhbox)
        subhbox = QHBoxLayout()
        subhbox.addStretch(1)
        self.db_num = QNumberBox()
        self.db_num.setFixedWidth(50)
        subhbox.addWidget(self.db_num)
        subvbox.addLayout(subhbox)
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

        for i, j in [(i, j) for i in range(6) for j in range(5)]:
            box = QCheckBox()
            grid.addWidget(box, i + 1, j)

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
