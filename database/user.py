from __future__ import annotations

from .db import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    total_reactions = db.Column(db.Integer, default=0)

    @classmethod
    def get_by_id(cls, id: int) -> User:
        """
        Retrieve a user by their ID.

        Args:
            id (int): The ID of the user to retrieve.

        Returns:
            User: The user with the specified ID.
        """
        return cls.query.get(id).first()

    def total_reactions_inc(self) -> None:
        """
        Increments the total number of reactions by 1 if it exists, otherwise sets it to 1.
        """
        if not self.total_reactions:
            self.total_reactions = 1
        else:
            self.total_reactions += 1

    def save(self) -> None:
        """
        Save the current object to the database session.
        No parameters.
        Returns None.
        """
        db.session.add(self)
        db.session.commit()
