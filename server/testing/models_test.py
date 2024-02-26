import pytest

from app import app
from models import db, Monster

class TestMonster:
    """ [TESTING SUITE: <Monster>] """

    def test_has_attributes(self):
        """ (attributes) Has all proper attributes"""