from configparser import ConfigParser

CONFIG_FILE = "config.ini"

def parse_config(file_path: str):
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config


config = parse_config(CONFIG_FILE)

SECTION = "DEFAULT"
MAPPING_FILE = config.get(SECTION, "MAPPING_FILE")
METRICS_FILE = config.get(SECTION, "METRICS_FILE")
CERTIFICATE_FILE = config.get(SECTION, "CERTIFICATE_FILE")
NEW_LINK_PREFIX = config.get(SECTION, "NEW_LINK_PREFIX")
DELETE_LINK_PREFIX = config.get(SECTION, "DELETE_LINK_PREFIX")
ANALYTICS_LINK_PREFIX = config.get(SECTION, "ANALYTICS_LINK_PREFIX")
API_LINK_PREFIX = config.get(SECTION, "API_LINK_PREFIX")
TEST_LINK_PREFIX = config.get(SECTION, "TEST_LINK_PREFIX")
PORT = int(config.get(SECTION, "PORT"))
