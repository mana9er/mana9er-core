import sys
import json
import codecs
import argparse
from PySide2 import QtCore

import core

parser = argparse.ArgumentParser(description='')
parser.add_argument('-f', '--config', type=str, default='config.json', help='Start core with a certain config file')
args = parser.parse_args()


def load_config(filename):
    return json.load(codecs.open(filename, mode='r', encoding='utf-8'))


def wrap_config(config):
    res = object()
    res.default_entrance = config['default_entrance']
    res.plugin_names = config['plugins']
    return res


if __name__ == '__main__':
    configs = load_config(args.config)

    app = QtCore.QCoreApplication()
    exec_core = core.Core(wrap_config(configs), app)
    sys.exit(app.exec_())
