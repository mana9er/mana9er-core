import sys
import json
import main
from PyQt5 import QtCore


class Record:
    pass


class Config:
    def __init__(self, config_dict):
        self.default_entrance = Record()
        self.default_entrance.wd = config_dict['default_entrance']['wd']
        self.default_entrance.exec = config_dict['default_entrance']['exec']
        self.plugin_names = config_dict['plugins']
        if 'log_level' in config_dict:
            self.log_level = config_dict['log_level']
        else:
            self.log_level = 1  # INFO level
        self.prefix = config_dict['prefix']


class Player:
    def __init__(self, name):
        self.name = name

    def is_console(self):
        return False

    def is_op(self):
        if self.is_console(): return True
        try:
            with open('ops.json', 'r', encoding='utf-8') as op_file:
                ops = json.load(op_file)
                for op in ops:
                    if op['name'] == self.name:
                        return True
                return False
        except (OSError, IOError):
            main.core_inst.logger.error('Fail to open ops.json when checking op permission. \
             This is probably caused by a wrong working directory or an old version of minecraft server')
            return False


class GhostingPlayer(Player):
    def __init__(self):
        super(GhostingPlayer, self).__init__('CONSOLE')

    def is_console(self):
        return True


class ConsoleListener(QtCore.QObject):
    newline = QtCore.pyqtSignal(str)

    def listen(self):
        while True:
            line = sys.stdin.readline().strip()
            if line:
                self.newline.emit(line)