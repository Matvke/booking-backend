import enum


class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROCESS = "in_process"
    COMPLETED = "completed"
    CANCELLED_BY_CLIENT = "cancelled_by_client"
    CANCELLED_BY_SPECIALIST = "cancelled_by_specialist"
    FAILED = "failed"

    @classmethod
    def get_display_name(cls, status: "SpecialistStatus") -> str:
        names = {
            cls.PENDING: "Ожидание",
            cls.CONFIRMED: "Подтверждено",
            cls.IN_PROCESS: "В процессе",
            cls.COMPLETED: "Завершено",
            cls.CANCELLED_BY_CLIENT: "Отменено клиентом",
            cls.CANCELLED_BY_SPECIALIST: "Отменено специалистом",
            cls.FAILED: "Ошибка",
        }
        return names[status]

    def is_final(self) -> bool:
        dict = {
            self.COMPLETED,
            self.FAILED,
            self.CANCELLED_BY_CLIENT,
            self.CANCELLED_BY_SPECIALIST,
        }
        return self in dict

    def can_be_updated(self) -> bool:
        return not self.is_final()


class SpecialistStatus(str, enum.Enum):
    ACTIVE = "active"
    ON_VACATION = "on_vacation"
    SICK_LEAVE = "sick_leave"
    INACTIVE = "inactive"

    @classmethod
    def get_display_name(cls, status: "SpecialistStatus") -> str:
        names = {
            cls.ACTIVE: "Активен",
            cls.ON_VACATION: "В отпуске",
            cls.SICK_LEAVE: "На больничном",
            cls.INACTIVE: "Неактивен",
        }
        return names[status]


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class UserRole(str, enum.Enum):
    USER = "user"
    SPECIALIST = "specialist"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    COMPANY_OWNER = "company_owner"

    @classmethod
    def get_display_name(cls, status: "SpecialistStatus") -> str:
        names = {
            cls.USER: "Пользователь",
            cls.SPECIALIST: "Специалист",
            cls.ADMIN: "Администратор",
            cls.SUPER_ADMIN: "Разработчик",
            cls.COMPANY_OWNER: "Владелец",
        }
        return names[status]
