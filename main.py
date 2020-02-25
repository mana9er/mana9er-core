#!/usr/bin/python3
import sys
import json
import argparse
from PyQt5 import QtCore

import core
import listener
import utils

parser = argparse.ArgumentParser(description='')
parser.add_argument('-c', '--config', type=str, default='config.json', help='Start core with a certain config file')
args = parser.parse_args()


def load_config(filename):
    with open(filename, mode='r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    app = QtCore.QCoreApplication(sys.argv)
    configs = utils.Config(load_config(args.config))
    core_inst = core.Core(configs)
    core_thread = QtCore.QThread()
    core_inst.moveToThread(core_thread)
    listener = listener.ConsoleListener()
    listener.newline.connect(core_inst.command)
    core_thread.started.connect(core_inst.init)
    core_thread.start()
    listener.listen()
