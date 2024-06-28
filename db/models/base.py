from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, DateTime, func, MetaData
import datetime

from core.defaults import default_guid


class Base(DeclarativeBase):
    pass


class BaseAbstractModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    guid: Mapped[str] = mapped_column(String(32), default=default_guid, unique=True)

    created: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False, server_default=func.now())
    updated: Mapped[datetime.datetime] = mapped_column(DateTime(), nullable=False, server_default=func.now(),
                                                       onupdate=func.now())
