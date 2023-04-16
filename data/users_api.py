import flask
from . import db_session
from .users import User
from flask import jsonify


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')  # api для пользователей
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'school', 'position', 'classClub'))
                 for item in users]
        }
    )