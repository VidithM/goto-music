import os
import pyrebase

FB_CONFIG = {
    'apiKey': "AIzaSyDjfdc64v44B1fecsZSc_TBj4sJPzaCi-g",
    'authDomain': "goto-music-c98e1.firebaseapp.com",
    'databaseURL': "https://goto-music-c98e1-default-rtdb.firebaseio.com/",
    'projectId': "goto-music-c98e1",
    'storageBucket': "goto-music-c98e1.appspot.com",
    'messagingSenderId': "902734405248",
    'appId': "1:902734405248:web:8e815e60bd1694cb335065"
}

AUTH = {
    'email' : os.environ['GOTO_MUSIC_EMAIL'],
    'password' : os.environ['GOTO_MUSIC_PASS']
}

def push(id, start):
    firebase = pyrebase.initialize_app(FB_CONFIG)
    db = firebase.database()

    auth = firebase.auth()
    token = auth.sign_in_with_email_and_password(AUTH['email'], AUTH['password'])['idToken']

    curr = db.child('songs').get().val()
    curr[id] = start
    db.child('songs').set(curr, token)
