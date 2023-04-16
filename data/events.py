import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Events(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'events'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    school = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"))
    description = sqlalchemy.Column(sqlalchemy.Text)
    classClub = sqlalchemy.Column(sqlalchemy.String)
    userCreated = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    schoolRelation = orm.relationship('School')