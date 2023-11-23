# models.py
from app import USERS
import re


class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = 0
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @staticmethod
    def is_valid_id(user_id):
        if user_id < 0 or user_id >= len(USERS):
            return False
        return True

    def add_post(self, post):
        self.posts.append(post.to_dict())

    def add_reaction(self, reaction):
        self.total_reactions += 1
        post_id = reaction.post_id
        self.posts[int(post_id)]["reactions"].append(reaction.to_dict())


class Post:
    def __init__(self, post_id, author_id=0, text=""):
        self.post_id = post_id
        self.author_id = author_id
        self.text = text
        self.reactions = []

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": self.reactions,
        }


class Reaction:
    def __init__(self, post_id, user_id, user_reaction):
        self.post_id = post_id
        self.user_id = user_id
        self.user_reaction = user_reaction

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "user_reaction": self.user_reaction,
        }
