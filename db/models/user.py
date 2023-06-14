"""
User model
"""

from sqlalchemy.orm import relationship

from db.models.base import CustomBaseModel


class User(
    CustomBaseModel,
):
    """
    User model
    """
    __tablename__ = "users"

    profile = relationship("Profile", uselist=False, back_populates="user")

    def __str__(self):
        return f"<User:{self.id}>"
