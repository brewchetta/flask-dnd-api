#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Monster

from create_app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(port=5000, debug=True)