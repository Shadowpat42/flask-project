from __future__ import annotations
import re
from typing import List

from sqlalchemy import desc as reverse

from .db import db
from .post import Post
from .reaction import Reaction


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    def json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "total_reactions": self.total_reactions
        }
    
    @property
    def total_reactions(self):
        return len(Reaction.get_by_user_id(self.id))

    @staticmethod
    def is_valid_email(email: str) -> bool:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @classmethod
    def all(cls) -> List[User]:
        """
        Retrieve all users from the database.

        Returns:
            List[User]: A list of all User objects in the database.
        """
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id: int) -> User:
        """
        Retrieve a user by their ID.

        Args:
            id (int): The ID of the user to retrieve.

        Returns:
            User: The user with the specified ID.
        """
        return cls.query.get(id)

    @classmethod
    def get_by_reactions(cls, desc: bool = False) -> List[User]:
        if not desc:
            return cls.query.all()
        else:
            return cls.query.order_by(reverse(cls.total_reactions)).all()

    
    def posts(self) -> List[Post]:
        """
        Get posts for the user.
        Returns:
            List[Post]: A list of Post objects.
        """
        posts = Post.get_by_user_id(self.id)
        return posts

    def save(self) -> None:
        """
        Save the current object to the database session.
        No parameters.
        Returns None.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        """
        Delete the current object from the database session.
        """
        for post in self.posts():
            post.delete()

        for reaction in Reaction.get_by_user_id(self.id):
            reaction.delete()

        db.session.delete(self)
        db.session.commit()