from base.properties import pretty_names
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from .forms import (
    AddUser,
    CreateAccountForm,
    DeleteUser,
    LoginForm,
    TacacsServerForm
)
from passlib.hash import cisco_type7
from .properties import user_search_properties
from sqlalchemy.orm.exc import NoResultFound
from tacacs_plus.client import TACACSClient
from tacacs_plus.flags import TAC_PLUS_AUTHEN_TYPE_ASCII
import flask_login

# start the login system
login_manager = flask_login.LoginManager()

blueprint = Blueprint(
    'users_blueprint',
    __name__,
    url_prefix='/users',
    template_folder='templates',
    static_folder='static'
)

from base.database import db
from .models import User, TacacsServer


@blueprint.route('/overview')
@login_required
def users():
    return render_template(
        'users_overview.html',
        fields=user_search_properties,
        names=pretty_names,
        users=User.query.all()
    )


@blueprint.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    add_user_form = AddUser(request.form)
    delete_user_form = DeleteUser(request.form)
    print('ttt'*100, request.form)
    if 'add_user' in request.form:
        kwargs = request.form.to_dict()
        password = kwargs.pop('password')
        kwargs['password'] = cisco_type7.hash(password)
        user = User(**kwargs)
        db.session.add(user)
    elif 'delete_user' in request.form:
        selection = delete_user_form.data['users']
        db.session.query(User).filter(User.username.in_(selection))\
            .delete(synchronize_session='fetch')
    if request.method == 'POST':
        db.session.commit()
    all_users = User.choices()
    delete_user_form.users.choices = all_users
    return render_template(
        'manage_users.html',
        add_user_form=add_user_form,
        delete_user_form=delete_user_form
    )

## Login & Registration


@blueprint.route('/create_account', methods=['GET', 'POST'])
def create_account():
    print('ttt'*100, request.form)
    if request.method == 'GET':
        form = CreateAccountForm(request.form)
        return render_template('login/create_account.html', form=form)
    else:
        kwargs = request.form.to_dict()
        password = kwargs.pop('password')
        kwargs['password'] = cisco_type7.hash(password)
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    print('ttt'*100, request.form)
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        user = db.session.query(User).filter_by(username=username).first()
        if user and cisco_type7.verify(password, user.password):
            flask_login.login_user(user)
            return redirect(url_for('base_blueprint.dashboard'))
        else:
            try:
                # tacacs_plus does not support py2 unicode, hence the
                # conversion to string.
                # TACACSClient cannot be saved directly to session
                # as it is not serializable: this temporary fixes will create
                # a new instance of TACACSClient at each TACACS connection
                # attemp: clearly suboptimal, to be improved later.
                encrypted_password = cisco_type7.hash(password)
                tacacs_server = db.session.query(TacacsServer).one()
                tacacs_client = TACACSClient(
                    str(tacacs_server.ip_address),
                    int(tacacs_server.port),
                    str(cisco_type7.decode(str(tacacs_server.password)))
                )
                if tacacs_client.authenticate(
                    username,
                    password,
                    TAC_PLUS_AUTHEN_TYPE_ASCII
                ).valid:
                    user = User(username=username, password=encrypted_password)
                    db.session.add(user)
                    db.session.commit()
                    flask_login.login_user(user)
                    return redirect(url_for('base_blueprint.dashboard'))
            except NoResultFound:
                pass
        return render_template('errors/page_403.html')
    if not flask_login.current_user.is_authenticated:
        form = LoginForm(request.form)
        return render_template('login/login.html', form=form)
    return redirect(url_for('base_blueprint.dashboard'))


@blueprint.route('/logout')
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('users_blueprint.login'))


@blueprint.route('/tacacs_server', methods=['GET', 'POST'])
@login_required
def tacacs_server():
    print('ttt'*100, request.form)
    if request.method == 'POST':
        tacacs_server = TacacsServer(**request.form)
        db.session.add(tacacs_server)
        db.session.commit()
    return render_template(
        'tacacs_server.html',
        form=TacacsServerForm(request.form)
    )
