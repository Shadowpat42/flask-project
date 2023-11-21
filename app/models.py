# models.py
import re


class User:
    def __init__(self, id, first_name, last_name, email, total_reactions=0):
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


class Post:
    def __init__(self, author_id=0, text="", reactions=[]):
        self.author_id = author_id
        self.text = text
        self.reactions = reactions
