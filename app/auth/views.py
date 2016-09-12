from flask import render_template, session, request, url_for, flash, redirect
from . import auth
from .oauth import twitter
from ..models import User
from .. import db


@twitter.tokengetter
def get_twitter_token(token=None):
    if session.has_key('twitter_oauth_tokens'):
        del session['twitter_oauth_tokens']
    return session.get('twitter_oauth_tokens')


@auth.route('/login')
def login():
    callback = url_for('auth.oauth_authorized',
                       next=request.args.get('next') or request.referrer or None,
                       _external=True)
    return twitter.authorize(callback=callback)


@auth.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('main.index'))


@auth.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('main.index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    social_id = resp['user_id']
    username = resp['screen_name']
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('main.index'))
