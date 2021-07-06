from PyQt5 import QtCore
import time

def deco_factory(prefix, suffix):
    def deco(s):
        return prefix + s + suffix
    return deco
error_deco = deco_factory('\033[31m', '\033[0m')
warning_deco = deco_factory('\033[33m', '\033[0m')
info_deco = deco_factory('\033[1m', '\033[0m')

class Logger(QtCore.QObject):
    sig_output = QtCore.pyqtSignal(str)

    def __init__(self, sender, profiles):
        super(Logger, self).__init__()
        self.sender = sender
        self.profiles = profiles

    def log(self, message, level, ending='\n'):
        if not isinstance(message, str):
            message = str(message)
        for i, profile in enumerate(self.profiles):
            if (profile.level <= level) or (level < 0):
                profile.output.write(message + ending)
                if i == 0:
                    self.sig_output.emit(message)
    
    def format_message(self, message, time_stamp, msg_type, level, deco=None):
        result = '[{}/{}] {}'.format(self.sender, msg_type, message)
        if time_stamp:
            result = '[{}]'.format(time.strftime('%Y-%m-%d %H:%M:%S')) + result
        if deco:
            result = deco(result)
        self.log(result, level)
    
    def error(self, message, time_stamp=True):
        self.format_message(message, time_stamp, 'ERROR', 3, error_deco)

    def warning(self, message, time_stamp=True):
        self.format_message(message, time_stamp, 'WARN', 2, warning_deco)

    def info(self, message, time_stamp=True):
        self.format_message(message, time_stamp, 'INFO', 1, info_deco)

    def debug(self, message, time_stamp=True):
        self.format_message(message, time_stamp, 'DEBUG', 0)

    def direct_output(self, message, ending='\n'):
        self.log(message, -1, ending)
