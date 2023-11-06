# models.py

class User:
    def __init__(self, id, first_name, last_name, email, total_reactions=0, posts=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = posts


