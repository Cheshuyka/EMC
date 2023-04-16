import flask
from . import db_session
from .schools import School
from flask import jsonify


blueprint = flask.Blueprint(
    'schools_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/schools')  # api для школ
def get_users():
    db_sess = db_session.create_session()
    schools = db_sess.query(School).all()
    return jsonify(
        {
            'schools':
                [item.to_dict(only=('id', 'title'))
                 for item in schools]
        }
    )