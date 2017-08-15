from flask import render_template, flash, redirect,g
from app import app
from .forms import LoginForm
from .bims import authenticate_user, get_salesevents

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname' : 'giles'}
    auctions = [
        {'id' : '1', 'capacity' : '10', 'vehicle' : 'ABC'},
        {'id' : '2', 'capacity' : '5', 'vehicle' : 'DEF'}
    ]

    auctions = get_salesevents()

    return render_template('index.html',jtiToken=g.jtiToken, user = user, auctions = auctions)


@app.route('/login', methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        g.jtiToken = authenticate_user()
        flash('Login requested for ID = "%s", rememberMe=%s' % (g.jtiToken, str(form.rememberMe.data)))

        return redirect('/index')

    return render_template('login.html', title='Sign In', form = form)

