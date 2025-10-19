from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.models.base import BaseAbstractModel

__all__ = ['User', 'Document']


class User(BaseAbstractModel):
    __tablename__ = "user_user_table"

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # relation with document
    documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f'<User {self.id}>'


class Document(BaseAbstractModel):
    __tablename__ = "user_document_table"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_user_table.id"))

    user: Mapped["User"] = relationship("User", back_populates="documents")

    def __repr__(self) -> str:
        return f'<Document {self.id} Title="{self.title}">'
