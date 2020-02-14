import yaml
import os
import logging

PROJECT_BASE = os.path.abspath(os.path.join(os.getcwd(), '..'))

def load_config_file(file_name='config.yaml'):
    config_file = open(os.path.join(PROJECT_BASE, file_name),'r').read()
    return yaml.load(config_file, Loader=yaml.FullLoader)

def get_db_file(config, file_extensions='.db'):
    db_file_dir = config['database']['db_file_dir']
    db_name = config['database']['db_name']
    return os.path.join(PROJECT_BASE, db_file_dir, db_name+file_extensions)

def get_logger(config, filename='logger.log'):
    level_config = config['system']['logging_level'].lower()
    level_mapping = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    level = level_mapping.get(level_config, logging.INFO)

    # create logger
    logger_name = "demo"
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # create file handler with formatter
    file_path = os.path.join(PROJECT_BASE, filename)
    fileHandler = logging.FileHandler(file_path)
    fileHandler.setLevel(level)
    fmt = "%(asctime)-15s %(levelname)s %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    fileHandler.setFormatter(formatter)

    # create stream handler to stdout
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    # add handlers
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger


def get_requests(config):
    settings = config['spider']['request']
    url = settings['url']
    dynamic_params = settings['dynamic_params']
    static_params = settings['static_params']
    header = settings['header']
    params = []
    for k, v in dynamic_params.items():
        min = v[0]
        max = v[1] + 1
        for i in range(min,max):
            this_param = {k: i}
            this_param.update(static_params)
            params.append(this_param)
    return (url, params, header)

config = load_config_file()

DB_FILE = get_db_file(config)
LOGGER = get_logger(config)
REQUESTS = get_requests(config)
