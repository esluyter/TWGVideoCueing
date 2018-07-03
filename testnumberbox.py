#!/usr/local/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from littlewidgets import QNumberBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = QWidget()
    nb = QNumberBox(mw)
    nb.move(200, 200)
    nb = QNumberBox(mw)
    nb.move(100, 100)
    mw.show()
    sys.exit(app.exec_())
