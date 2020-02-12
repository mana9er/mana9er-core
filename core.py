#!/usr/bin/python3
import sys
import importlib
from PyQt5 import QtCore
import log
import listener

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
    sig_server_start = QtCore.pyqtSignal()
    sig_server_stop = QtCore.pyqtSignal()
    sig_server_output = QtCore.pyqtSignal(list)
    sig_command = QtCore.pyqtSignal(str)
    core_quit = QtCore.pyqtSignal()

    def __init__(self, config):
        super(Core, self).__init__()
        self.config = config
        self.logger = log.Logger('mana9er', self.config.log_level)
        self.server_running = False
        self.server = None
        self.server_logs = []
        console_listener = listener.ConsoleListener(self)
        console_listener.newline.connect(self.command)
        console_listener.eof_input.connect(self.on_eof_input)
        for plugin_name in self.config.plugin_names:
            importlib.import_module(plugin_name + '.entrance').Entrance(self)
        self.builtin_callback = self.get_builtin_callback()
        self.start_server()

    def get_builtin_callback(self):
        return dict(quit=self.quit)

    def start_server(self, cmd = None):
        if self.server_running:
            self.logger.warning('Core.start_server called while server is running')
            return
        if not cmd:
            cmd = self.config.default_entrance
        self.server = QtCore.QProcess()
        self.server.readyRead.connect(self.on_server_output)
        self.server.finished.connect(self.on_server_stop)
        self.server.start(cmd)
        self.server_running = True  # TODO: add success check
        self.sig_server_start.emit()

    def write_server(self, content):
        content += '\n'
        if self.server_running:
            self.server.write(bytes(content, encoding='utf-8'))
        else:
            self.logger.warning('core.write_server called while the server is not running')

    def stop_server(self):
        if not self.server_running:
            self.logger.warning('Core.stop_server called while server is not running')
            return
        self.write_server('stop')

    @QtCore.pyqtSlot()
    def on_server_output(self):
        server_outputs = QtCore.QTextStream(self.server)
        new_lines = server_outputs.readAll().splitlines()
        for line in new_lines:
            self.server_logs.append(line)
            self.logger.server_output(line)
        self.sig_server_output.emit(new_lines)

    @QtCore.pyqtSlot()
    def on_server_stop(self):
        self.server_running = False
        self.server = None
        self.sig_server_stop.emit()

    def quit(self):
        self.logger.debug('core.quit called')
        self.logger.info('Quiting...')
        if self.server_running:
            self.logger.info('The server is running, stopping server first')
            self.stop_server()
            self.server.waitForFinished()  # self.on_server_stop called and self.sig_server_stop emitted
            self.logger.info('The server has been stopped')
        self.logger.info('Safe quiting...')
        self.logger.debug('disconnecting all the signals')
        self.sig_server_output.disconnect()
        self.sig_server_start.disconnect()
        self.sig_server_stop.disconnect()
        self.logger.debug('core.core_quit emitted, event loop is going to stop')
        self.core_quit.emit()

    def builtin_cmd(self, cmd):
        for key in self.builtin_callback:
            if cmd == self.config.prefix + key:
                self.builtin_callback[key]()

    @QtCore.pyqtSlot(str)
    def command(self, cmd):
        if cmd.startswith(self.config.prefix):
            self.builtin_cmd(cmd)
        else:
            self.write_server(cmd)
        self.sig_command.emit(cmd)

    @QtCore.pyqtSlot()
    def on_eof_input(self):
        self.logger.warning('EOF read from console. Type {}quit to exit mana9er'.format(self.config.prefix))
