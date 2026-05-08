from django.core.management.base import BaseCommand
from django.conf import settings

from django.db import connections

from pymongo import ASCENDING

# Sample data
USERS = [
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
    {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "Marvel"},
    {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
    {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
]
TEAMS = [
    {"name": "Marvel", "members": ["Iron Man", "Captain America", "Spider-Man"]},
    {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
]
ACTIVITIES = [
    {"user": "Iron Man", "activity": "Running", "duration": 30},
    {"user": "Superman", "activity": "Flying", "duration": 60},
    {"user": "Batman", "activity": "Martial Arts", "duration": 45},
]
LEADERBOARD = [
    {"user": "Iron Man", "points": 100},
    {"user": "Superman", "points": 120},
    {"user": "Batman", "points": 90},
]
WORKOUTS = [
    {"name": "Super Strength", "suggested_for": ["Superman", "Wonder Woman"]},
    {"name": "Agility Training", "suggested_for": ["Spider-Man", "Batman"]},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        conn = connections['default']
        if conn.connection is None:
            conn.connect()
        db = conn.connection.client[conn.settings_dict['NAME']]
        # Drop collections if they exist
        for col in ["users", "teams", "activities", "leaderboard", "workouts"]:
            db[col].drop()
        # Insert data
        db["users"].insert_many(USERS)
        db["teams"].insert_many(TEAMS)
        db["activities"].insert_many(ACTIVITIES)
        db["leaderboard"].insert_many(LEADERBOARD)
        db["workouts"].insert_many(WORKOUTS)
        # Create unique index on email for users
        db["users"].create_index([("email", ASCENDING)], unique=True)
        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
