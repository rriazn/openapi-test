from sqlmodel import SQLModel, Session, create_engine
from config import get_settings


def _load_models() -> None:
    # Register SQLModel tables in metadata before create_all/drop_all.
    import models  # noqa: F401


def get_engine():
    return create_engine(get_settings().database_url)


def get_session():
    engine = get_engine()
    return Session(engine)


def get_db():
    return get_session()


def delete_db():
    _load_models()
    engine = get_engine()
    SQLModel.metadata.drop_all(bind=engine)


def create_db():
    _load_models()
    engine = get_engine()
    SQLModel.metadata.create_all(bind=engine)


def reset_db():
    _load_models()
    engine = get_engine()
    SQLModel.metadata.drop_all(bind=engine)
    create_db()