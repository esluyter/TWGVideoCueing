"""
Custom compound widgets for TWG video cueing main window

- MainWidget
- MainWindow

Author: Eric Sluyter
Last edited: July 2018
"""

from model.cuelist import Cue
from widgets.buspanelwidgets import BusWidget, SoundPatchWidget
from widgets.cuelistwidgets import (CueListWidget, CueButtonsLayout,
    CueMidpanelLayout, CueNotesWidget)
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow, QToolTip, QAction,
    QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QDesktopWidget, QSizePolicy,
    QInputDialog, QMessageBox, QFileDialog)
from PyQt5.QtGui import QFont, QIcon
from common.publisher import Publisher
from widgets.fonts import UIFonts
from os.path import expanduser


class MainWidget(QWidget, Publisher):
    def __init__(self):
        QWidget.__init__(self)
        Publisher.__init__(self)
        self.role = 'view'
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

        self.notes = CueNotesWidget()
        self.notes.register(self)
        topstuff.addWidget(self.notes)

        vbox.addLayout(topstuff)

        #vbox.addWidget(QHLine())

        self.buses = [BusWidget(letter) for letter in ['A', 'B', 'C', 'D', 'E']]
        buslayout = QHBoxLayout()
        for bus in self.buses:
            buslayout.addWidget(bus)
            bus.register(self)
        self.sound = SoundPatchWidget()
        self.sound.register(self)
        buslayout.addWidget(self.sound)
        vbox.addLayout(buslayout)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def edited(self):
        edited = False
        for bus in self.buses:
            if bus.edited():
                edited = True
        if self.sound.edited():
            edited = True
        if self.notes.edited:
            edited = True
        return edited

    def view_update(self, what, etc):
        if what == 'edited':
            self.changed('edited')

    def set_cue_name(self, name):
        self.midpanel.cue_name.setText(name)

    def set_notes(self, notes):
        self.notes.setPlainText(notes)

    def set_media_info(self, media_info):
        for bus in self.buses:
            bus.set_media_info(media_info)

    def as_cue(self, name=None):
        name = self.midpanel.cue_name.text() if name is None else name
        buses = [bus.as_bus_cue() for bus in self.buses]
        notes = self.notes.toPlainText()
        sound = self.sound.as_audio_routing()
        return Cue(name, buses, notes, sound)

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

        new = QAction(QIcon('icons/document-empty.png'), '&New Cue List', self)
        new.triggered.connect(self.new)
        new.setShortcut('Ctrl+N')

        open = QAction(QIcon('icons/open-folder.png'), '&Open Cue List...', self)
        open.triggered.connect(self.open)
        open.setShortcut('Ctrl+O')

        refresh = QAction(QIcon('icons/refresh.png'), '&Refresh Cue List', self)
        refresh.triggered.connect(self.refresh)
        refresh.setShortcut('Ctrl+R')

        save = QAction(QIcon('icons/floppy-disk.png'), '&Save', self)
        save.triggered.connect(self.save)
        save.setShortcut('Ctrl+S')

        save_as = QAction(QIcon('icons/floppy-disks-pair.png'), '&Save As...', self)
        save_as.triggered.connect(self.save_as)
        save_as.setShortcut('Shift+Ctrl+S')

        close = QAction(QIcon('icons/door-exit.png'), '&Close', self)
        close.triggered.connect(self.close)
        close.setShortcut('Ctrl+W')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(new)
        fileMenu.addAction(open)
        #fileMenu.addAction(refresh)
        fileMenu.addSeparator()
        fileMenu.addAction(save)
        fileMenu.addAction(save_as)
        fileMenu.addSeparator()
        fileMenu.addAction(close)

        toolbar = self.addToolBar('Util')
        toolbar.addAction(new)
        toolbar.addAction(open)
        #toolbar.addAction(refresh)
        toolbar.addSeparator()
        toolbar.addAction(save)
        toolbar.addSeparator()
        toolbar.addAction(close)

        self.resize(1100, 800)
        self.center()
        self.setWindowTitle('New Cue List')
        self.statusBar().showMessage('Ready')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_text(self, title, label):
        return QInputDialog.getText(self, title, label)

    def new(self):
        if self.confirm_close():
            self.changed('new')

    def open(self):
        if self.confirm_close():
            filename = QFileDialog.getExistingDirectory(self, '', expanduser('data'))
            if filename != '':
                self.changed('open', filename)

    def refresh(self):
        return None

    def save(self):
        self.changed('save')

    def save_as(self):
        filename = QFileDialog.getSaveFileName(self, '', expanduser('data'))[0]
        if filename != '':
            self.changed('save_as', filename)

    def confirm_cue_change(self):
        if self.mainwidget.edited():
            reply = QMessageBox.question(self, 'Message',
                'There are unsaved edits, are you sure you want to change cues?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
            if reply == QMessageBox.Yes:
                return True
            else:
                return False
        else:
            return True

    def confirm_close(self):
        if self.mainwidget.edited() or self.isWindowModified():
            reply = QMessageBox.question(self, 'Message',
                'There are unsaved changes, are you sure you want to close?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
            if reply == QMessageBox.Yes:
                return True
            else:
                return False
        else:
            return True

    def closeEvent(self, event):
        if self.confirm_close():
            event.accept()
        else:
            event.ignore()
