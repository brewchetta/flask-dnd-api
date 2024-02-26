#!/usr/bin/env python3

from app import app
from models import db, Monster
from faker import Faker

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        print("Seeding complete!")
