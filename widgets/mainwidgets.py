"""
Custom compound widgets for TWG video cueing main window

- MainWidget
- MainWindow

Author: Eric Sluyter
Last edited: July 2018
"""

from buspanelwidgets import BusWidget, SoundPatchWidget
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow, QToolTip, QAction,
    QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QDesktopWidget, QListView)
from PyQt5.QtGui import QFont, QIcon, QStandardItemModel, QStandardItem
#from PyQt5.QtCore import Qt


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
        list.setFont(QFont('SansSerif', 15))

        hbox.addWidget(list)

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
        cue_name = QLabel('Cue Name')
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
        #notes.setPlainText('They were waiting at the table')
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
