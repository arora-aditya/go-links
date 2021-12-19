from configparser import ConfigParser


def parse_config():
    config = ConfigParser()
    config.read("config.ini")
    return config


config = parse_config()

SECTION = "DEFAULT"
MAPPING_FILE = config.get(SECTION, "MAPPING_FILE")
METRICS_FILE = config.get(SECTION, "METRICS_FILE")
CERTIFICATE_FILE = config.get(SECTION, "CERTIFICATE_FILE")
NEW_LINK_PREFIX = config.get(SECTION, "NEW_LINK_PREFIX")
PORT = int(config.get(SECTION, "PORT"))
