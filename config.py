#!/usr/bin/env python
"""Parses the config variables"""

import configparser

class Settings:
    """Module settings"""
    config_file = "timetracking.conf"

_SETTINGS = Settings()

def read_config():
    """Creates and fills a config object"""
    config = configparser.ConfigParser()
    config.read(_SETTINGS.config_file)

    return config

def get_sections():
    """Reads the config sections from config file"""
    config = read_config()

    return config.sections()

def get_value(key):
    """Reads value of key from config file"""
    config = read_config()

    return config['Files'][key]

if __name__ == "__main__":
    print("Config file: {}".format(_SETTINGS.config_file))
    print("Config sections: {}".format(", ".join(get_sections())))
    print("Projects file: {}".format(get_value("projects_file")))
