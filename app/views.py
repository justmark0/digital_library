from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.forms import LoginForm
from app.models import User


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect('/library')
    form = LoginForm()
    if form.validate_on_submit():
        if 'innopolis' not in form.email.data:
            #flash('Sorry! Your email is invalid for this resource.')
            return redirect(url_for('index'))
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        if not user.check_password(form.password.data):
            #flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/library', methods=['GET', 'POST'])
def library():
    if current_user.is_authenticated:
        return 'Hello ' + current_user.email.split('@')[0] + '''<div>
        <a href="''' + url_for('logout') + '''">Logout</a> </div>'''
    else:
        return 'Your are not authenticated!'