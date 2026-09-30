"""
data_store.py
Simulates cloud database storage.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


class DataStore:
    """Simulates Firebase Firestore / AWS DynamoDB."""

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.activity_log = []
        self._generate_history()

    def _generate_history(self, days=30):
        """Generate 30-day historical data."""
        now = datetime.now()
        for i in range(days, 0, -1):
            date = (
                now - timedelta(days=i)
            ).strftime("%Y-%m-%d")
            n_sessions = random.randint(10, 80)
            self.activity_log.append({
                "date":       date,
                "sessions":   n_sessions,
                "hours":      round(
                    n_sessions *
                    random.uniform(0.5, 1.5),
                    1
                ),
                "new_users":  random.randint(0,5),
                "posts":      random.randint(2,15),
                "likes":      random.randint(
                    20, 200
                ),
                "xp_earned":  n_sessions *
                              random.randint(50,150),
            })

    def get_activity_df(self):
        return pd.DataFrame(self.activity_log)

    def get_platform_stats(self):
        df = self.get_activity_df()
        if df.empty:
            return {}
        return {
            "total_sessions": int(
                df["sessions"].sum()
            ),
            "total_hours":    round(
                df["hours"].sum(), 1
            ),
            "total_posts":    int(
                df["posts"].sum()
            ),
            "total_likes":    int(
                df["likes"].sum()
            ),
            "total_xp":       int(
                df["xp_earned"].sum()
            ),
            "avg_daily_sessions": round(
                df["sessions"].mean(), 1
            ),
            "peak_day":       df.loc[
                df["sessions"].idxmax(),
                "date"
            ],
        }