import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Lost(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'lost'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    school = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"))
    location = sqlalchemy.Column(sqlalchemy.String)
    imageLink = sqlalchemy.Column(sqlalchemy.String)
    userFound = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    schoolRelation = orm.relationship('School')
    user = orm.relationship('User')