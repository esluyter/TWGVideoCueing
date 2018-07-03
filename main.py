#!/usr/local/bin/python3

"""
Testing the Python implementation of TWG Cueing System

Author: Eric Sluyter
Last edited: July 2018
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton,
    QMessageBox, QDesktopWidget, QMainWindow, QAction, QTextEdit, QLineEdit,
    QLabel, QSlider, QHBoxLayout, QVBoxLayout, QFrame, QCheckBox, QSlider,
    QSizePolicy, QGridLayout, QComboBox, QListView)
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        #self.setFrameShadow(QFrame.Sunken)

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
        self.pos_num = QLineEdit()
        subhbox.addWidget(self.pos_check)
        subhbox.addWidget(self.pos_num)
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
        self.speed_num = QLineEdit()
        subhbox.addWidget(self.speed_check)
        subhbox.addWidget(self.speed_num)
        subvbox.addLayout(subhbox)
        hbox.addLayout(subvbox)

        vbox.addLayout(hbox)

        hbox = QHBoxLayout()

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        label = QLabel('Zoom')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.zoom_check = QCheckBox()
        self.zoom_num = QLineEdit()
        subhbox.addWidget(self.zoom_check)
        subhbox.addWidget(self.zoom_num)
        subvbox.addLayout(subhbox)
        hbox.addLayout(subvbox)

        subvbox = QVBoxLayout()
        subvbox.setSpacing(0)
        label = QLabel('Flip')
        label.setFont(self.label_font)
        subvbox.addWidget(label)
        subhbox = QHBoxLayout()
        subhbox.setSpacing(10)
        self.flip_check = QCheckBox()
        self.flip_num = QLineEdit()
        subhbox.addWidget(self.flip_check)
        subhbox.addWidget(self.flip_num)
        subvbox.addLayout(subhbox)
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
        self.db_num = QLineEdit()
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
        self.capture_num = QLineEdit()
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
        title = QLabel('Sound Patch')
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

        vbox.addStretch(1)
        self.setLayout(vbox)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        list = QListView()
        list.setMinimumWidth(150)
        model = QStandardItemModel(list)
        cues = ['*100*', 'TBH', '5.4', '6', '7', '9', '17', '25', '28', '30', '31',
            'EAR ROUTING 2.0', '31.5', '33', '35', '38', '39', '38.5', '47', '47.05',
            '47.1', '47.2', '50', '50.6', '51', '54', '56', '85', '85.5', '87', '90',
            'A bus', 'DANCE']

        for cue in cues:
            item = QStandardItem(cue)
            model.appendRow(item)

        list.setModel(model)

        hbox.addWidget(list)

        vbox = QVBoxLayout()

        topstuff = QHBoxLayout()

        buttons = QVBoxLayout()
        buttons.setSpacing(0)
        buttons.addWidget(QPushButton('↑ Save as new cue before'))
        buttons.addWidget(QPushButton('Update current cue'))
        buttons.addWidget(QPushButton('↓ Save as new cue after'))
        buttons.addWidget(QLabel(' '))
        buttons.addWidget(QPushButton('+↑ Insert blank cue before'))
        buttons.addWidget(QPushButton('+↓ Insert blank cue after'))
        buttons.addWidget(QLabel(' '))
        buttons.addWidget(QPushButton('⌫ Delete current cue'))
        buttons.addWidget(QPushButton('✎ Rename current cue'))
        topstuff.addLayout(buttons)

        midpanel = QVBoxLayout()
        midpanel.setSpacing(0)
        cue_name = QLabel('Cue 6')
        cue_name.setFont(QFont('SansSerif', 40))
        midpanel.addWidget(cue_name)
        gobutton = QPushButton('GO')
        gobutton.setFont(QFont('SansSerif', 50))
        midpanel.addWidget(gobutton)
        transport = QHBoxLayout()
        transport.setSpacing(0)
        rw = QPushButton('◀◀')
        rw.setFont(QFont('SansSerif', 20))
        rw.setFixedHeight(70)
        pause = QPushButton('\u25ae\u25ae')
        pause.setFont(QFont('SansSerif', 35))
        pause.setFixedHeight(70)
        play = QPushButton('▶')
        play.setFont(QFont('SansSerif', 40))
        play.setFixedHeight(70)
        ff = QPushButton('►►')
        ff.setFont(QFont('SansSerif', 20))
        ff.setFixedHeight(70)
        transport.addWidget(rw)
        transport.addWidget(pause)
        transport.addWidget(play)
        transport.addWidget(ff)
        midpanel.addLayout(transport)
        topstuff.addLayout(midpanel)

        notes = QTextEdit()
        notes.setPlainText('They were waiting at the table')
        notes.setFont(QFont('SansSerif', 15, 100))
        topstuff.addWidget(notes)

        vbox.addLayout(topstuff)

        #vbox.addWidget(QHLine())

        buses = QHBoxLayout()
        buses.addWidget(BusWidget('A'))
        buses.addWidget(BusWidget('B'))
        buses.addWidget(BusWidget('C'))
        buses.addWidget(BusWidget('D'))
        buses.addWidget(BusWidget('E'))
        buses.addWidget(SoundPatchWidget())
        vbox.addLayout(buses)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        mainwidget = MainWidget()
        self.setCentralWidget(mainwidget)

        action = QAction(QIcon('poo.png'), '&Test', self)
        action.triggered.connect(self.close)
        #action.setStatusTip('This just quits the application...')
        action.setShortcut('Ctrl+T')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(action)

        toolbar = self.addToolBar('Test')
        toolbar.addAction(action)

        self.resize(1100, 800)
        self.center()
        self.setWindowTitle('TWG Cueing System')
        self.statusBar().showMessage('Ready')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#    def closeEvent(self, event):
#        reply = QMessageBox.question(self, 'Message',
#            'Are you sure you want to quit?', QMessageBox.Yes | QMessageBox.No,
#            QMessageBox.No)
#        if reply == QMessageBox.Yes:
#            event.accept()
#        else:
#            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'poo.png')
    icon = QIcon(path)
    app.setWindowIcon(icon)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
