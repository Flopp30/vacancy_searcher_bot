from sqlalchemy import (Column, BigInteger, VARCHAR, ForeignKey,
                        Integer, Boolean, text, String)
from sqlalchemy.orm import relationship, validates
from db.models.base import CustomBaseModel, BaseModel


class GradeTypes(BaseModel):
    """
    Grade type
    """
    __tablename__ = "grade_types"

    id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(128), nullable=False)


class WorkTypes(BaseModel):
    """
    Work types
    """
    __tablename__ = "work_types"

    id = Column(Integer, primary_key=True)
    type = Column(VARCHAR(128), nullable=False)


class Profile(
    CustomBaseModel,
):
    """
    Profile model
    """
    __tablename__ = "profiles"

    firstname = Column(VARCHAR(32))
    lastname = Column(VARCHAR(32))

    email = Column(
        String(255),
        server_default=text("''"),
    )

    professional_role = Column(VARCHAR(32))

    work_type_id = Column(Integer, ForeignKey("work_types.id"))
    work_type = relationship(WorkTypes, backref="profile")

    grade_type_id = Column(Integer, ForeignKey("grade_types.id"))
    grade_type = relationship(GradeTypes, backref="profile")

    region = Column(VARCHAR(32))

    salary_from = Column(Integer)
    salary_to = Column(Integer)

    ready_for_relocation = Column(Boolean, default=False)

    # telegram user id
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    user = relationship("User", uselist=False, back_populates="profile")

    @validates("email")
    def validate_email(self, key, address):
        """
        Email db validator
        :param key:
        :param address:
        :return:
        """
        return address
        # import re
        # from bot.settings import EMAIL_REG_EXP
        # if re.match(EMAIL_REG_EXP, address):
        #     return address
        # raise ValueError

    @validates("salary_from", "salary_to")
    def validate_numbers(self, key, number_):
        """
        Salary db validator
        :param number_:
        :param key:
        :return:
        """
        return int(number_)
