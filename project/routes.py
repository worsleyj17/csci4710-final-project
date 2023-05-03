import os
import secrets

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort

from project import app, db, bcrypt
from project.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from project.models import User, Post

from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def splash():
	return render_template('splash.html')

@app.route("/main")
def main():
    posts = Post.query.all()
    return render_template('main.html', posts=posts)

@app.route("/upcoming")
def upcoming():
    return render_template('upcoming.html')
	
@app.route("/team")
def team():
    return render_template('team.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # if already logged in, redirect to home page
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main'))
        else:
            flash('Error, double check username and password.', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated', 'success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('settings.html', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main'))
    return render_template('createPost.html', form=form, legend='Create a Post!')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm()
	
	
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
		
    return render_template('createPost.html', form=form, legend='Edit Post')
