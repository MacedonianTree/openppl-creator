import os
import logging

logging.root.setLevel(logging.INFO)

VERSION = '1.0.0'
__version__ = VERSION


DESCRIPTION = 'OpenPPL Creator V{0}'.format(VERSION)


from openppl_creator_lib import configuration

cfg = configuration.get_default()


cfg.update(configuration.read_config(os.getcwd()))