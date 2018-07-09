"""
TWG Cueing System controller

Author: Eric Sluyter
Last edited: July 2018
"""

from os.path import basename

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
        if what == 'path':
            if etc is None:
                self.view.setWindowTitle('New Cue List')
            else:
                self.view.setWindowTitle(basename(etc))
                self.view.setWindowModified(False)
        if what == 'unsaved_changes':
            self.view.setWindowModified(True)

    def view_update(self, what, etc):
        model = self.model
        view = self.view
        if what == 'cue_pointer' and etc != model.cue_pointer:
            if (view.confirm_cue_change()):
                model.goto_cue(etc)
        if what == 'cue_name' and etc != model.current_cue().name:
            model.rename_current_cue(etc)
        if what == 'blank_before':
            model.add_empty_cue_before_current('BLANK')
        if what == 'blank_after':
            model.add_empty_cue_after_current('BLANK')
        if what == 'delete_current':
            model.delete_current_cue()
        if what == 'update':
            model.replace_current_cue(view.mainwidget.as_cue())
        if what == 'update_fire':
            model.replace_current_cue(view.mainwidget.as_cue())
        if what == 'insert_before':
            name, ok = view.get_text('New cue name', 'New cue name:')
            if ok:
                model.add_cue_before_current(view.mainwidget.as_cue(name))
        if what == 'insert_after':
            name, ok = view.get_text('New cue name', 'New cue name:')
            if ok:
                model.add_cue_after_current(view.mainwidget.as_cue(name))
        if what == 'rwff_speed' and etc != model.rwff_speed:
            model.rwff_speed = etc
        if what == 'edited':
            view.mainwidget.buttons.setEdited(view.mainwidget.edited())
        if what == 'open':
            model.load_path(etc)
        if what == 'new':
            model.load_path(None)
        if what == 'save':
            if model.path is None:
                view.save_as()
            else:
                if view.mainwidget.edited():
                    model.replace_current_cue(view.mainwidget.as_cue())
        if what == 'save_as':
            model.save_as(etc)

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
