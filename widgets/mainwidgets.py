"""
Custom compound widgets for TWG video cueing main window

- MainWidget
- MainWindow

Author: Eric Sluyter
Last edited: July 2018
"""

from widgets.buspanelwidgets import BusWidget, SoundPatchWidget
from widgets.cuelistwidgets import CueListWidget
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow, QToolTip, QAction,
    QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QDesktopWidget)
from PyQt5.QtGui import QFont, QIcon
from common.publisher import Publisher


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        self.list = CueListWidget()
        hbox.addWidget(self.list)

        vbox = QVBoxLayout()

        topstuff = QHBoxLayout()

        buttons = QVBoxLayout()
        buttons.setSpacing(0)
        buttons.addWidget(QPushButton('↑ Save as new cue before'))
        buttons.addWidget(QPushButton('Update cue'))
        buttons.addWidget(QPushButton('↓ Save as new cue after'))
        buttons.addSpacing(15)
        buttons.addWidget(QPushButton('+↑ Insert blank cue before'))
        buttons.addWidget(QPushButton('+↓ Insert blank cue after'))
        buttons.addSpacing(15)
        buttons.addWidget(QPushButton('⌫ Delete cue'))
        buttons.addWidget(QPushButton('✎ Rename cue'))
        topstuff.addLayout(buttons)

        midpanel = QVBoxLayout()
        midpanel.setSpacing(0)
        self.cue_name = QLabel('Cue Name')
        self.cue_name.setFont(QFont('SansSerif', 40))
        midpanel.addWidget(self.cue_name)
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

        self.notes = QTextEdit()
        #notes.setPlainText('They were waiting at the table')
        self.notes.setFont(QFont('SansSerif', 15, 100))
        topstuff.addWidget(self.notes)

        vbox.addLayout(topstuff)

        #vbox.addWidget(QHLine())

        self.buses = [BusWidget(letter) for letter in ['A', 'B', 'C', 'D', 'E']]
        buslayout = QHBoxLayout()
        for bus in self.buses:
            buslayout.addWidget(bus)
        self.sound = SoundPatchWidget()
        buslayout.addWidget(self.sound)
        vbox.addLayout(buslayout)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def set_cue_name(self, name):
        self.cue_name.setText(name)

    def set_notes(self, notes):
        self.notes.setPlainText(notes)

    def set_media_info(self, media_info):
        for bus in self.buses:
            bus.set_media_info(media_info)

class MainWindow(QMainWindow, Publisher):

    def __init__(self):
        QMainWindow.__init__(self)
        Publisher.__init__(self)
        self.role = 'view'
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.mainwidget = MainWidget()
        self.setCentralWidget(self.mainwidget)

        action = QAction(QIcon('icons/poo.png'), '&Test', self)
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
