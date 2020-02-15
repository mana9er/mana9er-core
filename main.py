import sys
import json
import codecs
import argparse
from PyQt5 import QtCore

import core

parser = argparse.ArgumentParser(description='')
parser.add_argument('-c', '--config', type=str, default='config.json', help='Start core with a certain config file')
args = parser.parse_args()


def load_config(filename):
    with codecs.open(filename, mode='r', encoding='utf-8') as f:
        return json.load(f)


class Entrance(object):
    def __init__(self, entrance_dict):
        self.wd = entrance_dict['wd']
        self.exec = entrance_dict['exec']


class Config(object):
    def __init__(self, config_dict):
        self.default_entrance = Entrance(config_dict['default_entrance'])
        self.plugin_names = config_dict['plugins']
        if 'log_level' in config_dict:
            self.log_level = config_dict['log_level']
        else:
            self.log_level = 1  # INFO level
        self.prefix = config_dict['prefix']


if __name__ == '__main__':
    app = QtCore.QCoreApplication(sys.argv)
    configs = Config(load_config(args.config))
    core_inst = core.Core(configs)
    core_inst.core_quit.connect(app.quit)
    sys.exit(app.exec())
