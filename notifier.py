from PyQt5 import QtCore
import utils
import re

class Notifier(QtCore.QObject):
    sig_output = QtCore.pyqtSignal(str)
    sig_input = QtCore.pyqtSignal(utils.Player, str)

    @QtCore.pyqtSlot(str)
    def on_command(self, cmd):
        self.sig_input.emit(utils.GhostingPlayer(), cmd)

    @QtCore.pyqtSlot(list)
    def on_server_output(self, lines):
        for line in lines:
            match_obj = re.match(r'.*?<(\w+?)> (.*)', line)
            if match_obj:
                # some players said something
                player = match_obj.group(1)
                text = match_obj.group(2)
                self.sig_input.emit(utils.Player(player), text)
                
