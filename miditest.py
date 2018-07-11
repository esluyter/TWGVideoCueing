#!/usr/local/bin/python3

import rtmidi

alive = True

midiin = rtmidi.RtMidiIn()

def print_message(midi):
    if midi.isNoteOn():
        print('ON: ', midi.getNoteNumber(), midi.getVelocity())
    elif midi.isNoteOff():
        print('OFF:', midi.getNoteNumber())

def callback(delta, msg, data):
    print(delta, msg, data)

ports = range(midiin.getPortCount())
if ports:
    for i in ports:
        print(midiin.getPortName(i))
        if midiin.getPortName(i) == 'MPD218 Port A':
            print('Opening port %d!' % i)
            midiin.openPort(i)
    while alive:
        m = midiin.getMessage(250) # some timeout in ms
        if m:
            print_message(m)
else:
    print('NO MIDI INPUT PORTS!')
