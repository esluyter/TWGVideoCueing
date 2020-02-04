"""
MIDI implementation

Author: Eric Sluyter
Last edited: July 2018
"""

import rtmidi
from PyQt5.QtCore import QObject, pyqtSignal

class MidiWorker(QObject):
    noteOn = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, portName = 'MPD218'):
        super().__init__()
        self.midiin = rtmidi.RtMidiIn()
        self.portName = portName

    def listen(self):
        self.alive = False
        print('MIDI ports:')
        ports = range(self.midiin.getPortCount())
        if ports:
            for i in ports:
                if self.midiin.getPortName(i).startswith(self.portName):
                    self.alive = True
                    print(i, self.midiin.getPortName(i), ' - OPENING')
                    self.midiin.openPort(i)
                else:
                    print(i, self.midiin.getPortName(i))
            if self.alive:
                print('Port', repr(self.portName), 'open!')
            else:
                print('Port', repr(self.portName), 'not found.')
            while self.alive:
                m = self.midiin.getMessage(250) # some timeout in ms
                if m:
                    if m.isNoteOn():
                        self.noteOn.emit(m.getNoteNumber(), m.getVelocity())
        else:
            print('NO MIDI INPUT PORTS!')

        self.finished.emit()

    def stopListening(self):
        self.alive = False
