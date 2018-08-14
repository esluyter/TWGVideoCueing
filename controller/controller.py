"""
TWG Cueing System controller

Author: Eric Sluyter
Last edited: July 2018
"""

from controller.midi import MidiWorker
from PyQt5.QtCore import QThread
from os.path import basename, normpath, expanduser
from pythonosc import udp_client, osc_server, dispatcher
import threading
import re

class CueController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        model.register(self)
        for bus_state in model.bus_states:
            bus_state.register(self)
        view.register(self)
        view.mainwidget.register(self)
        view.mainwidget.list.register(self)
        view.mainwidget.buttons.register(self)
        view.mainwidget.midpanel.register(self)

        self.start_osc()

        self.midi_worker = MidiWorker()
        self.midi_thread = QThread()
        self.midi_worker.noteOn.connect(self.noteOn)
        self.midi_worker.moveToThread(self.midi_thread)
        self.midi_worker.finished.connect(self.midi_thread.quit)
        self.midi_thread.started.connect(self.midi_worker.listen)
        self.midi_thread.start()

        self.view_media_info()
        self.view_rwff_speed()
        self.view_cues()
        self.view_current_cue()

    def start_osc(self, start_server=True):
        with open(expanduser('data/settings.txt'), 'r') as file:
            contents = file.readlines()
            self.server_port = int(contents[0])
            client_info = contents[1].split(',')
            self.client_ip = client_info[0]
            self.client_port = int(client_info[1])

        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map('/db/*', self.db_update)
        self.dispatcher.map('/pos/*', self.pos_update)
        self.dispatcher.map('/matrix', self.matrix_update)
        if start_server:
            # must use 0.0.0.0 to receive OSC from anywhere
            self.server = osc_server.ThreadingOSCUDPServer(('0.0.0.0', self.server_port), self.dispatcher)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.start()
        #self.client = udp_client.SimpleUDPClient('192.168.2.3', 7500)
        self.client = udp_client.SimpleUDPClient(self.client_ip, self.client_port)
        # this seems necessary to prime the pump
        try:
            self.client.send_message('/dummy', 0)
            self.blank_all()
        except:
            print('OSC error!')

    def restart_osc(self, server_port, client_ip, client_port):
        with open(expanduser('data/settings.txt'), 'w') as file:
            file.write('%d\n' % server_port)
            file.write('%s,%d\n' % (client_ip, client_port))
        if server_port != self.server_port:
            self.server.shutdown()
            self.start_osc()
        else:
            self.start_osc(False)


    def noteOn(self, num, vel):
        {
            36: lambda: self.play_bus(0),
            37: lambda: self.pause_bus(0),
            38: lambda: self.play_bus(1),
            39: lambda: self.pause_bus(1),
            40: lambda: self.rw_bus(0),
            41: lambda: self.ff_bus(0),
            42: lambda: self.rw_bus(1),
            43: lambda: self.ff_bus(1),
            46: self.pause_all,
            47: lambda: self.view_update('move_up'),
            48: self.rw_all,
            49: self.ff_all,
            50: self.play_all,
            51: self.fire_cue
        }.get(num, lambda: None)()

    def pos_update(self, addr, pos):
        m = re.split(r'/pos/(\w)', addr)
        bus = ord(m[1]) - 65
        self.model.bus_states[bus].set_pos(pos)

    def db_update(self, addr, db):
        m = re.split(r'/db/(\w)/(\w)', addr)
        bus = ord(m[1]) - 65
        chan = m[2]
        if chan == 'l':
            self.view.mainwidget.sound.meters[bus].set_left_db(db)
        elif chan == 'r':
            self.view.mainwidget.sound.meters[bus].set_right_db(db)

    def matrix_update(self, addr, i, j, state):
        self.view.mainwidget.sound.set_checkbox(i, j, state == 1)

    def model_update(self, what, etc=None):
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
                self.view.setWindowTitle(basename(normpath(etc)))
                self.view.setWindowModified(False)
        if what == 'unsaved_changes':
            self.view.setWindowModified(True)
        if what == 'pos':
            pos = self.model.bus_states[etc].pos
            self.view.mainwidget.buses[etc].set_current_pos(pos)
        if what == 'media':
            media_name = self.model.media_info[self.model.bus_states[etc].media_index].name
            self.view.mainwidget.buses[etc].set_current_media(media_name)
        if what == 'active':
            active = self.model.bus_states[etc].active
            self.view.mainwidget.buses[etc].set_active(active)

    def view_update(self, what, etc=None):
        model = self.model
        view = self.view
        if what == 'cue_pointer' and etc != model.cue_pointer:
            if view.confirm_cue_change():
                model.goto_cue(etc)
        if what == 'move_up':
            if view.confirm_cue_change():
                model.decrement_cue()
        if what == 'move_down':
            if view.confirm_cue_change():
                model.increment_cue()
        if what == 'cue_name' and etc != model.current_cue().name:
            model.rename_current_cue(etc)
        if what == 'blank_before':
            if view.confirm_cue_change():
                model.add_empty_cue_before_current('BLANK')
        if what == 'blank_after':
            if view.confirm_cue_change():
                model.add_empty_cue_after_current('BLANK')
        if what == 'delete_current':
            model.delete_current_cue()
        if what == 'update':
            model.replace_current_cue(view.mainwidget.as_cue())
        if what == 'update_fire':
            model.replace_current_cue(view.mainwidget.as_cue())
            self.fire_cue(False)
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
        if what == 'capture_all':
            for bus in view.mainwidget.buses:
                bus.current_pos.capture()
        if what == 'transport':
            self.client.send_message('/isadora', [etc, 1])
        if what == 'play':
            self.play_bus(etc)
        if what == 'pause':
            self.pause_bus(etc)
        if what == 'rw':
            self.rw_bus(etc)
        if what == 'ff':
            self.ff_bus(etc)
        if what == 'play_all':
            self.play_all()
        if what == 'pause_all':
            self.pause_all()
        if what == 'rw_all':
            self.rw_all()
        if what == 'ff_all':
            self.ff_all()
        if what == 'set_bus_pos':
            bus, pos = etc
            self.bus_pos(bus, pos)
        if what == 'current_matrix':
            self.client.send_message('/fromsm', etc)
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
            self.fire_cue(True)
        if what == 'settings':
            view.show_settings_dialog([self.server_port, self.client_ip, self.client_port], model.media_info)
        if what == 'new_settings':
            osc_settings, media_list = etc
            server_port, client_ip, client_port = osc_settings
            self.restart_osc(server_port, client_ip, client_port)
            model.update_media_info(media_list)
        if what == 'quit':
            self.server.shutdown()
            self.midi_worker.stopListening()

    def play_bus(self, bus):
        bus_state = self.model.bus_states[bus]
        if bus_state.active:
            self.bus_speed(bus, bus_state.speed)

    def pause_bus(self, bus):
        bus_state = self.model.bus_states[bus]
        if bus_state.active:
            self.bus_speed(bus, 0)

    def rw_bus(self, bus):
        bus_state = self.model.bus_states[bus]
        if bus_state.active:
            self.bus_speed(bus, -1 * self.model.rwff_speed)

    def ff_bus(self, bus):
        bus_state = self.model.bus_states[bus]
        if bus_state.active:
            self.bus_speed(bus, self.model.rwff_speed)

    def play_all(self):
        data = []
        for bus_state in self.model.bus_states:
            data += ['n'] * 2 + [str(bus_state.speed) + ' 0' if bus_state.active else 'n'] + ['n'] * 4
        self.client.send_message('/fromsm', data)

    def pause_all(self):
        data = []
        for bus_state in self.model.bus_states:
            data += ['n'] * 2 + ['0 0' if bus_state.active else 'n'] + ['n'] * 4
        self.client.send_message('/fromsm', data)

    def rw_all(self):
        data = []
        for bus_state in self.model.bus_states:
            data += ['n'] * 2 + [str(-1 * self.model.rwff_speed * bus_state.speed) + ' 0' if bus_state.active else 'n'] + ['n'] * 4
        self.client.send_message('/fromsm', data)

    def ff_all(self):
        data = []
        for bus_state in self.model.bus_states:
            data += ['n'] * 2 + [str(self.model.rwff_speed * bus_state.speed) + ' 0' if bus_state.active else 'n'] + ['n'] * 4
        self.client.send_message('/fromsm', data)

    def fire_cue(self, increment=True):
        name, data = self.model.fire_current_cue(increment)
        self.client.send_message('/fromsm', data)
        self.client.send_message('/isadora', ['/cuename', name])

    def bus_speed(self, bus, speed):
        # there must be a better way.... :)
        data = ['n'] * (bus * 7 + 2) + [str(speed) + ' 0']
        self.client.send_message('/fromsm', data)

    def bus_pos(self, bus, pos):
        data = ['n'] * (bus * 7 + 1) + [str(pos)]
        self.client.send_message('/fromsm', data)
        self.model.bus_states[bus].set_pos(pos)

    def blank_all(self):
        data = (['0'] + (['n'] * 6)) * 5
        self.client.send_message('/fromsm', data)

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
