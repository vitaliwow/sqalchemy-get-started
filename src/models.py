import enum
from datetime import datetime
from typing import Annotated

from sqlalchemy import Column, Integer, String, Table, MetaData, ForeignKey, func, text, Enum, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class WorkerORM(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]


class WorkloadORM(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumeORM(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    worker_id: Mapped[int]
    title: Mapped[str]
    compensation: Mapped[int | None]
    workload: Mapped[WorkloadORM]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('UTC', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('UTC', now())"),
        onupdate=datetime.utcnow,
    )


metadata = MetaData()

workers = Table(
    "workers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String)
)

resumes_table = Table(
    "resumes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(256)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(WorkloadORM)),
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column("updated_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow),
)
