#!/usr/bin/env python

from __future__ import print_function

import os

from flask.ext.script import Manager, Server

from app import create_app


application = create_app(os.getenv('ENVIRONMENT') or 'development')
manager = Manager(application)
manager.add_command("runserver", Server(port=5000))


@manager.command
def list_routes():
    """List URLs of all application routes."""
    for rule in sorted(application.url_map.iter_rules(), key=lambda r: r.rule):
        print("{:10} {}".format(", ".join(rule.methods - set(['OPTIONS', 'HEAD'])), rule.rule))

if __name__ == '__main__':
    manager.run()
