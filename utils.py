import sys
import json
import main
from PyQt5 import QtCore


class Record:
    # Empty class, serves as a "record" in Pascal or a "struct" in C/C++.
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


class ConsoleListener(QtCore.QObject):
    newline = QtCore.pyqtSignal(str)

    def listen(self):
        while True:
            line = sys.stdin.readline().strip()
            if line:
                self.newline.emit(line)