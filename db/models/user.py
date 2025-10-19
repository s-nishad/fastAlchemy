from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from db.models.base import BaseAbstractModel

__all__ = ['User']


class User(BaseAbstractModel):
    __tablename__ = "user_user_table"
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), )
    email: Mapped[str] = mapped_column(String(255), )
    password: Mapped[str] = mapped_column(String(255), )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'<User {self.id}>'
