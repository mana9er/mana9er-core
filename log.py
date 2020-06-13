from PyQt5 import QtCore
import time


class Logger(QtCore.QObject):
    sig_output = QtCore.pyqtSignal(str)

    def __init__(self, sender, profiles):
        super(Logger, self).__init__()
        self.sender = sender
        self.profiles = profiles

    def log(self, message, level):
        if not isinstance(message, str):
            message = str(message)
        for i, profile in enumerate(self.profiles):
            if (profile.level <= level) or (level < 0):
                profile.output.write(message + '\n')
                if i == 0:
                    self.sig_output.emit(message)
    
    def format_message(self, message, time_stamp, msg_type, level):
        result = '[{}/{}] {}'.format(self.sender, msg_type, message)
        if time_stamp:
            result = '[{}]'.format(time.strftime('%H:%M:%S')) + result
        self.log(result, level)
    
    def error(self, message, time_stamp=None):
        self.format_message(message, time_stamp, 'ERROR', 3)

    def warning(self, message, time_stamp=None):
        self.format_message(message, time_stamp, 'WARN', 2)

    def info(self, message, time_stamp=None):
        self.format_message(message, time_stamp, 'INFO', 1)

    def debug(self, message, time_stamp=None):
        self.format_message(message, time_stamp, 'DEBUG', 0)

    def direct_output(self, message):
        self.log(message, -1)
