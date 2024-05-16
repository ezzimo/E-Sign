from sqlalchemy import create_engine
from sqlmodel import Session, select

from app.core.config import settings
from app.crud import user_crud
from app.models.models import User
from app.schemas.schemas import UserCreate

# Create the engine
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
)


def init_db(session: Session):
    # Ensure all models are imported and properly initialized
    # SQLModel.metadata.create_all(engine)  # Create all tables

    superuser_email = settings.FIRST_SUPERUSER

    user_query = select(User).where(User.email == superuser_email)
    user = session.exec(user_query).first()

    if not user:
        user_in = UserCreate(
            email=superuser_email,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            first_name=settings.FIRST_NAME,
            last_name=settings.LAST_NAME,
            role=settings.ROLE,
        )
        user = user_crud.create_user(session=session, user_create=user_in)
