#!/usr/bin/python3
import sys
import importlib
import json
import codecs
from PySide2 import QtCore
import log

# On core starting:
# load config
# load plugins (construct instances of plugin entrance, they connect necessary signals)
# create process for mc server and connect listener
# start mc server (with server_start signal emitted)

# On core running
# record server output and emit signal
# receive keyboard input, emit signal and send to server
# provide methods for server status query and operation

# On core quiting
# stop server and emit server_stop
# destruct instances of plugin entrance
# stop event loop


class Core(QtCore.QObject):
    server_start = QtCore.Signal()
    server_stop = QtCore.Signal()
    server_newlog = QtCore.Signal(list)
    core_quit = QtCore.Signal()

    def __init__(self, config):
        super(Core, self).__init__()
        self.config = config
        self.logger = log.Logger('mana9er', self.config.log_level)
        self.server_running = False
        self.server = None
        self.server_logs = []
        for plugin_name in self.config.plugin_names:
            importlib.import_module(plugin_name + '.entrance').entrance(self)
        self.start_server()

    def start_server(self, cmd = None):
        if self.server_running:
            self.logger.warning('Core.start_server called while server is running')
            return
        if not cmd:
            cmd = self.config.default_entrance
        self.server = QtCore.QProcess()
        self.server.readyRead.connect(self.on_server_newlog)
        self.server.finished.connect(self.on_server_stop)
        self.server.start(cmd)
        self.server_running = True
        self.server_start.emit()

    def stop_server(self):
        if not self.server_running:
            self.logger.warning('Core.stop_server called while server is not running')
            return
        self.server.write('stop\n')

    @QtCore.Slot()
    def on_server_newlog(self):
        server_outputs = QtCore.QTextStream(self.server)
        new_lines = server_outputs.readAll().splitlines()
        for line in new_lines:
            self.server_logs.append(line)
            self.logger.server_output(line)
        self.server_newlog.emit(new_lines)

    @QtCore.Slot()
    def on_server_stop(self):
        self.server_running = False
        self.server = None
        self.server_stop.emit()

    def quit(self):
        if self.server_running:
            self.stop_server()
            self.server.waitForFinished()  # self.on_server_stop called and self.server_stop emitted
        self.server_newlog.disconnect()
        self.server_start.disconnect()
        self.server_stop.disconnect()
        self.core_quit.emit()

