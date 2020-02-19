import sys
from PyQt5 import QtCore

class ConsoleListener(QtCore.QObject):
    newline = QtCore.pyqtSignal(str)

    def listen(self):
        while True:
            line = sys.stdin.readline().strip()
            if line:
                self.newline.emit(line)
