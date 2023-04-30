import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

#FireStore instance
cred = credentials.Certificate("./auth/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
new_db = firestore.client()