#!/usr/bin/python3
import sys
import importlib
import json
import codecs
from PySide2 import QtCore

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


def wrap_config(config):
    res = object()
    res.default_entrance = config['default_entrance']
    res.plugin_names = config['plugins']
    return res


class Core(QtCore.QObject):
    server_start = QtCore.Signal()
    server_stop = QtCore.Signal()
    server_newlog = QtCore.Signal(list)

    def __init__(self, config_filename, app):
        super(Core, self).__init__()
        self.app = app
        self.server_running = False
        self.server = None
        self.quit_flag = False
        self.config = wrap_config(json.load(codecs.open(config_filename, mode='r', encoding='utf-8')))
        self.server_logs = []
        self.plugins = []
        for plugin_name in self.config.plugin_names:
            self.plugins.append(importlib.import_module(plugin_name + '.entrance').entrance(self))
        self.start_server()

    def start_server(self, cmd = None):
        if self.server_running:
            logger.warning('Core.start_server called while server is running')
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
            logger.warning('Core.stop_server called while server is not running')
            return
        self.server.write('stop\n')

    def on_server_newlog(self):
        newlog = self.server.readAll().data().decode('utf-8').splitlines()
        for line in newlog:
            self.server_logs.append(line)
            logger.server_output(line)
        self.server_newlog.emit(newlog)

    def on_server_stop(self):
        self.server_running = False
        self.server = None
        self.server_stop.emit()
        if self.quit_flag: self.safe_quit()

    def safe_quit(self):
        self.plugins.clear()
        self.app.quit()

    def quit(self):
        if self.server_running:
            self.quit_flag = True
            self.stop_server()
            return
        else: self.safe_quit()


if __name__ == '__main__':
    app = QtCore.QCoreApplication()
    core = Core('config.json', app)
    sys.exit(app.exec_())
