#!/usr/bin/env python
"""Handles the projects list"""

import json
import os.path
import sys
import unittest

from config import Config

CONFIG = Config()
PROJECTS_FILE = CONFIG.value('Files.projects_file')

class ProjectError(Exception):
    """Generic exception for the projects module"""
    pass

_data = {} # projects cache

def names():
    """Lists names of all configured projects"""
    return list(_load_projects().keys())

def exists(name):
    """Returns true if project with given name is configured"""
    return name in names()

def _load_projects():
    """Loads the project data from file"""

    global _data

    if not _data:
        if not os.path.isfile(PROJECTS_FILE):
            print("Creating projects file", PROJECTS_FILE)
            _write_projects_file({})

        try:
            with open(PROJECTS_FILE) as file:
                _data = json.load(file)
        except FileNotFoundError:
            raise ProjectError("Projects file not found")
        except json.JSONDecodeError:
            raise ProjectError("Invalid projects file")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    return _data

def add_project(name):
    """Appends project with name to projects"""
    if exists(name):
        raise ProjectError("Project {} already defined")
    projects = _load_projects()
    projects[name] = {} # add data values later
    _write_projects_file(projects)

def _write_projects_file(contents):
    """Writes projects data to JSON file"""

    global _data

    with open(PROJECTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contents, f, sort_keys = True, indent = 2)
    _data = {} # reset cache

class TestProjectFileHandling(unittest.TestCase):

    def setUp(self):
        global PROJECTS_FILE
        PROJECTS_FILE = 'test_projects.json'
        _write_projects_file({})

    def test_project_file_is_empty(self):
        self.assertEqual({}, _load_projects(), "projects file should be empty")

    def test_create_project(self):
        add_project("TestProject")
        self.assertEqual({"TestProject": {}}, _load_projects(), "should add first project")
        add_project("DemoProject")
        self.assertEqual({"DemoProject": {}, "TestProject": {}}, _load_projects(), "should add second project and list in alphabetical order")
    
    def test_add_project_with_named_parameters(self):
        add_project(name="NamedTestProject")
        self.assertEqual({"NamedTestProject": {}}, _load_projects())

    def test_names(self):
        add_project("foo")
        add_project("bar")
        self.assertEqual(["bar", "foo"], names(), "should return project names as alphabetical list")

    def test_exists(self):
        add_project("ProjectExists")
        self.assertTrue(exists("ProjectExists"))
        self.assertFalse(exists("ProjectDoesNotExist"))

    def test_add_duplicate(self):
        add_project("foo")
        with self.assertRaises(ProjectError):
            add_project("foo")

if __name__ == "__main__":
    unittest.main()
