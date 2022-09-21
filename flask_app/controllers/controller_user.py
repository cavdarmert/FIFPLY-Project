from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User
#MAY NOT NEED BELOWS, WILL CHECK LATER !!!
from flask_app.models.model_post import Post
##CHECK BELOW TOO, MAY NOT NEED HERE!
from flask_bcrypt import Bcrypt
##CHECK BELOW TOO, MAY NOT NEED HERE!
app.secret_key = "keep it safe"
##CHECK BELOW TOO, MAY NOT NEED HERE!
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'id' in session:
        return redirect ('/dashboard')
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.is_valid(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    session['id'] = User.new_user(data)
    return redirect ('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash('Please login before going to dashboard!')
        return redirect ('/')
    user = User.get_one_by_id(int(session['id']))  
    return render_template('dashboard.html', user=user, posts=Post.get_all())

@app.route('/login', methods=['POST'])
def login():
    user_to_check = User.get_one_by_email(request.form['email'])
    if not user_to_check:
        flash('Invalid credentials')
        return redirect('/')
    if not bcrypt.check_password_hash(user_to_check.password, request.form['password']):
        flash('Invalid credentials')
        return redirect('/')
    session['id'] = user_to_check.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    del session['id']
    flash('User Just Logged Out!')
    return redirect('/')

@app.route('/why')
def why():
    if 'id' not in session:
        return redirect ('/')
    return render_template('why.html')
