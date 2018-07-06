"""
TWG Cueing System controller

Author: Eric Sluyter
Last edited: July 2018
"""

class CueController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        model.register(self)
        view.register(self)
        view.mainwidget.list.register(self)
        self.set_media_info()
        self.view_cues()
        self.view_current_cue()

    def model_update(self, what, etc):
        if what == 'cue_pointer':
            self.view_current_cue()

    def view_update(self, what, etc):
        model = self.model
        if what == 'cue_pointer' and etc != model.cue_pointer:
            model.goto_cue(etc)

    def set_media_info(self):
        self.view.mainwidget.set_media_info(self.model.media_info)

    def view_cues(self):
        self.view.mainwidget.list.set_cues([cue.name for cue in self.model.cues])

    def view_current_cue(self):
        current_cue = self.model.current_cue()
        mainwidget = self.view.mainwidget
        mainwidget.list.set_current_cue(self.model.cue_pointer)
        mainwidget.set_cue_name(current_cue.name)
        mainwidget.set_notes(current_cue.notes)
        for i, bus in enumerate(current_cue.buses):
            mainwidget.buses[i].set_values(bus)
        mainwidget.sound.set_cue_routing(current_cue.audio_routing)
