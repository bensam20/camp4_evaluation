from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Blogs, Users, Comments
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def greet():
    return "Good Day"



@views.route("/login/", methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@views.route("/dashboard/", methods=("GET", "POST"))
@login_required
def dashboard():
    blogs = Blogs.query.order_by(Blogs.id.desc()).all()
    authors={}
    for user in Users.query.all():
        authors[user.id] = user.name
    return render_template("dashboard.html", user=current_user, blogs=blogs, authors=authors)


@views.route("/post/<int:blogId>", methods=("GET", "POST"))
@login_required
def post(blogId):
    if request.method == 'POST':
        comment = request.form.get('comment')
        userId = current_user.id
        blogId = blogId
        print(blogId)
        print(f"{comment}, {userId}, {blogId}")
        new_comment = Comments(body=comment, user_id=userId, blog_id=blogId)
        # db.session.add(new_comment)
        # db.session.commit()
        flash('Comment added!', category='success')
    authors={}
    for user in Users.query.all():
        authors[user.id] = user.name
    post = Blogs.query.get(blogId)
    return render_template('post.html', post=post, user=current_user,authors=authors)