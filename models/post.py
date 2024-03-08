from __future__ import annotations
from typing import List

from sqlalchemy import desc

from .db import db
from .reaction import Reaction


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, default=0)
    text = db.Column(db.String)

    def json(self):
        return {
            "post_id": self.id,
            "author_id": self.author_id,
            "text": self.text,
            "reactions": [reaction.json() for reaction in self.get_reactions()]
        }

    def get_reactions(self) -> List[Reaction]:
        """
        Get reactions for the user.
        Returns:
            List[Reaction]: A list of Reaction objects.
        """
        reactions = Reaction.get_by_user_id(self.author_id)
        return reactions

    @classmethod
    def get_by_user_id(cls, author_id: int, desc: bool = False) -> List[Post]:
        """
        Retrieve a list of posts by a given user ID.

        Args:
            author_id (int): The ID of the user whose posts are to be retrieved.

        Returns:
            List[Post]: A list of post objects associated with the given user ID.
        """
        if not desc:
            return cls.query.filter_by(author_id=author_id).all()
        else:
            return cls.query.filter_by(author_id=author_id).order_by(desc(cls.id)).all()
    
    @classmethod
    def get_by_id(cls, id: int) -> Post:
        """
        Retrieve a Post by its ID.

        Args:
            id (int): The ID of the Post to retrieve.

        Returns:
            Post: The Post object with the specified ID.
        """
        return cls.query.get(id)

    def save(self) -> None:
        """
        Save the current object in the database session and commit the changes.
        """
        db.session.add(self)
        db.session.commit()
    
    def delete(self) -> None:
        """
        Delete the current object from the database session.
        """
        db.session.delete(self)
        db.session.commit()