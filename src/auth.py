"""
auth.py
Simulates cloud authentication.
"""

import hashlib
from datetime import datetime
from faker import Faker

fake = Faker("en_IN")

DEMO_USERS = [
    {
        "email":    "neha@demo.com",
        "password": "demo123",
        "name":     "Neha Joshi",
        "username": "neha_codes",
        "avatar":   "👩‍💻",
        "hobbies":  ["Python Coding",
                     "Guitar", "Reading"],
        "city":     "Pune",
        "level":    "⭐ Advanced",
        "xp":       2450,
        "current_streak": 12,
        "longest_streak": 28,
        "total_hours":    87.5,
        "total_sessions": 145,
        "followers":      234,
        "following":      89,
        "bio":  "B.Tech AI & Data Science student."
                " Love coding & music! 🎵💻",
    },
    {
        "email":    "rahul@demo.com",
        "password": "demo123",
        "name":     "Rahul Verma",
        "username": "rahul_creates",
        "avatar":   "👨‍🎨",
        "hobbies":  ["Drawing","Yoga","Chess"],
        "city":     "Mumbai",
        "level":    "📈 Intermediate",
        "xp":       1200,
        "current_streak": 5,
        "longest_streak": 15,
        "total_hours":    42.0,
        "total_sessions": 68,
        "followers":      89,
        "following":      124,
        "bio":  "Artist by heart, coder by day! 🎨",
    },
    {
        "email":    "priya@demo.com",
        "password": "demo123",
        "name":     "Priya Sharma",
        "username": "priya_grows",
        "avatar":   "👩‍🎤",
        "hobbies":  ["Singing","Running",
                     "Cooking"],
        "city":     "Delhi",
        "level":    "🏆 Expert",
        "xp":       4800,
        "current_streak": 21,
        "longest_streak": 45,
        "total_hours":    210.0,
        "total_sessions": 320,
        "followers":      512,
        "following":      201,
        "bio": "Music is my therapy! 🎵 "
               "Runner & foodie 🏃",
    },
]


class AuthService:
    """Simulates cloud auth system."""

    def __init__(self):
        self.sessions = {}

    def login(self, email, password):
        user = next(
            (u for u in DEMO_USERS
             if u["email"] == email and
             u["password"] == password),
            None
        )
        if not user:
            return None, "Invalid credentials!"

        token = hashlib.md5(
            (email + str(datetime.now()))
            .encode()
        ).hexdigest()[:16]

        session = {
            **user,
            "token": token,
            "logged_in": datetime.now()
                        .isoformat(),
        }
        self.sessions[token] = session
        return session, "Login successful!"