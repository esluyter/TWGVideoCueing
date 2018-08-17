#!/usr/local/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from widgets.littlewidgets import QNumberBox
from widgets.buswidgets import CueMediaWidget, CueSpeedWidget, CueVolumeWidget
from model.cuelist import Media

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = QWidget()
    #nb = QNumberBox(mw)
    #nb.move(200, 200)
    #nb = QNumberBox(mw)
    #nb.move(100, 100)

    l = QVBoxLayout()

    pw = CueMediaWidget()
    pw1 = CueSpeedWidget()

    media_info = {0: Media('BLANK', 0), 1: Media('ISNR', 200.1), 3: Media('TBH pt 1', 34.56)}
    pw.set_media_info(media_info)
    pw.setValue(3)

    l.addWidget(pw)
    l.addWidget(pw1)

    pw1.setValue((2, 1))

    mw.setLayout(l)

    mw.show()
    sys.exit(app.exec_())
