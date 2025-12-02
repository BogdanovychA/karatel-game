# -*- coding: utf-8 -*-

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./karatel/storage/karatel-game-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
