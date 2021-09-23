from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from . import main 
from flask_login import login_required, current_user
from .forms import UpdateProfile, GeneralForm, GeneralReviewForm, SaleForm, SaleReviewForm, SeductionForm, SeductionReviewForm, MusicForm, MusicReviewForm, ProjectForm, ProjectReviewForm, InterviewForm, InterviewReviewForm, AdvertisementForm, AdvertisementReviewForm
from .. import db
from sqlalchemy import func
from ..models import Pitch, User

@main.route('/')
def index():
    """
    View root page function that returns the index page and its data
    """
    pitch = Pitch.query.all()
    Interview = Pitch.query.filter_by(category='Interview').all()
    Advertisement = Pitch.query.filter_by(category='Advertisement').all()
    MusicForm = Pitch.query.filter_by(category='Music').all()
    Seduction = Pitch.query.filter_by(category='Seduction').all()
    General= Pitch.query.filter_by(category='General').all()
    Project= Pitch.query.filter_by(category='Project').all()
    ReviewAdvertisement=Pitch.query.filter_by(category='ReviewAdvertisement').all()
    ReviewGeneral = Pitch.query.filter_by(category=' ReviewGeneral').all()
    ReviewInterview = Pitch.query.filter_by(category='ReviewInterview').all()


    return render_template('index.html', pitch=pitch)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)













@main.route('/user/rating')
@login_required
def ratings():
    upvote = Upvote(user=current_user)
    upvote.save_upvote()
    votes = db.session.query(func.sum(Upvote.upvote)).scalar()
    votes = str(votes)
    return votes


@main.route('/user/rating')
@login_required
def rating():
    downvote = Downvote(user=current_user)
    downvote.save_downvote()
    votes = db.session.query(func.sum(Downvote.downvote)).scalar()
    votes = str(votes)
    return votes


