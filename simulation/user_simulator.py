"""
user_simulator.py
Generates realistic users for Hobby Tracker.
"""

import random
import hashlib
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_IN")

HOBBIES_LIST = [
    "Guitar", "Piano", "Singing",
    "Drawing", "Painting", "Photography",
    "Python Coding", "Web Development",
    "Machine Learning", "Reading",
    "Yoga", "Meditation", "Running",
    "Swimming", "Cooking", "Baking",
    "Chess", "Gardening", "Dance",
    "Language Learning",
]

CITIES = [
    "Mumbai", "Pune", "Delhi",
    "Bangalore", "Chennai", "Hyderabad",
    "Kolkata", "Jaipur", "Ahmedabad",
    "Surat",
]

AVATARS = ["🧑","👩","👨","🧑‍💻","👩‍🎨",
           "👨‍🎤","👩‍🔬","👨‍🏫","🧑‍🎓","👩‍💼"]


class User:
    """Represents a platform user."""

    def __init__(self, user_id=None):
        self.user_id      = user_id or \
                            self._gen_id()
        self.name         = fake.name()
        self.username     = fake.user_name()
        self.email        = fake.email()
        self.city         = random.choice(CITIES)
        self.avatar       = random.choice(AVATARS)
        self.bio          = fake.sentence(
            nb_words=12
        )
        self.joined_at    = (
            datetime.now() -
            timedelta(days=random.randint(30,365))
        ).isoformat()
        self.hobbies      = random.sample(
            HOBBIES_LIST,
            random.randint(2, 5)
        )
        self.followers    = random.randint(0, 200)
        self.following    = random.randint(0, 150)
        self.total_hours  = round(
            random.uniform(10, 500), 1
        )
        self.total_sessions = random.randint(
            10, 300
        )
        self.current_streak = random.randint(
            0, 30
        )
        self.longest_streak = random.randint(
            self.current_streak,
            self.current_streak + 30
        )
        self.badges       = []
        self.level        = self._calc_level()
        self.xp           = random.randint(
            100, 5000
        )
        self.is_active    = True

    def _gen_id(self):
        data = fake.email() + str(
            datetime.now().timestamp()
        )
        return "USR-" + hashlib.md5(
            data.encode()
        ).hexdigest()[:8].upper()

    def _calc_level(self):
        if self.total_hours >= 200:
            return "🏆 Expert"
        elif self.total_hours >= 100:
            return "⭐ Advanced"
        elif self.total_hours >= 50:
            return "📈 Intermediate"
        else:
            return "🌱 Beginner"

    def to_dict(self):
        return {
            "user_id":       self.user_id,
            "name":          self.name,
            "username":      self.username,
            "email":         self.email,
            "city":          self.city,
            "avatar":        self.avatar,
            "bio":           self.bio,
            "joined_at":     self.joined_at,
            "hobbies":       self.hobbies,
            "followers":     self.followers,
            "following":     self.following,
            "total_hours":   self.total_hours,
            "total_sessions":self.total_sessions,
            "current_streak":self.current_streak,
            "longest_streak":self.longest_streak,
            "badges":        self.badges,
            "level":         self.level,
            "xp":            self.xp,
            "is_active":     self.is_active,
        }


class UserManager:
    """Manages all platform users."""

    def __init__(self, n=30):
        self.users = {}
        self._create(n)

    def _create(self, n):
        for _ in range(n):
            u = User()
            self.users[u.user_id] = u

    def get_all(self):
        return [
            u.to_dict()
            for u in self.users.values()
        ]

    def get_random(self, n=1):
        sample = random.sample(
            list(self.users.values()),
            min(n, len(self.users))
        )
        return sample[0] if n == 1 else sample

    def get_leaderboard(self):
        return sorted(
            self.get_all(),
            key=lambda x: x["total_hours"],
            reverse=True
        )[:10]