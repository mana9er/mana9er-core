import os
import sys
import json
import time
import datetime
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
        self.log_level = config_dict.get('log_level', 1) # default to INFO level
        self.prefix = config_dict['prefix']
        self.log_keep_days = config_dict.get('log_keep_days', 15)


class ConsoleListener(QtCore.QObject):
    newline = QtCore.pyqtSignal(str)

    def listen(self):
        while True:
            line = sys.stdin.readline().strip()
            if line:
                self.newline.emit(line)


class FileOutput:
    # Implement 'write' method for logging to files
    # Used in Logger.profiles
    def __init__(self, root_dir, keep_days):
        self.root_dir = root_dir
        self.keep_days = keep_days      # keep_days = 0 means keep forever
        self.logs_dir = os.path.join(root_dir, 'logs')
        if not os.path.exists(self.logs_dir):
            os.mkdir(self.logs_dir)
        self.cur_file = None
        self.cur_date = None

    def _change_log_file(self):
        datestr = time.strftime('%Y%m%d', time.localtime())
        if datestr != self.cur_date:
            # date has changed
            if self.cur_file:
                self.cur_file.close()
            new_log_file = os.path.join(self.logs_dir, datestr + '.log')
            if os.path.exists(new_log_file):
                self.cur_file = open(new_log_file, 'a')
            else:
                self.cur_file = open(new_log_file, 'w')
            self.cur_date = datestr
            self._rm_expired_logs()

    def _rm_expired_logs(self):
        if self.keep_days == 0:
            return  # keep_days = 0 means keep forever
        all_files = os.listdir(self.logs_dir)
        date_now = datetime.date.today()
        for filename in all_files:
            parts = filename.split('.')
            if not (len(parts) == 2 and parts[1] == 'log'):
                continue
            ts = time.strptime(parts[0], '%Y%m%d')
            date_log = datetime.date(ts[0], ts[1], ts[2])
            delta = date_now - date_log
            if delta.days > self.keep_days:
                os.remove(os.path.join(self.logs_dir, filename))

    def write(self, data):
        self._change_log_file()
        self.cur_file.write(data)
        self.cur_file.flush()