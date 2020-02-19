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
            self.notifier = QtCore.QWinEventNotifier(k32.GetStdHandle(-10))
        else:
            self.notifier = QtCore.QSocketNotifier(sys.stdin.fileno(), QtCore.QSocketNotifier.Read)
        self.notifier_thread = QtCore.QThread()
        self.notifier.moveToThread(self.notifier_thread)
        
        that = self
        @QtCore.pyqtSlot()
        def receive():
            print('receive')
            line = sys.stdin.readline().strip()
            if not line:
                that.eof_input.emit()
            else:
                that.newline.emit(line)
        self.notifier.activated.connect(receive)
        self.notifier_thread.start()
    def __del__(self):
        self.notifier_thread.quit()
        self.notifier_thread.wait()

