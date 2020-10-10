from flask import render_template, request, redirect
from app import app, db


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        return redirect('/library')

