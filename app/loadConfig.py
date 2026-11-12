'''
This script loads the yaml file, which holds all
configuration information.
'''

import yaml, os

#For Logging
import logging

def load_config(filename = 'app/config.yaml', *, env_var=None):
    """Load YAML, optionally selecting an explicit environment-provided path."""
    if env_var:
        filename = os.environ.get(env_var, filename)
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg
