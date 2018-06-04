#!/usr/bin/env python
"""Time tracking

Usage:
  timetracking -p PROJECTNAME [-c] start
  timetracking [-p PROJECTNAME] end
  timetracking [-a] list
  timetracking report
  timetracking add
  timetracking -h

Options:
-p PROJECTNAME --project=PROJECTNAME    project name
-c --continue                           also continue tracking other active projects
-a --active                             list only projects currently being tracked
-h --help                               show this help message
"""

import os
import sys
from docopt import docopt

import projects
import tracker

def print_help():
    """Prints out the help message"""
    print(__doc__)

def main(argv):
    """Main controller for time tracking functions"""

    project_name = ""
    continue_previous = False

    args = docopt(__doc__, version="0.1")

    if args['--project']:
        project_name = load_project(args['--project'])

    if args['--continue']:
        continue_previous = True

    if args['list']:
        if args['--active']:
            print("\n".join(tracker.currently_tracked_projects()))
        else:
            print("\n".join(projects.names()))
    elif args['start']:
        if not continue_previous:
            tracker.stop_all()
        tracker.start(project_name)
    elif args['end']:
        if project_name:
            tracker.stop(project_name)
        else:
            tracker.stop_all()
    elif args['report']:
        tracker.print_report()
    elif args['add']:
        add_new_project()

def load_project(project_name):
    """Sets project name after checking it is valid"""
    if not projects.exists(project_name):
        print("Invalid project: {}".format(project_name))
        sys.exit(1)
    else:
        return project_name

def add_new_project():
    """Asks for project data and adds the project"""
    project_name = input("Project name: ").replace(' ', '')
    try:
        projects.add_project(project_name)
    except projects.ProjectError as e:
        print("Cannot add project {}, error: {}".format(project_name, e))
        print(e.args)
        print(type(e).__name__)

if __name__ == "__main__":
    main(sys.argv[1:])
