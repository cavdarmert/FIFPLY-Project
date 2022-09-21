from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_post import Post
#MAY NOT NEED BELOW, WILL CHECK LATER !!!
from flask_app.models.model_user import User


@app.route("/posts/new")
def new_post():
    if 'id' not in session:
        flash('Plesae login before trying to go to dashboard page')
        return redirect('/')
        ##below edited, line below was not there, I added, and return didn't have the second argument, initially.
        ##ABOVE FROM CONTROLLER_USER line 34
    user = User.get_one_by_id(int(session['id']))
    return render_template("new_post.html", user=user)

@app.route('/posts/create', methods=['POST'])
def create_post():
    if not Post.is_valid(request.form):
        return redirect('/posts/new')
    #CREATING A POST BELOW
    data = {
        **request.form,
        'user_id': session['id']
    }
    Post.save(data)
    return redirect('/dashboard')

@app.route('/posts/<int:id>/view')
def show_one_post(id):
    if 'id' not in session:
        flash('Please login first!')
        return redirect('/')
    data = {'id':id}
    post = Post.get_one_by_id(data)
    user = User.get_one_by_id(int(session['id']))
    return render_template("show_post.html", post=post, user=user)

@app.route('/posts/<int:id>/delete')
def delete_post(id):
    if 'id' not in session:
        flash('Please login first!')
        return redirect('/')
    data = {'id':id}
    post = Post.get_one_by_id(data)
    if post.user_id != session['id']:
        flash("You can't DELETE this post!")
        return redirect('/dashboard')
    Post.delete_by_id(data)
    return redirect('/dashboard')

@app.route('/posts/<int:id>/edit')
def edit_post_form(id):
    data = {'id':id}
    post = Post.get_one_by_id(data)
    if post.user_id != session['id']:
        flash("You can't EDIT this post!")
        return redirect('/dashboard')
    user = User.get_one_by_id(int(session['id']))
    return render_template("edit_post.html", post=post, user=user)

@app.route('/posts/<int:id>/update', methods=['POST'])
def update_post(id):
    updated_info = {
        **request.form,
        'id': id
    }
    post = Post.get_one_by_id(updated_info)
    if post.user_id != session['id']:
        flash("HEY!!! You can't EDIT this post!")
        return redirect('/dashboard')

    if not Post.is_valid(updated_info):
        return redirect(f'/posts/{id}/edit')

    Post.update(updated_info)
    return redirect('/dashboard')
    