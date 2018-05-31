#!/usr/bin/env python
"""Handles the time tracking file operations

Valid commands:
START - starts tracking
STOP  - stops tracking
"""

from datetime import datetime, timedelta

import config
import math

TRACKING_FILE = config.get_value("tracking_file")

def currently_tracked_projects():
    """Lists all projects that are currently being tracked.

    A tracked project has a start time but no stop time
    """
    active_projects = []
    try:
        with open(TRACKING_FILE) as f:
            for line in f:
                words = line.split()
                command, project_name = words[-2:]
                if command == "START":
                    if not project_name in active_projects:
                        active_projects.append(project_name)
                elif command == "STOP":
                    if project_name in active_projects:
                        active_projects.remove(project_name)
                else:
                    raise ValueError("Invalid tracker command: {}".format(command))
    except FileNotFoundError:
        open(TRACKING_FILE, "w").close()

    return active_projects

def start(project_name):
    """Starts tracking a project
    
    If project is already active, prints notification
    """
    if project_name in currently_tracked_projects():
        print("{} is already active".format(project_name))
        return
    
    _log_command("START", project_name)

def stop(project_name):
    """Ends tracking an active project

    If project is not active, prints notification
    """
    if project_name not in currently_tracked_projects():
        print("{} is not active".format(project_name))
        return
    
    _log_command("STOP", project_name)

def report():
    """Creates a report for time used in projects"""
    started = {}
    with open(TRACKING_FILE) as f:
        for line in f:
            date, time, command, project_name = line.split()
            # print("date: {}\ttime: {}\tcommand: {}\tproject: {}".format(date, time, command, project_name))

            if command == "START":
                started[project_name] = _to_datetime(date, time)
            if command == "STOP":
                elapsed = _to_datetime(date, time) - started[project_name]
                if elapsed.days:
                    print("Error: tracking up for more than a day: {}".format(line))
                else:
                    print("{}  {:>15}:  {}".format(date, project_name, elapsed))
                del started[project_name]

        if started:
            print("Active projects:")
            print(started)

def stop_all():
    """Ends tracking all active projects"""
    for project_name in currently_tracked_projects():
        stop(project_name)

def _log_command(command, project_name):
    with open(TRACKING_FILE, "a") as f:
        f.write("{} {} {}\n".format(datetime.now().isoformat(sep=' ', timespec='minutes'), command, project_name))

def _to_datetime(date, time):
    return datetime.strptime("{} {}".format(date, time), '%Y-%m-%d %H:%M')

if __name__ == "__main__":
    report()