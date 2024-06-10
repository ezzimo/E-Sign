import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.crud import user_crud
from app.models.models import Message
from app.models.models import User
from app.schemas.schemas import (
    UpdatePassword,
    UserCreate,
    UserCreateOpen,
    UserOut,
    UsersOut,
    UserUpdate,
    UserUpdateMe,
)
from app.utils import generate_new_account_email, send_email

# Create a logger for your application
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UsersOut
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    logger.info(f"Fetching users list with skip={skip} and limit={limit}")
    try:
        count_statement = select(func.count()).select_from(User)
        count = session.exec(count_statement).one()

        statement = select(User).offset(skip).limit(limit)
        user_models = session.exec(statement).all()

        users_out = [
            UserOut(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                full_name=user.full_name,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in user_models
        ]
        logger.info(f"Fetched {len(users_out)} users successfully.")
        return UsersOut(data=users_out, count=count)
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserOut
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    logger.info(f"Creating a new user with email: {user_in.email}")
    try:
        if user_crud.get_user_by_email(session=session, email=user_in.email):
            logger.warning(f"User with email {user_in.email} already exists.")
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        user = user_crud.create_user(session=session, user_create=user_in)
        if settings.emails_enabled and user_in.email:
            email_data = generate_new_account_email(
                email_to=user_in.email,
                username=user_in.email,
                password=user_in.password,
            )
            send_email(
                email_to=user_in.email,
                subject=email_data.subject,
                html_content=email_data.html_content,
            )
        logger.info(f"User with email {user_in.email} created successfully.")
        return user
    except HTTPException:
        raise
    except Exception as e:
        # Log detailed validation errors for debugging
        logger.error(f"Validation Error: {str({e.detail})}")
        # Optionally, return the detailed errors for client-side debugging
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/me", response_model=UserOut)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    logger.info(f"Updating user information for user {current_user.id}")
    try:
        if user_in.email:
            existing_user = user_crud.get_user_by_email(
                session=session, email=user_in.email
            )
            if existing_user and existing_user.id != current_user.id:
                logger.warning(
                    f"Email {user_in.email} is already in use by another user."
                )
                raise HTTPException(
                    status_code=409, detail="User with this email already exists"
                )
        user_data = user_in.dict(exclude_unset=True)
        user_crud.update_user(session=session, db_user=current_user, user_in=user_data)
        logger.info(f"User {current_user.id}'s information updated successfully.")
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    logger.info(f"Updating password for user {current_user.id}")
    try:
        if not verify_password(body.current_password, current_user.hashed_password):
            logger.warning("Incorrect current password provided.")
            raise HTTPException(status_code=400, detail="Incorrect password")
        if body.current_password == body.new_password:
            logger.warning("New password is the same as the current one.")
            raise HTTPException(
                status_code=400,
                detail="New password cannot be the same as the current one",
            )
        current_user.hashed_password = get_password_hash(body.new_password)
        session.add(current_user)
        session.commit()
        logger.info(f"Password for user {current_user.id} updated successfully.")
        return Message(message="Password updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating password for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get("/me", response_model=UserOut)
def read_user_me(*, session: SessionDep, current_user: CurrentUser) -> Any:
    logger.info(f"Fetching current user information for user {current_user.id}")
    # This function might not require a try-except as it's a simple retrieval,
    # but logging the action still provides valuable audit trail
    return current_user


@router.post("/open", response_model=UserOut)
def create_user_open(*, session: SessionDep, user_in: UserCreateOpen) -> Any:
    logger.info("Creating a new user from open registration.")
    try:
        if not settings.USERS_OPEN_REGISTRATION:
            logger.warning("Open user registration is disabled.")
            raise HTTPException(
                status_code=403,
                detail="Open user registration is forbidden on this server",
            )
        if user_crud.get_user_by_email(session=session, email=user_in.email):
            logger.warning(f"User with email {user_in.email} already exists.")
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system",
            )
        user = user_crud.create_user(session=session, user_create=user_in)
        logger.info(f"User {user.id} created successfully from open registration.")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during open user registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get("/{user_id}", response_model=UserOut)
def read_user_by_id(
    user_id: int, *, session: SessionDep, current_user: CurrentUser
) -> Any:
    logger.info(f"Fetching user information by ID {user_id}")
    try:
        user = session.get(User, user_id)
        if not user:
            logger.warning(f"User {user_id} not found.")
            raise HTTPException(status_code=404, detail="User not found")
        if user != current_user and not current_user.is_superuser:
            logger.warning(
                f"User {current_user.id} does not have privileges to access user {user_id}."
            )
            raise HTTPException(
                status_code=403, detail="The user doesn't have enough privileges"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserOut,
)
def update_user(*, session: SessionDep, user_id: int, user_in: UserUpdate) -> Any:
    logger.info(f"Updating user {user_id}")
    try:
        db_user = session.get(User, user_id)
        if not db_user:
            logger.warning(f"User {user_id} does not exist.")
            raise HTTPException(
                status_code=404,
                detail="The user with this id does not exist in the system",
            )
        user_crud.update_user(session=session, db_user=db_user, user_in=user_in)
        logger.info(f"User {user_id} updated successfully.")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.delete("/{user_id}")
def delete_user(
    *, session: SessionDep, current_user: CurrentUser, user_id: int
) -> Message:
    logger.info(f"Deleting user {user_id}")
    try:
        user = session.get(User, user_id)
        if not user:
            logger.warning(f"User {user_id} not found for deletion.")
            raise HTTPException(status_code=404, detail="User not found")
        if user == current_user and current_user.is_superuser:
            logger.warning("Superuser attempted self-deletion.")
            raise HTTPException(
                status_code=403,
                detail="Super users are not allowed to delete themselves",
            )
        user_crud.delete_user(session=session, user_id=user_id)
        logger.info(f"User {user_id} deleted successfully.")
        return Message(message="User deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
