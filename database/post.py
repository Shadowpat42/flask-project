from __future__ import annotations
from typing import List

from .db import db
from .reaction import Reaction


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    text = db.Column(db.String)

    def get_reactions(self) -> List[Reaction]:
        """
        Get reactions for the user.
        Returns:
            List[Reaction]: A list of Reaction objects.
        """
        reactions = Reaction.get_by_user_id(self.user_id)
        return reactions

    @classmethod
    def get_by_user_id(cls, user_id: int) -> List[Post]:
        """
        Retrieve a list of posts by a given user ID.

        Args:
            user_id (int): The ID of the user whose posts are to be retrieved.

        Returns:
            List[Post]: A list of post objects associated with the given user ID.
        """
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_id(cls, id: int) -> Post:
        """
        Retrieve a Post by its ID.

        Args:
            id (int): The ID of the Post to retrieve.

        Returns:
            Post: The Post object with the specified ID.
        """
        return cls.query.get(id).first()

    def save(self) -> None:
        """
        Save the current object in the database session and commit the changes.
        """
        db.session.add(self)
        db.session.commit()