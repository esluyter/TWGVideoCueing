"""
Custom widgets for top panel

- CueListWidget

Author: Eric Sluyter
Last edited: July 2018
"""

from widgets.fonts import UIFonts
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
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
