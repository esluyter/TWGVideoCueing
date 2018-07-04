#!/usr/local/bin/python3

import sys
sys.path.append('widgets')

from pythonosc import dispatcher, osc_server
import threading

from painterwidgets import LevelMeter
from PyQt5.QtWidgets import QApplication



def quit(addr):
    global server, lm
    print('Quitting..')
    server.shutdown()
    lm.close()

def db(addr, l, r):
    global lm
    lm.set_dbs(l, r)

if __name__ == '__main__':
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map('/filter', print)
    dispatcher.map('/quit', quit)
    dispatcher.map('/db/*', db)

    server = osc_server.ThreadingOSCUDPServer(('localhost', 9001), dispatcher)
    print('Serving on {}'.format(server.server_address))
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    app = QApplication(sys.argv)
    lm = LevelMeter()
    lm.show()
    sys.exit(app.exec_())
