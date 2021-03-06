from flask import url_for, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from mainApp import app, db
from mainApp.models import Message, User


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/main')
@login_required
def main():
    if current_user.login == 'maxim':
        return render_template('main.html', messages=Message.query.all())
    return 'Nope! You have no access to this page!'



@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    # messages.append(Message(text, tag))
    db.session.add(Message(text, tag))
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main'))
        else:
            flash('Wrong password!')
    else:
        flash('Please fill login and password')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not(login or password or password2):
            flash('Please, fill in all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response
