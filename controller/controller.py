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
        view.mainwidget.register(self)
        view.mainwidget.list.register(self)
        view.mainwidget.buttons.register(self)
        view.mainwidget.midpanel.register(self)
        self.view_media_info()
        self.view_rwff_speed()
        self.view_cues()
        self.view_current_cue()

    def model_update(self, what, etc):
        if what == 'cue_pointer':
            self.view_current_cue()
        if what == 'cues':
            self.view_cues(True)
            self.view_current_cue(True)
        if what == 'cue_name':
            self.view_cues()
            self.view_current_cue_name()
        if what == 'media_info':
            self.view_media_info()

    def view_update(self, what, etc):
        model = self.model
        view = self.view
        if what == 'cue_pointer' and etc != model.cue_pointer:
            model.goto_cue(etc)
        if what == 'cue_name' and etc != model.current_cue().name:
            model.rename_current_cue(etc)
        if what == 'blank_before':
            model.add_empty_cue_before_current('BLANK')
        if what == 'blank_after':
            model.add_empty_cue_after_current('BLANK')
        if what == 'delete_current':
            model.delete_current_cue()
        if what == 'rwff_speed' and etc != model.rwff_speed:
            model.rwff_speed = etc
        if what == 'edited':
            edited = False
            for bus in view.mainwidget.buses:
                if bus.edited():
                    edited = True
            if view.mainwidget.sound.edited():
                edited = True
            if view.mainwidget.notes.edited:
                edited = True
            view.mainwidget.buttons.setEdited(edited)

    def view_media_info(self):
        self.view.mainwidget.set_media_info(self.model.media_info)

    def view_rwff_speed(self):
        self.view.mainwidget.midpanel.set_rwff_speed(self.model.rwff_speed)

    def view_cues(self, flush=False):
        if flush:
            self.view.mainwidget.list.hide()
        self.view.mainwidget.list.set_cues([cue.name for cue in self.model.cues])
        if flush:
            self.view.mainwidget.list.show()

    def view_current_cue_name(self, flush=False):
        self.view.mainwidget.set_cue_name(self.model.current_cue().name)
        self.view.mainwidget.list.set_current_cue(self.model.cue_pointer)

    def view_current_cue(self, flush=False):
        current_cue = self.model.current_cue()
        mainwidget = self.view.mainwidget

        if flush:
            mainwidget.hide()

        self.view_current_cue_name()
        mainwidget.set_notes(current_cue.notes)
        for i, bus in enumerate(current_cue.buses):
            mainwidget.buses[i].set_values(bus)
        mainwidget.sound.set_cue_routing(current_cue.audio_routing)

        if flush:
            mainwidget.show()
