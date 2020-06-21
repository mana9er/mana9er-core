import os
import sys
import importlib
from PyQt5 import QtCore
import log
import utils
import notifier

# On core starting:
# load config
# load plugins (construct instances of plugin, they connect necessary signals)
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

    def __init__(self, config):
        super(Core, self).__init__()
        self.config = config

    @QtCore.pyqtSlot()
    def init(self):
        self.init_cwd = os.getcwd()
        self.server_running = False
        self.server = None
        self.server_logs = []

        self.notifier = notifier.Notifier()
        self.sig_command.connect(self.notifier.on_command)
        self.sig_server_output.connect(self.notifier.on_server_output)

        stdout_profile = utils.Record()
        stdout_profile.level = self.config.log_level
        stdout_profile.output = sys.stdout
        log_profiles = [stdout_profile]
        self.logger = log.Logger('mana9er', log_profiles)
        self.logger.sig_output.connect(self.notifier.sig_output)

        # load plugins
        for plugin_name in self.config.plugin_names:
            plugin_logger = log.Logger(plugin_name, log_profiles)
            plugin_logger.sig_output.connect(self.notifier.sig_output)
            importlib.import_module(plugin_name).load(plugin_logger, self)  # import plugins, call init function
        self.build_builtin_callback()
        self.start_server()

    def build_builtin_callback(self):
        # Callback functions provided by Core itself
        self.builtin_callback = dict(
            start=self.start_server,
            stop=self.stop_server,
            restart=self.restart_server,
            quit=self.quit
        )

    def start_server(self, entrance=None):
        self.logger.debug('core.start_server called')
        if self.server_running:
            self.logger.warning('Core.start_server called while server is running')
            return
        self.logger.info('Starting server...')
        if not entrance:
            entrance = self.config.default_entrance
        os.chdir(self.init_cwd)
        os.chdir(entrance.wd)
        self.server = QtCore.QProcess()
        self.server.readyRead.connect(self.on_server_output)
        self.server.finished.connect(self.on_server_stop)
        self.server.start(entrance.exec)
        self.server_running = True  # TODO: add success check
        self.sig_server_start.emit()

    def write_server(self, content):
        self.logger.debug('core.write_server called')
        content += '\n'
        if self.server_running:
            self.server.write(bytes(content, encoding='utf-8'))
        else:
            self.logger.warning('core.write_server called while the server is not running')

    def stop_server(self):
        self.logger.debug('core.stop_server called')
        if not self.server_running:
            self.logger.warning('Core.stop_server called while server is not running')
            return
        self.logger.info('Stopping server...')
        self.write_server('stop')

    def restart_server(self):
        self.logger.debug('core.restart_server called')
        self.logger.info('Restarting server...')
        self.stop_server()
        self.server.waitForFinished()  # self.on_server_stop called and self.sig_server_stop emitted
        self.start_server()

    @QtCore.pyqtSlot()
    def on_server_output(self):
        self.logger.debug('core.on_server_output called')
        server_outputs = QtCore.QTextStream(self.server)
        new_lines = server_outputs.readAll().splitlines()
        for line in new_lines:
            self.server_logs.append(line)
            self.logger.direct_output(line)
        self.sig_server_output.emit(new_lines)

    @QtCore.pyqtSlot()
    def on_server_stop(self):
        self.logger.debug('self.on_server_stop called')
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
        sys.exit(0)

    def builtin_cmd(self, cmd):
        self.logger.debug('core.builtin_cmd called with cmd={}'.format(cmd))
        for key in self.builtin_callback:
            if cmd == self.config.prefix + key:
                self.builtin_callback[key]()

    @QtCore.pyqtSlot(str)
    def command(self, cmd):
        self.logger.debug('core.command called')
        if cmd.startswith(self.config.prefix):
            self.builtin_cmd(cmd)
        else:
            self.write_server(cmd)
        self.sig_command.emit(cmd)
