import sys
import json
import codecs
import argparse
from PySide2 import QtCore

import core

parser = argparse.ArgumentParser(description='')
parser.add_argument('-c', '--config', type=str, default='config.json', help='Start core with a certain config file')
args = parser.parse_args()


def load_config(filename):
    return json.load(codecs.open(filename, mode='r', encoding='utf-8'))


class Config(object):
    def __init__(self, config_dict):
        self.default_entrance = config_dict['default_entrance']
        self.plugin_names = config_dict['plugins']
        if 'log_level' in config_dict:
            self.log_level = config_dict['log_level']
        else:
            self.log_level = 1  # INFO


if __name__ == '__main__':
    app = QtCore.QCoreApplication()
    configs = Config(load_config(args.config))
    core_inst = core.Core(configs)
    core_inst.core_quit.connect(app.quit)
    sys.exit(app.exec_())
