from app.database.firestore import init_firestore_client_service_account


def init_app() -> None:
    init_firestore_client_service_account()
