"""
CueList model classes

Author: Eric Sluyter
Last edited: July 2018
"""

class MediaInfo:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

class BusCue:
    def __init__(self, media_index=None, pos=None, speed=None, ramp_time=None,
            zoom=None, db=None):
        self.media_index = None if media_index == 'n' else media_index
        self.pos = None if pos == 'n' else pos
        self.speed = None if speed == 'n' else speed
        self.ramp_time = None if ramp_time == 'n' else ramp_time
        self.zoom = None if zoom == 'n' else zoom
        self.db = None if db == 'n' else db

class AudioRouting:
    def __init__(self):
        #TODO: fill with empty matrix state
        pass

    def __init__(self, matrix_state):
        self.matrix_state = matrix_state

class Cue:
    def __init__(self, csv_row):
        self.name = csv_row.pop(0)
        self.buses = [
            BusCue(csv_row.pop(0), csv_row.pop(0), csv_row.pop(0), csv_row.pop(0),
                csv_row.pop(0), csv_row.pop(0)),
            BusCue(csv_row.pop(0), csv_row.pop(0), csv_row.pop(0), csv_row.pop(0),
                csv_row.pop(0), csv_row.pop(0)),
            BusCue(csv_row.pop(0), csv_row.pop(0), csv_row.pop(0), csv_row.pop(0),
                csv_row.pop(0), csv_row.pop(0)),
            BusCue(csv_row.pop(0), csv_row.pop(0), csv_row.pop(0), csv_row.pop(0),
                csv_row.pop(0), csv_row.pop(0)),
            BusCue(csv_row.pop(0), csv_row.pop(0), csv_row.pop(0), csv_row.pop(0),
                csv_row.pop(0), csv_row.pop(0))
        ]
        self.notes = csv_row.pop(0)
        self.audio_routing = AudioRouting(csv_row.pop(0))

    def __init__(self, name, buses, notes, audio_routing):
        self.name = name
        self.buses = buses
        self.notes = notes
        self.audio_routing = audio_routing

class BusState:
    def __init__(self):
        self.media_index = 0
        self.pos = 0.0
        self.active = False

class CueList:
    def __init__(self, path=None):
        self.cue_pointer = None
        self.bus_states = [BusState(), BusState(), BusState(), BusState(), BusState()]
        self.current_routing = AudioRouting()
        self.fire_cue_on_update = False
        if (path is not None):
            self.load_path(path)

    def load_path(self, path):
        self.path = path
        self.cue_pointer = 0
        self.load_cues()
        self.load_media_info()

    def load_cues(self):
        #TODO: load cues
        pass

    def load_media_info(self):
        #TODO: load media info
        pass

    def update_media_info(self, data):
        #TODO: update media info and write it to disk
        pass

    def write_media_info(self):
        #TODO: write media info to file
        pass

    def set_bus_pos(self, index, pos):
        self.bus_states[index].pos = pos

    def set_bus_media(self, index, media_index):
        self.bus_states[index].media_index = media_index

    def set_bus_active(self, index, active):
        self.bus_states[index].active = active

    def goto_cue(self, index):
        self.cue_pointer = index

    def current_cue(self):
        #TODO: implement, return copy of cue
        pass

    def increment_cue(self):
        pass

    def decrement_cue(self):
        pass

    def replace_current_cue(self, cue):
        pass

    def add_cue_after_current(self, cue, name):
        pass

    def add_cue_before_current(self, cue, name):
        pass

    def add_empty_cue_after_current(self, name):
        pass

    def add_empty_cue_before_current(self, name):
        pass

    def rename_current_cue(self, name):
        pass

    def delete_current_cue(self, name):
        pass

    def fire_current_cue(self, name):
        pass
