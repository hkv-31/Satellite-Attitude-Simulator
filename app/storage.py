import os

_db = None

def _get_db():
    global _db
    if _db is not None:
        return _db

    # Firestore is optional locally. If credentials are not available,
    # simulations still work and the API returns storage_status="disabled".
    try:
        from google.cloud import firestore
        _db = firestore.Client()
        return _db
    except Exception:
        return None

def save_simulation(result):
    db = _get_db()
    if db is None:
        return None

    collection = os.getenv("FIRESTORE_COLLECTION", "simulations")
    ref = db.collection(collection).document()
    ref.set(result)
    return ref.id
