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
    QLabel, QSlider, QTextEdit)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QPalette
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
        self.itemDelegate().closeEditor.connect(self.name_changed)
        self.lock = False

    def set_cues(self, cues):
        self.cues = cues
        self.item_model.clear()

        for cue in self.cues:
            item = QStandardItem(cue)
            self.item_model.appendRow(item)

    def set_current_cue(self, index):
        self.lock = True
        index = self.item_model.index(index, 0)
        self.setCurrentIndex(index)
        self.lock = False

    def update_cue_pointer(self, a, b):
        if self.lock:
            return
        self.changed('cue_pointer', self.currentIndex().row())

    def name_changed(self):
        index = self.currentIndex().row()
        item = self.item_model.item(index, 0)
        name = item.text()
        self.changed('cue_name', name)

class CueButtonsLayout(QVBoxLayout, Publisher):
    def __init__(self):
        QVBoxLayout.__init__(self)
        Publisher.__init__(self)
        self.role = 'view'
        self.initUI()

    def initUI(self):
        self.setSpacing(0)

        blank_before = QPushButton('+↑ Insert blank cue before')
        blank_after = QPushButton('+↓ Insert blank cue after')
        blank_before.clicked.connect(self.blank_before_clicked)
        blank_after.clicked.connect(self.blank_after_clicked)
        self.addWidget(blank_before)
        self.addWidget(blank_after)
        self.addSpacing(15)
        self.insert_before = QPushButton('↑ Save as new cue before')
        self.insert_before.clicked.connect(self.insert_before_clicked)
        self.addWidget(self.insert_before)
        self.update = QPushButton('Update cue')
        self.update.clicked.connect(self.update_clicked)
        self.update_fire = QPushButton('Update and fire cue')
        self.update_fire.clicked.connect(self.update_fire_clicked)
        self.addWidget(self.update)
        self.addWidget(self.update_fire)
        self.insert_after = QPushButton('↓ Save as new cue after')
        self.insert_after.clicked.connect(self.insert_after_clicked)
        self.addWidget(self.insert_after)
        self.addSpacing(15)
        delete = QPushButton('⌫ Delete cue')
        delete.clicked.connect(self.delete_clicked)
        self.addWidget(delete)

    def blank_before_clicked(self):
        self.changed('blank_before')

    def blank_after_clicked(self):
        self.changed('blank_after')

    def delete_clicked(self):
        self.changed('delete_current')

    def update_clicked(self):
        self.changed('update')

    def update_fire_clicked(self):
        self.changed('update_fire')

    def insert_before_clicked(self):
        self.changed('insert_before')

    def insert_after_clicked(self):
        self.changed('insert_after')

    def setEdited(self, edited):
        for button in [self.update, self.insert_before, self.insert_after]:
            p = button.palette()
            if edited:
                p.setColor(QPalette.Button, QColor(255, 180, 180))
            else:
                p.setColor(QPalette.Button, QColor('transparent'))
            button.setAutoFillBackground(True)
            button.setPalette(p)
        p = self.update_fire.palette()
        if edited:
            p.setColor(QPalette.Button, QColor(0, 200, 0))
        else:
            p.setColor(QPalette.Button, QColor('transparent'))
        self.update_fire.setAutoFillBackground(True)
        self.update_fire.setPalette(p)

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
        self.changed('rwff_speed', self.rwff_num.value)

    def sliderStateChanged(self):
        self.rwff_num.setValue(self.rwff_slider.value())
        self.changed('rwff_speed', self.rwff_num.value)

    def set_rwff_speed(self, speed):
        self.rwff_slider.setValue(speed)
        self.rwff_num.setValue(speed)

class CueNotesWidget(QTextEdit, Publisher):
    def __init__(self):
        QTextEdit.__init__(self)
        Publisher.__init__(self)

        self.role = 'view'

        self.cue_text = ''
        self.default_bg = QColor('white')
        self.edited_bg = QColor(255, 200, 200)
        self.edited = False
        self.initUI()

    def initUI(self):
        self.setFont(UIFonts.notes_font)

    def keyPressEvent(self, event):
        QTextEdit.keyPressEvent(self, event)
        self.setEdited(str(self.toPlainText()) != self.cue_text)

    def setPlainText(self, text):
        self.cue_text = text
        QTextEdit.setPlainText(self, text)
        self.setEdited(False)

    def setEdited(self, edited):
        if edited == self.edited:
            return
        self.edited = edited
        p = self.palette()
        p.setColor(QPalette.Base, self.edited_bg if edited else self.default_bg)
        self.setPalette(p)
        self.changed('edited')
