"""
hobby_simulator.py
Simulates hobbies, skills and learning goals.
"""

import random
import hashlib
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_IN")

HOBBY_CATEGORIES = {
    "Music":       ["Guitar","Piano","Singing",
                    "Drums","Violin","Flute"],
    "Art":         ["Drawing","Painting",
                    "Photography","Sketching",
                    "Digital Art","Calligraphy"],
    "Technology":  ["Python Coding",
                    "Web Development",
                    "Machine Learning",
                    "Mobile Apps","Cybersecurity",
                    "Data Science"],
    "Fitness":     ["Yoga","Running","Swimming",
                    "Gym","Cycling","Martial Arts"],
    "Mind":        ["Reading","Chess","Meditation",
                    "Journaling","Language Learning",
                    "Public Speaking"],
    "Creative":    ["Cooking","Baking","Gardening",
                    "Dance","Writing","Pottery"],
}

SKILL_LEVELS = [
    "Absolute Beginner",
    "Beginner",
    "Elementary",
    "Pre-Intermediate",
    "Intermediate",
    "Upper-Intermediate",
    "Advanced",
    "Expert",
    "Master",
]

GOAL_TYPES = [
    "Complete 30 sessions",
    "Practice 100 hours",
    "Learn 5 new techniques",
    "Achieve streak of 30 days",
    "Complete online course",
    "Perform/publish work",
    "Teach someone else",
    "Enter competition",
]


class Hobby:
    """Represents a user's hobby/skill."""

    def __init__(self, user_id,
                 hobby_name=None,
                 category=None):
        self.hobby_id    = self._gen_id()
        self.user_id     = user_id
        self.category    = category or \
                           random.choice(
                               list(
                                   HOBBY_CATEGORIES
                                   .keys()
                               )
                           )
        self.name        = hobby_name or \
                           random.choice(
                               HOBBY_CATEGORIES[
                                   self.category
                               ]
                           )
        self.emoji       = self._get_emoji()
        self.skill_level = random.choice(
            SKILL_LEVELS[:6]
        )
        self.target_level= random.choice(
            SKILL_LEVELS[
                SKILL_LEVELS.index(
                    self.skill_level
                )+1:
            ]
        )
        self.goal        = random.choice(
            GOAL_TYPES
        )
        self.goal_progress = random.randint(
            0, 100
        )
        self.started_at  = (
            datetime.now() -
            timedelta(days=random.randint(7,180))
        ).strftime("%Y-%m-%d")
        self.total_hours = round(
            random.uniform(1, 200), 1
        )
        self.sessions    = random.randint(
            5, 150
        )
        self.streak      = random.randint(0, 30)
        self.is_active   = True
        self.color       = self._get_color()

    def _gen_id(self):
        return "HOB-" + hashlib.md5(
            str(datetime.now().timestamp())
            .encode()
        ).hexdigest()[:8].upper()

    def _get_emoji(self):
        emojis = {
            "Music":      "🎵",
            "Art":        "🎨",
            "Technology": "💻",
            "Fitness":    "💪",
            "Mind":       "🧠",
            "Creative":   "✨",
        }
        return emojis.get(self.category, "⭐")

    def _get_color(self):
        colors = {
            "Music":      "#a78bfa",
            "Art":        "#f472b6",
            "Technology": "#60a5fa",
            "Fitness":    "#34d399",
            "Mind":       "#fbbf24",
            "Creative":   "#fb923c",
        }
        return colors.get(self.category,"#a78bfa")

    def to_dict(self):
        return {
            "hobby_id":      self.hobby_id,
            "user_id":       self.user_id,
            "category":      self.category,
            "name":          self.name,
            "emoji":         self.emoji,
            "skill_level":   self.skill_level,
            "target_level":  self.target_level,
            "goal":          self.goal,
            "goal_progress": self.goal_progress,
            "started_at":    self.started_at,
            "total_hours":   self.total_hours,
            "sessions":      self.sessions,
            "streak":        self.streak,
            "is_active":     self.is_active,
            "color":         self.color,
        }


class HobbyManager:
    """Manages hobbies across all users."""

    def __init__(self, user_manager):
        self.hobbies     = {}
        self.user_manager= user_manager
        self._seed_hobbies()

    def _seed_hobbies(self):
        for user in self.user_manager\
                .users.values():
            for hobby_name in user.hobbies[:3]:
                cat = self._find_category(
                    hobby_name
                )
                h   = Hobby(
                    user.user_id,
                    hobby_name, cat
                )
                self.hobbies[h.hobby_id] = h

    def _find_category(self, name):
        for cat, hobbies in \
                HOBBY_CATEGORIES.items():
            if name in hobbies:
                return cat
        return "Creative"

    def get_user_hobbies(self, user_id):
        return [
            h.to_dict()
            for h in self.hobbies.values()
            if h.user_id == user_id
        ]

    def get_all(self):
        return [
            h.to_dict()
            for h in self.hobbies.values()
        ]

    def get_by_category(self, category):
        return [
            h.to_dict()
            for h in self.hobbies.values()
            if h.category == category
        ]

    def add_hobby(self, user_id,
                  name, category):
        h = Hobby(user_id, name, category)
        self.hobbies[h.hobby_id] = h
        return h

    def get_popular(self):
        from collections import Counter
        names = [
            h.name
            for h in self.hobbies.values()
        ]
        return Counter(names).most_common(10)