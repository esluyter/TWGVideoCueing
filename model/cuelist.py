"""
CueList model classes

- Media
- BusState
- BusCue
- AudioRouting
- Cue
- CueList

Author: Eric Sluyter
Last edited: July 2018
"""

import os
import csv
import re
from common.publisher import Publisher
from common.util import *


class Media:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __repr__(self):
        return "Media('%s', %s)" % (self.name, self.duration)

class BusState:
    def __init__(self, media_index=0, pos=0.0, active=False):
        self.media_index = media_index
        self.pos = pos
        self.active = active

    def __repr__(self):
        return "BusState(%s, %s, %s)" % (self.media_index, self.pos, self.active)

class BusCue:
    def __init__(self, media_index=None, pos=None, speed=None, ramp_time=None,
            zoom=None, db=None):
        self.media_index = None if media_index == 'n' or media_index is None else int(media_index)
        self.pos = None if pos == 'n' or pos is None else float(pos)
        self.speed = None if speed == 'n' or speed is None else float(speed)
        self.ramp_time = None if ramp_time == 'n' or ramp_time is None else float(ramp_time)
        self.zoom = None if zoom == 'n' or zoom is None else float(zoom)
        self.db = None if db == 'n' or db is None else float(db)

    def __repr__(self):
        return "BusCue(%s, %s, %s, %s, %s, %s)" % (self.media_index, self.pos,
            self.speed, self.ramp_time, self.zoom, self.db)

class AudioRouting:
    def __init__(self, matrix_state=None):
        if matrix_state is None:
            self.matrix_state = make_2d_list(5, 6, False)
        else:
            self.matrix_state = matrix_state

    @classmethod
    def from_csv_string(cls, string):
        matrix_state = make_2d_list(5, 6, False)
        for cell in clump(string.split(' '), 3):
            row = int(cell[0])
            col = int(cell[1])
            state = cell[2] == '1'
            matrix_state[row][col] = state
        return cls(matrix_state)

    def __repr__(self):
        return "AudioRouting(%s)" % self.matrix_state

    def at(self, row, col):
        return self.matrix_state[row][col]

class Cue:
    def __init__(self, name='', buses=None, notes='', audio_routing=None):
        self.name = name
        self.buses = [BusCue() for i in range(5)] if buses is None else buses
        self.notes = notes
        self.audio_routing = AudioRouting() if audio_routing is None else audio_routing

    @classmethod
    def from_csv_row(cls, csv_row):
        name = csv_row.pop(0)
        buses = [BusCue(*[csv_row.pop(0) for i in range(6)]) for j in range(5)]
        notes = csv_row.pop(0)
        audio_routing = AudioRouting.from_csv_string(csv_row.pop(0))
        return cls(name, buses, notes, audio_routing)

    def __repr__(self):
        return "Cue('%s', %s, '%s', %s)" % (self.name, self.buses, self.notes,
            self.audio_routing)

class CueList(Publisher):
    def __init__(self, path=None, rwff_speed=8.0):
        super().__init__()
        self.role = 'model'
        self.bus_states = [BusState() for i in range(5)]
        self.current_routing = AudioRouting()
        self.rwff_speed = rwff_speed
        self.load_path(path)

    def __repr__(self):
        return "<CueList path:'%s', fire_on_update:%s, media_info:%s, bus_states:%s, current_routing:%s, cues:%s>" % (self.path, self.fire_on_update, self.media_info, self.bus_states, self.current_routing, self.cues)

    def load_path(self, path):
        self.path = path
        self.cue_pointer = 0
        self.load_cues()
        self.load_media_info()

    def load_cues(self):
        if self.path is None:
            self.cues = [Cue('BLANK', [BusCue() for i in range(5)], '', AudioRouting())]
        else:
            self.cues = []
            with open(os.path.join(self.path, 'cues.csv'), 'r') as csv_file:
                reader = csv.reader(csv_file)
                next(reader) #skip header row
                for row in reader:
                    self.cues.append(Cue.from_csv_row(row))
        self.changed('cues')

    def write_cues(self):
        pass

    def load_media_info(self):
        self.media_info = {0: Media('BLANK', 0)}
        if self.path is not None:
            with open(os.path.join(self.path, 'mediainfo.txt'), 'r') as file:
                for line in file:
                    m = re.split(r'(\d+), "([^"]+)" ([\d\.]+);', line)
                    index = int(m[1])
                    name = m[2]
                    duration = float(m[3])
                    self.media_info[index] = Media(name, duration)
        self.changed('media_info')

    def update_media_info(self, data):
        #TODO: update media info and write it to disk
        pass

    def write_media_info(self):
        #TODO: write media info to file
        pass

    def set_bus_pos(self, index, pos):
        self.bus_states[index].pos = pos
        self.changed('bus' + index + 'pos')

    def set_bus_media(self, index, media_index):
        self.bus_states[index].media_index = media_index
        self.changed('bus' + index + 'media')

    def set_bus_active(self, index, active):
        self.bus_states[index].active = active
        self.changed('bus' + index + 'active')

    def goto_cue(self, index):
        self.cue_pointer = index % len(self.cues)
        self.changed('cue_pointer')

    def current_cue(self):
        return self.cues[self.cue_pointer]

    def increment_cue(self):
        self.cue_pointer = (self.cue_pointer + 1) % len(self.cues)
        self.changed('cue_pointer')

    def decrement_cue(self):
        self.cue_pointer = (self.cue_pointer - 1) % len(self.cues)
        self.changed('cue_pointer')

    def replace_current_cue(self, cue):
        self.cues[self.cue_pointer] = cue
        self.changed('cues')

    def add_cue_after_current(self, cue):
        self.cue_pointer += 1
        self.cues.insert(self.cue_pointer, cue)
        self.changed('cues')

    def add_cue_before_current(self, cue):
        self.cues.insert(self.cue_pointer, cue)
        self.changed('cues')

    def add_empty_cue_after_current(self, name):
        self.cue_pointer += 1
        self.cues.insert(self.cue_pointer, Cue(name))
        self.changed('cues')

    def add_empty_cue_before_current(self, name):
        self.cues.insert(self.cue_pointer, Cue(name))
        self.changed('cues')

    def rename_current_cue(self, name):
        self.current_cue().name = name
        self.changed('cue_name')

    def delete_current_cue(self):
        del self.cues[self.cue_pointer]
        self.changed('cues')

    def fire_current_cue(self, name):
        pass
