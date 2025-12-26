from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column


class IDIntMixin:
    """Миксина для автоинкрементного целочисленного ID."""

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )


class TimestampMixin:
    """Миксина для timestamps"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class DisabledMixin:
    """Миксина для поля disable"""

    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class TimestampDisabledMixin(TimestampMixin, DisabledMixin):
    pass
