"""
community_simulator.py
Simulates community feed, posts,
likes and comments.
"""

import random
import hashlib
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_IN")

POST_TEMPLATES = [
    "Just completed Day {day} of my "
    "{hobby} journey! 🔥 Feeling amazing!",
    "Reached {hours} hours of practice "
    "in {hobby}! Small steps = big results 💪",
    "New milestone unlocked in {hobby}! "
    "Never thought I'd get here 🎉",
    "Sharing my {hobby} progress for "
    "this week. Consistency is key! ✨",
    "Finally mastered a new technique "
    "in {hobby} today! 🎯",
    "Day {day} streak in {hobby}! "
    "Who else is on a learning journey? 🚀",
    "Just earned the '{badge}' badge "
    "for my {hobby} practice! 🏆",
    "My {hobby} session today was "
    "absolutely incredible! Here's what "
    "I learned 📚",
    "Started learning {hobby} {weeks} "
    "weeks ago. The progress is real! 💯",
    "Completed my weekly goal in "
    "{hobby}! Consistency beats talent 🌟",
]

COMMENT_TEMPLATES = [
    "This is so inspiring! Keep going! 🔥",
    "Amazing progress! You're killing it! 💪",
    "Wow, I'm also learning {hobby}! "
    "Let's connect!",
    "This motivated me to start today! 🙏",
    "Great work! What resources do you use?",
    "Incredible! How long did this take?",
    "You're an inspiration to us all! 🌟",
    "Keep up the great work! Almost there!",
    "This is exactly what I needed to see!",
    "Followed! Can't wait to see more! 👏",
]


class Post:
    """Represents a community post."""

    def __init__(self, user, hobby_name,
                 badge_name=None):
        self.post_id   = self._gen_id()
        self.user_id   = user.user_id
        self.user_name = user.name
        self.user_avatar = user.avatar
        self.hobby     = hobby_name
        self.content   = self._gen_content(
            hobby_name, badge_name
        )
        self.image_emoji = self._get_image()
        self.likes     = random.randint(0, 150)
        self.comments  = []
        self.tags      = self._gen_tags(
            hobby_name
        )
        self.created_at= (
            datetime.now() -
            timedelta(
                hours=random.randint(0, 168)
            )
        ).isoformat()
        self.is_pinned = False
        self.views     = random.randint(
            self.likes, self.likes * 5
        )
        self._seed_comments()

    def _gen_id(self):
        return "POST-" + hashlib.md5(
            str(datetime.now().timestamp())
            .encode()
        ).hexdigest()[:8].upper()

    def _gen_content(self, hobby, badge):
        tmpl = random.choice(POST_TEMPLATES)
        return tmpl.format(
            hobby=hobby,
            day=random.randint(1,100),
            hours=random.randint(10,500),
            badge=badge or "Streak Master",
            weeks=random.randint(1,52),
        )

    def _get_image(self):
        images = [
            "🎵","🎨","💻","💪","🧠",
            "✨","📚","🎯","🏆","🌟",
            "🔥","⭐","🎉","🚀","💯",
        ]
        return random.choice(images)

    def _gen_tags(self, hobby):
        base = [
            hobby.lower().replace(" ",""),
            "learning", "progress",
            "skills", "growth",
        ]
        return random.sample(base, 3)

    def _seed_comments(self):
        n = random.randint(0, 8)
        for _ in range(n):
            self.comments.append({
                "user":    fake.name(),
                "avatar":  random.choice(
                    ["👤","👩","👨","🧑"]
                ),
                "text":    random.choice(
                    COMMENT_TEMPLATES
                ).format(
                    hobby=self.hobby
                ),
                "time":    (
                    datetime.now() -
                    timedelta(
                        hours=random.randint(
                            0, 24
                        )
                    )
                ).strftime("%H:%M"),
                "likes":   random.randint(0,20),
            })

    def to_dict(self):
        return {
            "post_id":     self.post_id,
            "user_id":     self.user_id,
            "user_name":   self.user_name,
            "user_avatar": self.user_avatar,
            "hobby":       self.hobby,
            "content":     self.content,
            "image_emoji": self.image_emoji,
            "likes":       self.likes,
            "comments":    self.comments,
            "comment_count":len(self.comments),
            "tags":        self.tags,
            "created_at":  self.created_at,
            "is_pinned":   self.is_pinned,
            "views":       self.views,
        }


class CommunityManager:
    """Manages community feed and interactions."""

    def __init__(self, user_manager,
                 hobby_manager):
        self.posts        = []
        self.user_manager = user_manager
        self.hobby_manager= hobby_manager
        self._seed_posts(40)

    def _seed_posts(self, n=40):
        users = list(
            self.user_manager.users.values()
        )
        for _ in range(n):
            user  = random.choice(users)
            hobby = random.choice(
                user.hobbies
            ) if user.hobbies else "Reading"
            post  = Post(user, hobby)
            self.posts.append(post)

        # Sort by time
        self.posts.sort(
            key=lambda x: x.created_at,
            reverse=True,
        )

    def get_feed(self, limit=20,
                 category=None):
        posts = self.posts
        if category and category != "All":
            posts = [
                p for p in posts
                if any(
                    cat_hobby in p.hobby
                    for cat_hobby in
                    __import__(
                        "simulation.hobby_simulator",
                        fromlist=["HOBBY_CATEGORIES"]
                    ).HOBBY_CATEGORIES.get(
                        category, []
                    )
                )
            ]
        return [
            p.to_dict()
            for p in posts[:limit]
        ]

    def add_post(self, user, hobby,
                 content):
        post         = Post(user, hobby)
        post.content = content
        self.posts.insert(0, post)
        return post

    def like_post(self, post_id):
        for p in self.posts:
            if p.post_id == post_id:
                p.likes += 1
                return True
        return False

    def add_comment(self, post_id,
                    user_name, text):
        for p in self.posts:
            if p.post_id == post_id:
                p.comments.append({
                    "user":   user_name,
                    "avatar": "👤",
                    "text":   text,
                    "time":   datetime.now()
                             .strftime("%H:%M"),
                    "likes":  0,
                })
                return True
        return False

    def get_trending_tags(self):
        from collections import Counter
        all_tags = []
        for p in self.posts:
            all_tags.extend(p.tags)
        return Counter(all_tags).most_common(10)

    def get_stats(self):
        total_likes = sum(
            p.likes for p in self.posts
        )
        total_comments = sum(
            len(p.comments)
            for p in self.posts
        )
        return {
            "total_posts":    len(self.posts),
            "total_likes":    total_likes,
            "total_comments": total_comments,
            "total_views":    sum(
                p.views for p in self.posts
            ),
            "avg_likes":      round(
                total_likes /
                max(len(self.posts),1), 1
            ),
        }