#!/usr/bin/env python
"""Handles the projects list"""

import json
import sys

import config

PROJECTS_FILE = config.get_value("projects_file")

class ProjectError(Exception):
    """Generic exception for the projects module"""
    pass

_data = []

def names():
    """Lists names of all configured projects"""
    return [project['name'] for project in _load_projects()]

def exists(name):
    """Returns true if project with given name is configured"""
    return name in names()

def _load_projects():
    """Loads the project data from file"""

    global _data

    if not _data:
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

if __name__ == "__main__":
    try:
        print(_load_projects())
        print(names())
        print(exists("TestProject"))
        print(exists("NoProject"))
    except ProjectError as error:
        print(error)
