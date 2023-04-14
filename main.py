from data import db_session
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from data.schools import School
from data.lost import Lost
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_know_its_a_secret_key_really_secret'

login_manager = LoginManager()
login_manager.init_app(app)


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddSchool(FlaskForm):
    name = EmailField('Название школы', validators=[DataRequired()])
    idAdmin = IntegerField('ID Админа', validators=[DataRequired()])
    submit = SubmitField('Добавить')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('mainPage.html', title='EMC')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть", background='white')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Авторизация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/change_profile', methods=['POST', 'GET'])
@login_required
def change():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if not(user):
        abort(520)
    if len(request.args['name']) > 0:
        user.name = request.args['name']
    if len(request.args['surname']) > 0:
        user.surname = request.args['surname']
    if len(request.args['school']) > 0:
        user.school = request.args['school']
    if request.args['position'] != 'Не выбрано':
        user.position = request.args['position']
    if len(request.args['classClub']) > 0:
        user.classClub = request.args['classClub']
    if len(request.args['email']) > 0:
        user.email = request.args['email']
    db_sess.commit()
    return redirect('/profile')


@app.route('/send_request', methods=['POST', 'GET'])
@login_required
def send_request():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user.verified == 0:
        return render_template('profile.html', message='Заявка уже была подана')
    if user.school == None:
        return render_template('profile.html', message='Не указана школа')
    if user.position == 'Учитель' or user.position == 'Ученик':
        if user.classClub == None:
            return render_template('profile.html', message='Не указан класс')
        user.verified = 0
        db_sess.commit()
        return render_template('profile.html', message='Заявка подана')
    elif user.position == 'Админ школы':
        user.verified = 0
        db_sess.commit()
        return render_template('profile.html', message='Заявка подана')
    return render_template('profile.html', message='Не выбрана роль')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Авторизация')


@app.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    db_sess = db_session.create_session()
    if current_user.position == 'Учитель':
        users = db_sess.query(User).filter(User.position == 'Ученик', User.classClub == current_user.classClub,
                                           User.verified == 0, User.school == current_user.school).all()
    elif current_user.position == 'Админ школы':
        users = db_sess.query(User).filter((User.position == 'Учитель') | (User.position == 'Ученик') | (User.position == 'Админ школы'),
                                           User.verified == 0, User.school == current_user.school).all()
    else:
        abort(403)
    return render_template('requests.html', title='Авторизация', users=users)


@app.route('/schools', methods=['GET', 'POST'])
@login_required
def schools():
    form = AddSchool()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        school = db_sess.query(School).filter(School.title == form.name.data).first()
        admin = db_sess.query(User).filter(User.id == form.idAdmin.data).first()
        if school or not(admin):
            return render_template('school.html', form=form, title='Добавление школы')
        if admin.position != 'Админ школы':
            return render_template('school.html', form=form, title='Добавление школы')
        school = School(title=form.name.data)
        db_sess.add(school)
        school = db_sess.query(School).filter(School.title == school.title).first()
        admin.school = school.id
        admin.verified = 2
        db_sess.commit()
        return redirect('/')
    return render_template('school.html', title='Добавление школы', form=form)


@app.route('/accept_request/<int:id>')
@login_required
def accept_request(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.verified = 2
    db_sess.commit()
    return redirect('/requests')


@app.route('/cancel_request/<int:id>')
@login_required
def cancel_request(id):
    db_sess = db_session.create_session()
    cancel = request.args['cancel']
    user = db_sess.query(User).filter(User.id == id).first()
    user.whyCancelled = cancel
    user.verified = 1
    db_sess.commit()
    return redirect('/requests')


@app.route('/lostList')
@login_required
def lostList():
    db_sess = db_session.create_session()
    lost = db_sess.query(Lost).filter(Lost.school == current_user.school).order_by(Lost.userFound != current_user.id).all()
    return render_template('lostList.html', lost=lost)


@app.route('/lost/<int:id>')
@login_required
def lost(id):
    db_sess = db_session.create_session()
    lost = db_sess.query(Lost).filter(Lost.school == current_user.school, Lost.id == id).first()
    return render_template('lost.html', lost=lost)


@app.route('/addLost')
@login_required
def addLost():
    pass


@app.route('/deleteLost/<int:id>')
@login_required
def deleteLost(id):
    db_sess = db_session.create_session()
    lost = db_sess.query(Lost).filter(Lost.id == id).first()
    db_sess.delete(lost)
    db_sess.commit()
    lost = db_sess.query(Lost).filter(Lost.school == current_user.school).order_by(Lost.userFound != current_user.id).all()
    return render_template('lostList.html', lost=lost)


def security():  # TODO: проверка юзеров (в случае, если сайт введен в адресной строке)
    pass


if __name__ == '__main__':
    db_session.global_init('db/EMC.db')
    # db_sess = db_session.create_session()
    # lost = Lost(
    #    title='Планшет',
    #    school=1,
    #    location='кабинет физики',
    #    imageLink="/static/img/example.png",
    #    userFound=2
    # )
    # db_sess.add(lost)

    # user = User(
    #    surname='Власов',
    #    name='Илья',
    #    position='Создатель',
    #    email='chief@gmail.com',
    #    verified=2
    # )
    # user.set_password('268268268268a')
    # db_sess.add(user)
    # db_sess.commit()
    app.run()