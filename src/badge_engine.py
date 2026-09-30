"""
badge_engine.py
Gamification badge and achievement system.
"""

from datetime import datetime


BADGES = {
    # Streak badges
    "First Step":     {
        "emoji": "👣",
        "desc":  "Complete your first session",
        "xp":    50,
        "color": "#60a5fa",
        "category": "Streak",
    },
    "Week Warrior":   {
        "emoji": "🗓️",
        "desc":  "7-day practice streak",
        "xp":    100,
        "color": "#34d399",
        "category": "Streak",
    },
    "Fortnight Hero": {
        "emoji": "💪",
        "desc":  "14-day practice streak",
        "xp":    200,
        "color": "#a78bfa",
        "category": "Streak",
    },
    "Month Master":   {
        "emoji": "🏆",
        "desc":  "30-day practice streak",
        "xp":    500,
        "color": "#fbbf24",
        "category": "Streak",
    },
    # Hours badges
    "10 Hours":       {
        "emoji": "⏱️",
        "desc":  "10 hours of practice",
        "xp":    100,
        "color": "#60a5fa",
        "category": "Hours",
    },
    "50 Hours":       {
        "emoji": "⭐",
        "desc":  "50 hours of practice",
        "xp":    250,
        "color": "#fbbf24",
        "category": "Hours",
    },
    "100 Hours":      {
        "emoji": "💯",
        "desc":  "100 hours of practice",
        "xp":    500,
        "color": "#f87171",
        "category": "Hours",
    },
    "500 Hours":      {
        "emoji": "🌟",
        "desc":  "500 hours of practice",
        "xp":    2000,
        "color": "#fbbf24",
        "category": "Hours",
    },
    # Session badges
    "Session Starter":{
        "emoji": "🚀",
        "desc":  "Complete 10 sessions",
        "xp":    100,
        "color": "#34d399",
        "category": "Sessions",
    },
    "Dedicated":      {
        "emoji": "🎯",
        "desc":  "Complete 50 sessions",
        "xp":    300,
        "color": "#a78bfa",
        "category": "Sessions",
    },
    "Century Club":   {
        "emoji": "💎",
        "desc":  "Complete 100 sessions",
        "xp":    600,
        "color": "#60a5fa",
        "category": "Sessions",
    },
    # Community badges
    "Social Butterfly":{
        "emoji": "🦋",
        "desc":  "Share 5 posts",
        "xp":    150,
        "color": "#f472b6",
        "category": "Community",
    },
    "Influencer":     {
        "emoji": "📣",
        "desc":  "Get 100 likes",
        "xp":    300,
        "color": "#fb923c",
        "category": "Community",
    },
    "Mentor":         {
        "emoji": "🧑‍🏫",
        "desc":  "Help 10 community members",
        "xp":    400,
        "color": "#34d399",
        "category": "Community",
    },
    # Skill badges
    "Multi-Talented": {
        "emoji": "🎭",
        "desc":  "Track 3+ hobbies",
        "xp":    200,
        "color": "#e879f9",
        "category": "Skills",
    },
    "Perfectionist":  {
        "emoji": "✨",
        "desc":  "Rate 5 sessions 5 stars",
        "xp":    150,
        "color": "#fbbf24",
        "category": "Skills",
    },
    "Early Bird":     {
        "emoji": "🌅",
        "desc":  "Complete 10 morning sessions",
        "xp":    200,
        "color": "#fb923c",
        "category": "Skills",
    },
    "Night Owl":      {
        "emoji": "🦉",
        "desc":  "Complete 10 evening sessions",
        "xp":    200,
        "color": "#a78bfa",
        "category": "Skills",
    },
}


class BadgeEngine:
    """
    Evaluates and awards badges
    based on user activity.
    """

    def __init__(self):
        self.badge_log = []

    def evaluate(self, user_data,
                 sessions, hobbies,
                 posts):
        """Evaluate all badges for a user."""
        earned = []
        uid    = user_data.get("user_id","")

        total_sessions = len([
            s for s in sessions
            if s.get("user_id") == uid
        ])
        total_hours = sum(
            s.get("duration_hrs", 0)
            for s in sessions
            if s.get("user_id") == uid
        )
        streak = user_data.get(
            "current_streak", 0
        )
        user_posts = len([
            p for p in posts
            if p.get("user_id") == uid
        ])
        total_likes = sum(
            p.get("likes", 0)
            for p in posts
            if p.get("user_id") == uid
        )
        n_hobbies = len(hobbies)

        checks = {
            "First Step":      total_sessions >= 1,
            "Week Warrior":    streak >= 7,
            "Fortnight Hero":  streak >= 14,
            "Month Master":    streak >= 30,
            "10 Hours":        total_hours >= 10,
            "50 Hours":        total_hours >= 50,
            "100 Hours":       total_hours >= 100,
            "500 Hours":       total_hours >= 500,
            "Session Starter": total_sessions >= 10,
            "Dedicated":       total_sessions >= 50,
            "Century Club":    total_sessions >= 100,
            "Social Butterfly":user_posts >= 5,
            "Influencer":      total_likes >= 100,
            "Multi-Talented":  n_hobbies >= 3,
        }

        for badge_name, condition in \
                checks.items():
            if condition:
                badge_info = BADGES[badge_name]
                earned.append({
                    "name":     badge_name,
                    "emoji":    badge_info["emoji"],
                    "desc":     badge_info["desc"],
                    "xp":       badge_info["xp"],
                    "color":    badge_info["color"],
                    "category": badge_info[
                        "category"
                    ],
                    "earned_at":datetime.now()
                                .strftime(
                                    "%Y-%m-%d"
                                ),
                })

        return earned

    def get_next_badges(self, user_data,
                        sessions, hobbies):
        """Get badges user is close to earning."""
        uid = user_data.get("user_id","")
        total_sessions = len([
            s for s in sessions
            if s.get("user_id") == uid
        ])
        total_hours = sum(
            s.get("duration_hrs", 0)
            for s in sessions
            if s.get("user_id") == uid
        )
        streak = user_data.get(
            "current_streak", 0
        )

        upcoming = []

        targets = [
            ("Week Warrior",   "streak",   7,
             streak),
            ("Month Master",   "streak",   30,
             streak),
            ("50 Hours",       "hours",    50,
             total_hours),
            ("100 Hours",      "hours",    100,
             total_hours),
            ("Century Club",   "sessions", 100,
             total_sessions),
        ]

        for name, metric, target, current \
                in targets:
            if current < target:
                pct  = round(
                    current / target * 100, 1
                )
                left = round(target - current, 1)
                badge= BADGES[name]
                upcoming.append({
                    "name":    name,
                    "emoji":   badge["emoji"],
                    "color":   badge["color"],
                    "progress":pct,
                    "left":    left,
                    "metric":  metric,
                    "target":  target,
                    "current": round(current, 1),
                })

        return sorted(
            upcoming,
            key=lambda x: x["progress"],
            reverse=True
        )[:4]

    def get_all_badges(self):
        """Get all available badges."""
        return [
            {
                "name":     name,
                **info,
            }
            for name, info in BADGES.items()
        ]