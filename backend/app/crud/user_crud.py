from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(
    *, session: Session, db_user: User, user_in: UserUpdate | dict[str, Any]
) -> User:
    user_data = (
        user_in.model_dump(exclude_unset=True)
        if isinstance(user_in, UserUpdate)
        else user_in
    )
    extra_data = {}
    if "password" in user_data:
        password = user_data.pop("password")
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password

    for key, value in user_data.items():
        setattr(db_user, key, value)

    for key, value in extra_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def delete_user(*, session: Session, user_id: int) -> None:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
