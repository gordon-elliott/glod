__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import yaml
import pkg_resources
from dotmap import DotMap

config_path = pkg_resources.resource_filename(__name__, 'config/dev.yaml')

with open(config_path, 'r') as ymlfile:
    configuration = DotMap(yaml.load(ymlfile))
