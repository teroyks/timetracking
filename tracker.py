#!/usr/bin/env python
"""Handles the time tracking file operations

Valid commands:
START - starts tracking
STOP  - stops tracking
"""

from datetime import datetime, timedelta

import config
import math

TRACKING_FILE = config.get_value("Files.tracking_file")

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

def print_report():
    """Creates a report for time used in projects"""
    started = {}
    daily_totals = {}

    try:
        round_to_mins = int(config.get_value("Tracker.round_minutes"))
    except KeyError:
        round_to_mins = 15

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
                    daily_totals[date][project_name] = \
                        daily_totals.setdefault(date, {}).get(project_name, timedelta(0)) \
                        + _round_timedelta(elapsed, round_to_mins)
                del started[project_name]

        if started:
            print("Active projects:")
            print(started)

    for date, project_totals in daily_totals.items():
        print(datetime.strptime(date, '%Y-%m-%d').strftime('%a %-d.%-m.%Y'))
        for project_name, project_total in project_totals.items():
            print("\t{:>15}:  {}".format(project_name, project_total))

def stop_all():
    """Ends tracking all active projects"""
    for project_name in currently_tracked_projects():
        stop(project_name)

def _log_command(command, project_name):
    with open(TRACKING_FILE, "a") as f:
        f.write("{} {} {}\n".format(datetime.now().isoformat(sep=' ', timespec='minutes'), command, project_name))

def _to_datetime(date, time):
    return datetime.strptime("{} {}".format(date, time), '%Y-%m-%d %H:%M')

def _round_timedelta(delta, round_to_mins):
    """Parses timedelta to hours and minutes

    Rounds the minute amount up to round_to_mins
    """
    hours, mins = delta.seconds // 3600, delta.seconds % 3600 // 60
    mins = math.ceil(mins / round_to_mins) * round_to_mins
    return timedelta(hours=hours, minutes=mins)

if __name__ == "__main__":
    print_report()