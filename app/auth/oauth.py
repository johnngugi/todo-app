from flask import session, request
from .. import oauth


twitter = oauth.remote_app('twitter',
                           # unless absolute urls are used to make requests, this will be added
                           # before all URLs.  This is also true for request_token_url and others.
                           base_url='https://api.twitter.com/1.1/',
                           # where flask should look for new request tokens
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           # where flask should exchange the token with the remote application
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
                           # they mostly work the same, but for sign on /authenticate is
                           # expected because this will give the user a slightly different
                           # user interface on the twitter side.
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           # the consumer keys from the twitter application registry.
                           consumer_key='SFKpn0AdoGBQYqZmHpTXs8AKb',
                           consumer_secret='odvu4rB0fyv4mXQ3XOpLnkksiKbajfX8oUZcvGXuI5gBU84l2T'
                           )
