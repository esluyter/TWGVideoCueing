"""
Custom compound widgets for TWG video cueing main window

- MainWidget
- MainWindow

Author: Eric Sluyter
Last edited: July 2018
"""

from widgets.buspanelwidgets import BusWidget, SoundPatchWidget
from widgets.cuelistwidgets import CueListWidget, CueButtonsLayout, CueMidpanelLayout
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow, QToolTip, QAction,
    QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QDesktopWidget, QSizePolicy)
from PyQt5.QtGui import QFont, QIcon
from common.publisher import Publisher
from widgets.fonts import UIFonts


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

        self.buttons = CueButtonsLayout()
        topstuff.addLayout(self.buttons)

        self.midpanel = CueMidpanelLayout()
        topstuff.addLayout(self.midpanel)

        self.notes = QTextEdit()
        self.notes.setFont(UIFonts.notes_font)
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
        self.midpanel.cue_name.setText(name)

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
