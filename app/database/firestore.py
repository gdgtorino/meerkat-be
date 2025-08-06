import os

import firebase_admin
from firebase_admin import firestore, credentials

from app.config.env import get_env


def init_firestore_client_service_account() :
    if firebase_admin._apps:
        return firestore.client()
    else:
        # Use a service account.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        firestore_credential = os.path.join(current_dir, "../config/resource", get_env()["firestore.path_credential_file"])
        cred = credentials.Certificate(firestore_credential)
        firebase_admin.initialize_app(cred)


def get_firestore_client():
    '''
    This method return a firestore client.
    '''
    return firestore.client()
