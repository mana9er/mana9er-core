from PyQt5 import QtCore
import utils

class Notifier(QtCore.QObject):
    sig_output = QtCore.pyqtSignal(str)
    sig_input = QtCore.pyqtSignal(utils.Player, str)

    @QtCore.pyqtSlot(str)
    def on_command(self, cmd):
        self.sig_input.emit(utils.GhostingPlayer(), cmd)

    @QtCore.pyqtSlot(list)
    def on_server_output(self, lines):
        # TODO: parsing and emit sig_input
