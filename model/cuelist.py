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

# this is a superclass that implements the Observer pattern
class Publisher:
    def __init__(self):
        self.subscribers = set()
    def register(self, who):
        self.subscribers.add(who)
    def unregister(self, who):
        self.subscribers.discard(who)
    def changed(self, what):
        self.subscribers.update(what)


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
    def __init__(self, media_index='n', pos='n', speed='n', ramp_time='n',
            zoom='n', db='n'):
        self.media_index = None if media_index == 'n' else int(media_index)
        self.pos = None if pos == 'n' else float(pos)
        self.speed = None if speed == 'n' else float(speed)
        self.ramp_time = None if ramp_time == 'n' else float(ramp_time)
        self.zoom = None if zoom == 'n' else float(zoom)
        self.db = None if db == 'n' else float(db)

    def __repr__(self):
        return "BusCue(%s, %s, %s, %s, %s, %s)" % (self.media_index, self.pos,
            self.speed, self.ramp_time, self.zoom, self.db)

class AudioRouting:
    def __init__(self, matrix_state=None):
        self.matrix_state = matrix_state

    def __repr__(self):
        return "AudioRouting(%s)" % self.matrix_state

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
        audio_routing = AudioRouting(csv_row.pop(0))
        return cls(name, buses, notes, audio_routing)

    def __repr__(self):
        return "Cue('%s', %s, '%s', %s)" % (self.name, self.buses, self.notes,
            self.audio_routing)

class CueList(Publisher):
    def __init__(self, path=None, fire_on_update=False):
        super().__init__()
        self.bus_states = [BusState() for i in range(5)]
        self.current_routing = AudioRouting()
        self.fire_on_update = fire_on_update
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
        self.changed('cues')

    def delete_current_cue(self):
        del self.cues[self.cue_pointer]
        self.changed('cues')

    def fire_current_cue(self, name):
        pass