#!/usr/local/bin/python3

"""
Testing the Python implementation of TWG Cueing System

Author: Eric Sluyter
Last edited: July 2018
"""

import sys, os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from widgets.mainwidgets import MainWindow
from model.cuelist import CueList
from controller.controller import CueController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icons/poo.png')
    icon = QIcon(path)
    app.setWindowIcon(icon)

    model = CueList('../TTHA')
    view = MainWindow()
    controller = CueController(model, view)

    view.show()
    sys.exit(app.exec_())
