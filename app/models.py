# models.py
import re
from app import USERS


class User:
    def __init__(self, user_id, first_name, last_name, email, total_reactions=0):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = []
        self.status = "created"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions,
            "status": self.status,
        }

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @staticmethod
    def is_valid_id(user_id):
        return 0 <= user_id < len(USERS) and USERS[user_id].status != "deleted"

    def add_post(self, post):
        if post.status != "deleted":
            self.posts.append(post.to_dict())

    def add_reaction(self, reaction):
        user = USERS[reaction.user_id]
        user.total_reactions += 1
        post_id = reaction.post_id
        self.posts[int(post_id)]["reactions"].append(reaction.to_dict())


class Post:
    def __init__(self, post_id, author_id=0, text=""):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []
        self.status = "created"

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
            "status": self.status,
        }

    @staticmethod
    def is_valid_id(user_id, post_id):
        post_status = USERS[user_id].posts[post_id]["status"]
        return (
            0 <= user_id < len(USERS)
            and 0 <= post_id < len(USERS[user_id].posts)
            and post_status != "deleted"
        )


class Reaction:
    def __init__(self, post_id, user_id, user_reaction):
        self.post_id = post_id
        self.user_id = user_id
        self.user_reaction = user_reaction
        self.status = "created"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_reaction": self.user_reaction,
        }

    @staticmethod
    def is_valid_reaction(reaction):
        return reaction in ["like", "dislike"]
