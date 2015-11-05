import yaml
import os
import logging

config_file_name = 'config.yml'


def get_default():
    cfg = {'input_path': 'src',
           'output_path': 'out',
           'output_file_name': '{0}.oppl'.format(os.path.split(os.getcwd())[1]),
           'hand_list_file_name': 'hand_lists'
        }
    return cfg

def read_config(path): 
    config_file_path = get_config_file(path)

    if not os.path.isfile(config_file_path):
        logging.info('Config file not found.')
        return {}

    with open(config_file_path, 'r') as config_file:
        cfg = yaml.load(config_file)

    return cfg

def write_config(path):
    config_file_path = get_config_file(path)

    if os.path.isfile(config_file_path):
        logging.info('Config file already exits.')
        return

    with open(config_file_path, 'w') as config_file:
        config_file.write(yaml.dump(get_default(), default_flow_style=False))
    logging.info('Config file saved as %s', config_file_name)


def get_config_file(path):
    return os.path.join(path, config_file_name)

