from os.path import abspath, join, dirname

import firebase_admin
from firebase_admin import credentials, firestore

config_full_path = abspath(join(dirname(__file__), "config1.json"))
cred = credentials.Certificate(config_full_path)
firebase_admin.initialize_app(cred)


db = firestore.client()
