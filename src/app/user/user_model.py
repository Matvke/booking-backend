from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.mixins.orm_mixins import IDIntMixin, TimestampDisabledMixin


class User(Base, IDIntMixin, TimestampDisabledMixin):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(
        String(),
        nullable=True,
    )
