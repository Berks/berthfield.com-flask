import os
from firebase_admin import credentials, firestore, initialize_app

# Initialize DB
if os.getenv('GAE_ENV', '').startswith('standard'):
    # production
    default_app = initialize_app(credential=credentials.ApplicationDefault())
else:
    # localhost
    cred = credentials.Certificate("../../key.json")
    initialize_app(cred)


def get_db():
    # config database
    if os.getenv('GAE_ENV', '').startswith('standard'):
        # production
        db = firestore.client()
    else:
        # localhost
        if os.getenv('TESTING', '').startswith('yes'):
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8002"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8002/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8002"
        else:
            os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8081"
            os.environ["FIRESTORE_EMULATOR_HOST_PATH"] = "localhost:8081/firestore"
            os.environ["FIRESTORE_HOST"] = "http://localhost:8081"
        db = firestore.client()

    return db
