from PyQt5 import QtCore


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

    def error(self, message, time_stamp=None):
        time_log = '[{}] '.format(time.strftime('%H:%M:%S')) if time_stamp is not None else ''
        self.log('{}[{}/ERROR] {}'.format(time_log, self.sender, message), 3)

    def warning(self, message, time_stamp=None):
        time_log = '[{}] '.format(time.strftime('%H:%M:%S')) if time_stamp is not None else ''
        self.log('{}[{}/WARN] {}'.format(time_log, self.sender, message), 2)

    def info(self, message, time_stamp=None):
        time_log = '[{}] '.format(time.strftime('%H:%M:%S')) if time_stamp is not None else ''
        self.log('{}[{}/INFO] {}'.format(time_log, self.sender, message), 1)

    def debug(self, message, time_stamp=None):
        time_log = '[{}] '.format(time.strftime('%H:%M:%S')) if time_stamp is not None else ''
        self.log('{}[{}/DEBUG] {}'.format(time_log, self.sender, message), 0)

    def direct_output(self, message):
        self.log(message, -1)
