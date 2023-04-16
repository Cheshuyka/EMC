import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    school = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.id"), nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, default='Не выбрано')
    classClub = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    verified = sqlalchemy.Column(sqlalchemy.Integer, default=1)  # 0: заявка рассматривается; 1: в заявке отказано/ее не подавали; 2: заявка принята
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    whyCancelled = sqlalchemy.Column(sqlalchemy.String, default='Вам еще не отказывали')
    schoolRelation = orm.relationship('School')
    lost = orm.relationship("Lost", back_populates='user')
    event = orm.relationship("Events", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)