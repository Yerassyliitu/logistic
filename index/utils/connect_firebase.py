from os.path import abspath, join, dirname

import firebase_admin
from firebase_admin import credentials, firestore

config_full_path = abspath(join(dirname(__file__), "config.json"))
cred = credentials.Certificate(config_full_path)
firebase_admin.initialize_app(cred)


db = firestore.client()

# Путь к коллекции и документу
order_collection_path = "orders"
history_status_collection_path = "history_status"
default_user_reference = db.collection("users").document("109bGlPHtIhhjEjXCEXJHPUvdn42")
created_status_reference = db.collection("status").document("7yEPTlnhhimFdko4ROjS")
to_receiving_country = db.collection("status").document("qi2e8oKRn2XWKILfidbI")