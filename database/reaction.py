from __future__ import annotations
from enum import Enum
from typing import List

from .db import db


class ReactionType(Enum):
    LIKE = "like"
    DISLIKE = "dislike"

class Reaction(db.Model):
    __tablename__ = "reaction"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    reaction = db.Column(db.Enum(ReactionType))

    @classmethod
    def get_by_user_id(cls, user_id: int) -> List[Reaction]:
        """
        Get reactions by user ID.
        
        Args:
            user_id (int): The ID of the user.
        
        Returns:
            List[Reaction]: A list of Reaction objects.
        """
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_post_id(cls, post_id: int) -> List[Reaction]:
        """
        Retrieves reactions by post_id.

        Args:
            post_id (int): The ID of the post.

        Returns:
            List[Reaction]: A list of Reaction objects.
        """
        return cls.query.filter_by(post_id=post_id).all()
    
    @classmethod
    def get_by_id(cls, id: int) -> Reaction:
        """
        Retrieve a Reaction object by its ID.

        Args:
            id (int): The ID of the Reaction object to retrieve.

        Returns:
            Reaction: The Reaction object with the specified ID, or None if not found.
        """
        return cls.query.get(id)
    
    def save(self) -> None:
        """
        Save the current object to the database session.
        """
        db.session.add(self)
        db.session.commit()