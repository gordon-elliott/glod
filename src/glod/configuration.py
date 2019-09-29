__copyright__ = 'Copyright(c) Gordon Elliott 2017'

""" 
"""

import logging.config
import yaml
import pkg_resources

from dotmap import DotMap

config_path = pkg_resources.resource_filename(__name__, 'config/dev.yaml')

with open(config_path, 'r') as ymlfile:
    configuration = DotMap(yaml.full_load(ymlfile))

logging.config.dictConfig(configuration.logging.toDict())

LOG = logging.getLogger(__file__)
LOG.info(f"Configuration loaded from {config_path}")
