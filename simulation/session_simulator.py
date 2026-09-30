"""
session_simulator.py
Simulates practice sessions and progress logs.
"""

import random
import hashlib
import numpy as np
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_IN")

MOODS = ["😊 Great","😐 Okay","😓 Tough",
         "🔥 On Fire","😴 Tired"]
FOCUS_AREAS = [
    "Basics","Technique","Speed",
    "Accuracy","Theory","Practice",
    "New Skill","Revision","Performance",
]


class PracticeSession:
    """Represents a single practice session."""

    def __init__(self, user_id, hobby_id,
                 hobby_name, date=None):
        self.session_id  = self._gen_id()
        self.user_id     = user_id
        self.hobby_id    = hobby_id
        self.hobby_name  = hobby_name
        self.date        = date or (
            datetime.now() -
            timedelta(
                days=random.randint(0,60)
            )
        ).strftime("%Y-%m-%d")
        self.duration_min= random.choice(
            [15,20,30,45,60,90,120]
        )
        self.duration_hrs= round(
            self.duration_min / 60, 2
        )
        self.mood        = random.choice(MOODS)
        self.focus_area  = random.choice(
            FOCUS_AREAS
        )
        self.notes       = fake.sentence(
            nb_words=10
        )
        self.xp_earned   = self._calc_xp()
        self.rating      = random.randint(3, 5)
        self.created_at  = datetime.now()\
                          .isoformat()

    def _gen_id(self):
        return "SES-" + hashlib.md5(
            str(datetime.now().timestamp())
            .encode()
        ).hexdigest()[:8].upper()

    def _calc_xp(self):
        base = self.duration_min * 2
        bonus= random.randint(0, 20)
        return base + bonus

    def to_dict(self):
        return {
            "session_id":   self.session_id,
            "user_id":      self.user_id,
            "hobby_id":     self.hobby_id,
            "hobby_name":   self.hobby_name,
            "date":         self.date,
            "duration_min": self.duration_min,
            "duration_hrs": self.duration_hrs,
            "mood":         self.mood,
            "focus_area":   self.focus_area,
            "notes":        self.notes,
            "xp_earned":    self.xp_earned,
            "rating":       self.rating,
            "created_at":   self.created_at,
        }


class SessionManager:
    """Manages all practice sessions."""

    def __init__(self, hobby_manager):
        self.sessions      = []
        self.hobby_manager = hobby_manager
        self._seed_sessions()

    def _seed_sessions(self):
        for hobby in self.hobby_manager\
                .hobbies.values():
            n = random.randint(5, 30)
            for i in range(n):
                date = (
                    datetime.now() -
                    timedelta(days=i*2)
                ).strftime("%Y-%m-%d")
                s = PracticeSession(
                    hobby.user_id,
                    hobby.hobby_id,
                    hobby.name,
                    date,
                )
                self.sessions.append(s)

    def log_session(self, user_id,
                    hobby_id, hobby_name,
                    duration_min, mood,
                    focus_area, notes):
        s = PracticeSession(
            user_id, hobby_id, hobby_name
        )
        s.duration_min = duration_min
        s.duration_hrs = round(
            duration_min / 60, 2
        )
        s.mood         = mood
        s.focus_area   = focus_area
        s.notes        = notes
        s.xp_earned    = duration_min * 2
        self.sessions.append(s)
        return s

    def get_user_sessions(self, user_id,
                          days=30):
        cutoff = (
            datetime.now() -
            timedelta(days=days)
        ).strftime("%Y-%m-%d")
        return [
            s.to_dict()
            for s in self.sessions
            if s.user_id == user_id and
            s.date >= cutoff
        ]

    def get_hobby_sessions(self, hobby_id):
        return [
            s.to_dict()
            for s in self.sessions
            if s.hobby_id == hobby_id
        ]

    def get_all(self):
        return [s.to_dict()
                for s in self.sessions]

    def get_stats(self):
        total_hrs = sum(
            s.duration_hrs
            for s in self.sessions
        )
        return {
            "total_sessions": len(self.sessions),
            "total_hours":    round(total_hrs,1),
            "avg_duration":   round(
                np.mean([
                    s.duration_min
                    for s in self.sessions
                ]), 1
            ) if self.sessions else 0,
        }