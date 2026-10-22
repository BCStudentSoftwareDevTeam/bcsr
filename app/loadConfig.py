'''
This script loads the yaml file, which holds all
configuration information.
'''

import yaml, os

#For Logging
import logging

def load_config(filename = 'app/config.yaml'):
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


def load_secret_config():
    """Allow an explicit configuration file, including isolated test settings."""
    return load_config(os.environ.get('BCSR_SECRET_CONFIG', 'app/secret_config.yaml'))
