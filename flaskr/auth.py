import functools
from flask import Blueprint, flash, g, redirect, render_template, \
      request, session, url_for

#from model import user, blog as userModel, blogModel
from model import user as userModel
from db import registerUser

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = userModel.objects(id=user_id)[0]

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if username is None:
            error = 'username is empty'
        elif password is None:
            error = 'password is empty'
        elif userModel.objects(username=username).count() != 0:
            error = 'user is exisited'
        
        if error is None:
            user = registerUser(username, password) 
            return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        userSet = userModel.objects(username=username)
        if userSet.count() == 0:
            error = 'user not found'
        elif userSet[0].password != password:
            error = 'password is not correct'
        
        if error is None:
            session.clear()
            session['user_id'] = userSet[0].id
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrappedView(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))
        
        return view(**kwargs)

    return wrappedView