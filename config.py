#!/usr/bin/env python
"""Parses the config variables"""

import configparser
import contextlib
import os
import unittest

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

def get_value(section_key):
    """Reads value of key from config file
    
    section_key value "Foo.bar" finds value of key "bar" from section "Foo".
    """
    config = read_config()

    section, key = section_key.split('.')
    return config[section][key]

class TestConfig(unittest.TestCase):

    _test_config_file = "timetracking_test.conf"
    _parser = None

    def setUp(self):
        """Overrides normal configuration file"""
        _SETTINGS.config_file = self._test_config_file
        self._parser = configparser.ConfigParser()
    
    def tearDown(self):
        """Removes the config file created by test"""
        with contextlib.suppress(FileNotFoundError):
            os.remove(self._test_config_file)
    
    def test_read_project_file(self):
        """Tests reading a config parser from file"""
        self.assertEqual(self._test_config_file, _SETTINGS.config_file, "should use test config instead of the real one")
        self._write_config_to_file(self._parser)

        self.assertIsInstance(read_config(), configparser.ConfigParser)

    def test_read_sections(self):
        """Tests reading the sections list from config"""
        self._parser['First'] = {'foo': 1}
        self._parser['Second'] = {}
        self._write_config_to_file(self._parser)

        self.assertEqual(['First', 'Second'], get_sections())
    
    def test_read_value(self):
        """Tests reading the value from correct section"""
        self._parser['Foo'] = {'baz': 'first value'}
        self._parser['Bar'] = {'baz' : 'second value'}
        self._write_config_to_file(self._parser)

        self.assertEqual('second value', get_value("Bar.baz"))
        self.assertEqual('first value', get_value("Foo.baz"))

    def _write_config_to_file(self, parser):
        """Writes the configuration to test config file"""
        with open(self._test_config_file, "w") as f:
            parser.write(f)

if __name__ == "__main__":
    unittest.main()
