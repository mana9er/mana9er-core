import sys
from PyQt5 import QtCore


class ConsoleListener(QtCore.QObject):
    newline = QtCore.pyqtSignal(str)
    eof_input = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ConsoleListener, self).__init__(parent)
        if sys.platform.startswith('win32'):
            import ctypes
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            notifier = QtCore.QWinEventNotifier(k32.GetStdHandle(-10), self)
        else:
            notifier = QtCore.QSocketNotifier(sys.stdin.fileno(), QtCore.QSocketNotifier.Read, self)
        notifier.activated.connect(self.receive)

    @QtCore.pyqtSlot()
    def receive(self):
        line = sys.stdin.readline().strip()
        if not line:
            self.eof_input.emit()
        else:
            self.newline.emit(line)
