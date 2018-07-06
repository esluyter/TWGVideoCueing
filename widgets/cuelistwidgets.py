"""
Custom widgets for top panel

- CueListWidget
- CueButtonsLayout
- CueMidpanelLayout

Author: Eric Sluyter
Last edited: July 2018
"""

from widgets.fonts import UIFonts
from widgets.littlewidgets import QNumberBox
from PyQt5.QtWidgets import (QListView, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from common.publisher import Publisher

class CueListWidget(QListView, Publisher):
    def __init__(self):
        QListView.__init__(self)
        Publisher.__init__(self)
        self.role = 'view'
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(150)
        self.item_model = QStandardItemModel(self)
        self.setModel(self.item_model)
        self.setFont(UIFonts.cuelist_font)
        self.set_cues([''])
        self.selectionModel().currentChanged.connect(self.update_cue_pointer)

    def set_cues(self, cues):
        self.cues = cues
        self.item_model.clear()

        for cue in self.cues:
            item = QStandardItem(cue)
            self.item_model.appendRow(item)

    def set_current_cue(self, index):
        index = self.item_model.index(index, 0)
        self.setCurrentIndex(index)

    def update_cue_pointer(self, a, b):
        self.changed('cue_pointer', self.currentIndex().row())

class CueButtonsLayout(QVBoxLayout, Publisher):
    def __init__(self):
        QVBoxLayout.__init__(self)
        Publisher.__init__(self)
        self.role = 'view'
        self.initUI()

    def initUI(self):
        self.setSpacing(0)

        self.addWidget(QPushButton('+↑ Insert blank cue before'))
        self.addWidget(QPushButton('+↓ Insert blank cue after'))
        self.addSpacing(15)
        self.addWidget(QPushButton('↑ Save as new cue before'))
        self.addWidget(QPushButton('Update cue'))
        self.addWidget(QPushButton('Update and fire cue'))
        self.addWidget(QPushButton('↓ Save as new cue after'))
        self.addSpacing(15)
        self.addWidget(QPushButton('⌫ Delete cue'))
        self.addWidget(QPushButton('✎ Rename cue'))

class CueMidpanelLayout(QVBoxLayout, Publisher):
    def __init__(self):
        QVBoxLayout.__init__(self)
        Publisher.__init__(self)
        self.role = 'view'
        self.initUI()

    def initUI(self):
        self.setSpacing(0)

        self.cue_name = QLabel('Cue Name')
        self.cue_name.setFont(UIFonts.cue_name_font)
        self.addWidget(self.cue_name)

        self.gobutton = QPushButton('GO')
        self.gobutton.setFont(UIFonts.gobutton_font)
        self.addWidget(self.gobutton)

        self.transport = QHBoxLayout()
        self.transport.setSpacing(0)

        self.rw = QPushButton('◀◀')
        self.rw.setFont(UIFonts.transport_rwff_font)
        self.rw.setFixedHeight(70)
        self.pause = QPushButton('\u25ae\u25ae')
        self.pause.setFont(UIFonts.transport_pause_font)
        self.pause.setFixedHeight(70)
        self.play = QPushButton('▶')
        self.play.setFont(UIFonts.transport_play_font)
        self.play.setFixedHeight(70)
        self.ff = QPushButton('►►')
        self.ff.setFont(UIFonts.transport_rwff_font)
        self.ff.setFixedHeight(70)

        self.transport.addWidget(self.rw)
        self.transport.addWidget(self.pause)
        self.transport.addWidget(self.play)
        self.transport.addWidget(self.ff)

        self.addLayout(self.transport)

        self.rwff_speed = QHBoxLayout()
        self.rwff_speed.setSpacing(0)
        label = QLabel('RW/FF speed')
        label.setFont(UIFonts.label_font)
        label.setFixedWidth(70)
        self.rwff_slider = QSlider(Qt.Horizontal)
        self.rwff_slider.setFixedWidth(150)
        self.rwff_slider.setMinimum(2)
        self.rwff_slider.setMaximum(40)
        self.rwff_num = QNumberBox()
        self.rwff_num.setFixedWidth(50)
        self.rwff_num.setMinimum(2)
        self.rwff_num.setMaximum(40)
        self.rwff_speed.addWidget(label)
        self.rwff_speed.addWidget(self.rwff_slider)
        self.rwff_speed.addWidget(self.rwff_num)

        self.addLayout(self.rwff_speed)

        self.rwff_num.valueChanged.connect(self.numStateChanged)
        self.rwff_slider.valueChanged.connect(self.sliderStateChanged)

    def numStateChanged(self):
        self.rwff_slider.setValue(self.rwff_num.value)

    def sliderStateChanged(self):
        self.rwff_num.setValue(self.rwff_slider.value())

    def set_rwff_speed(self, speed):
        self.rwff_slider.setValue(speed)
        self.rwff_num.setValue(speed)
