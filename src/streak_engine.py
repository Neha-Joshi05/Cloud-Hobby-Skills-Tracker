"""
streak_engine.py
Calculates streaks and consistency scores.
"""

import random
from datetime import datetime, timedelta
import numpy as np


class StreakEngine:
    """
    Tracks daily practice streaks.
    Rewards consistency over intensity.
    """

    def __init__(self):
        self.streak_history = {}

    def calculate_streak(self, sessions,
                         user_id):
        """Calculate current streak from sessions."""
        if not sessions:
            return 0, 0

        dates = sorted(set(
            s["date"] for s in sessions
            if s.get("user_id") == user_id
        ), reverse=True)

        if not dates:
            return 0, 0

        current = 0
        longest = 0
        temp    = 0
        today   = datetime.now().strftime(
            "%Y-%m-%d"
        )
        yesterday = (
            datetime.now() - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        # Check if streak is active
        if dates[0] not in [today, yesterday]:
            current = 0
        else:
            # Count consecutive days
            check_date = datetime.strptime(
                dates[0], "%Y-%m-%d"
            )
            for i, date_str in enumerate(dates):
                d = datetime.strptime(
                    date_str, "%Y-%m-%d"
                )
                expected = check_date - \
                           timedelta(days=i)
                if d == expected:
                    current += 1
                    temp    += 1
                    longest  = max(longest, temp)
                else:
                    temp = 0

        return current, max(longest, current)

    def get_weekly_activity(self, sessions,
                            user_id):
        """Get activity for last 7 days."""
        result = {}
        for i in range(7):
            date = (
                datetime.now() -
                timedelta(days=i)
            ).strftime("%Y-%m-%d")
            day_sessions = [
                s for s in sessions
                if s.get("user_id") == user_id
                and s.get("date") == date
            ]
            result[date] = {
                "count": len(day_sessions),
                "minutes": sum(
                    s.get("duration_min", 0)
                    for s in day_sessions
                ),
            }
        return result

    def get_consistency_score(self, sessions,
                              user_id,
                              days=30):
        """
        Consistency score 0-100.
        Based on % of days practiced.
        """
        if not sessions:
            return 0

        dates = set(
            s["date"] for s in sessions
            if s.get("user_id") == user_id
        )
        active_days = len(dates)
        return round(
            min(active_days / days * 100, 100),
            1
        )

    def get_heatmap_data(self, sessions,
                         user_id, weeks=12):
        """Generate heatmap data for GitHub-style chart."""
        result = {}
        for i in range(weeks * 7):
            date = (
                datetime.now() -
                timedelta(days=i)
            ).strftime("%Y-%m-%d")
            day_sessions = [
                s for s in sessions
                if s.get("user_id") == user_id
                and s.get("date") == date
            ]
            result[date] = sum(
                s.get("duration_min", 0)
                for s in day_sessions
            )
        return result

    def simulate_streak_update(self, user):
        """Simulate daily streak update."""
        user_dict = user.to_dict() \
            if hasattr(user, "to_dict") \
            else user
        streak = user_dict.get(
            "current_streak", 0
        )
        if random.random() > 0.2:
            streak += 1
        else:
            streak = 0
        return streak