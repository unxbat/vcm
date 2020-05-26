#!/usr/bin/env
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, make_response, send_file, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.models import User, Video
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is None or (current_user.username==form.username.data ):
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash('Your changes have been saved.')
        else:
            flash(f'Current username "{form.username.data}" is busy, please choose another one')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# noinspection PyArgumentList
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     form = MediaForm()
#     if form.validate_on_submit():
#         file = form.media.data
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.instance_path, 'media', filename))
#         return redirect(url_for('index'))
#
#     return render_template('upload.html', title='Upload file', form=form)

@app.route('/videos', methods=['GET'])
@login_required
def videos():
    video_list = Video.query.all()
    return render_template('videos.html', title='Videos', video_list=video_list)


# @app.route('/player/<video>', headers=)
# @login_required
# def player(video):
#     v = Video.query.filter_by(name=video).first()
#     return render_template('player.html', video=v) эта  залупа не рабоатет

@app.route('/player/<video>')
@login_required
def player(video):
    v = Video.query.filter_by(name=video).first()
    resp = make_response(send_file(v.full_path, 'video/mp4'))
#    return render_template('player.html', video=v)
    resp.headers['Content-Disposition'] = 'inline'
    return resp


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    before_request()
    return render_template('user.html', user=user)

