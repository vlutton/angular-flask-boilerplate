#!/usr/bin/env python
from flask import Flask, g, jsonify
from flask.ext.script import Manager
from boilerplate_app import app
from boilerplate_app.models import db, User, Role

manager = Manager(app)

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

@manager.command
def createdb(testdata=False):
    db.create_all()
    db.session.commit()

@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=api', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


if __name__ == '__main__':
    manager.run()
