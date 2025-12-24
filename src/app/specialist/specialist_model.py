from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.enums import SpecialistStatus
from app.core.orm_mixins import IDIntMixin, TimestampDisabledMixin


class Specialist(Base, IDIntMixin, TimestampDisabledMixin):
    __tablename__ = "specialists"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    speciality: Mapped[str | None] = mapped_column(String(50), nullable=True)
    invoke_token: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    specialist_status: Mapped[SpecialistStatus] = mapped_column(
        SQLEnum(SpecialistStatus), default=SpecialistStatus.ACTIVE, nullable=False
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL")
    )
