#!/usr/bin/env python
"""Parses the config variables"""

import configparser
import contextlib
import os
import unittest

class Config():
    _file = 'timetracking.conf'

    def __init__(self, file=None):
        if file:
            self._file = file

    @property
    def parser(self):
        """Creates and fills a config object"""
        parser = configparser.ConfigParser()
        parser.read(self._file)

        return parser

    @property
    def sections(self):
        """Reads the config sections from config file"""

        return self.parser.sections()

    def value(self, section_key: str):
        """Reads value of key from config file
        
        section_key value "Foo.bar" finds value of key "bar" from section "Foo".
        """
        section, key = section_key.split('.')

        return self.parser[section][key]

class TestConfig(unittest.TestCase):

    test_config_file = "test_timetracking.conf"

    def setUp(self):
        """Initializes test
        
        - overrides normal configuration file
        - creates a helper configparser for initializing the config for the test
        """
        self.config = Config(self.test_config_file)
        self.config_writer = configparser.ConfigParser()
    
    def tearDown(self):
        """Removes the config file if created by test"""
        with contextlib.suppress(FileNotFoundError):
            os.remove(self.test_config_file)
    
    def test_read_config_file(self):
        self.assertEqual(self.test_config_file, self.config._file, 'should use test config instead of the real one')
        self._write_config_to_file(self.config_writer)

        self.assertIsInstance(self.config.parser, configparser.ConfigParser)

    def test_read_sections(self):
        self.config_writer['First'] = {'foo': 1}        
        self.config_writer['Second'] = {}
        self._write_config_to_file(self.config_writer)

        self.assertEqual(['First', 'Second'], self.config.sections)
    
    def test_read_value_from_section(self):
        self.config_writer['Foo'] = {'baz': 'first value'}
        self.config_writer['Bar'] = {'baz' : 'second value'}
        self._write_config_to_file(self.config_writer)

        self.assertEqual('second value', self.config.value('Bar.baz'))
        self.assertEqual('first value', self.config.value('Foo.baz'))

    def _write_config_to_file(self, parser: configparser.ConfigParser):
        """Writes the configuration to test config file
        
        Arguments:
        parser -- ConfigParser instance to write to the file
        """
        with open(self.test_config_file, 'w') as file:
            parser.write(file)

if __name__ == "__main__":
    unittest.main()
