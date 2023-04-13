import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class School(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'schools'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    user = orm.relationship("User", back_populates='schoolRelation')
    lost = orm.relationship("Lost", back_populates='schoolRelation')