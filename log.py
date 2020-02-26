from PyQt5 import QtCore


class Logger:
    sig_output = QtCore.pyqtSignal(str)

    def __init__(self, sender, profiles):
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

    def error(self, message):
        self.log('[{}/ERROR] {}'.format(self.sender, message), 3)

    def warning(self, message):
        self.log('[{}/WARN] {}'.format(self.sender, message), 2)

    def info(self, message):
        self.log('[{}/INFO] {}'.format(self.sender, message), 1)

    def debug(self, message):
        self.log('[{}/DEBUG] {}'.format(self.sender, message), 0)

    def direct_output(self, message):
        self.log(message, -1)
