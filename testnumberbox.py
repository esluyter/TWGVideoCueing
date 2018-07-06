#!/usr/local/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from widgets.littlewidgets import QNumberBox
from widgets.buswidgets import CuePositionWidget, CueSpeedWidget, CueVolumeWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = QWidget()
    #nb = QNumberBox(mw)
    #nb.move(200, 200)
    #nb = QNumberBox(mw)
    #nb.move(100, 100)

    l = QVBoxLayout()

    pw = CueVolumeWidget()
    pw1 = CueSpeedWidget()
    l.addWidget(pw)
    l.addWidget(pw1)

    pw1.setValue((2, 1))

    mw.setLayout(l)

    mw.show()
    sys.exit(app.exec_())
