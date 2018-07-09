"""
TWG Cueing System controller

Author: Eric Sluyter
Last edited: July 2018
"""

from os.path import basename
from pythonosc import udp_client, osc_server, dispatcher
import threading
import re

class CueController:
    def __init__(self, model, view):
        self.dispatcher = dispatcher.Dispatcher()
        #dispatcher.map('/filter', print)
        #dispatcher.map('/quit', quit)
        self.dispatcher.map('/db/*', self.db_update)
        self.dispatcher.map('/pos/*', self.pos_update)
        # must use 0.0.0.0 to receive OSC from anywhere
        self.server = osc_server.ThreadingOSCUDPServer(('0.0.0.0', 7400), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        self.client = udp_client.SimpleUDPClient('192.168.2.3', 7500)

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

    def pos_update(self, addr, pos):
        m = re.split(r'/pos/(\w)', addr)
        bus = ord(m[1]) - 65
        self.view.mainwidget.buses[bus].set_current_pos(pos)

    def db_update(self, addr, db):
        m = re.split(r'/db/(\w)/(\w)', addr)
        bus = ord(m[1]) - 65
        chan = m[2]
        if chan == 'l':
            self.view.mainwidget.sound.meters[bus].set_left_db(db)
        elif chan == 'r':
            self.view.mainwidget.sound.meters[bus].set_right_db(db)

    def model_update(self, what, etc):
        if what == 'cue_pointer':
            self.view_current_cue(True)
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
        if what == 'go':
            name, data = model.fire_current_cue(True)
            self.client.send_message('/fromsm', data)
            self.client.send_message('/isadora', ['/cuename', name])
        if what == 'quit':
            self.server.shutdown()

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
