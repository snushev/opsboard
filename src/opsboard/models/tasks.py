from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.opsboard.core.base import Base
from src.opsboard.core.enums import TaskPriority, TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.TODO,
    )

    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM,
    )

    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    project: Mapped["Project"] = relationship(
        back_populates="tasks",
    )

    assignee: Mapped["User | None"] = relationship(
        back_populates="assigned_tasks",
        foreign_keys=[assignee_id],
    )

    creator: Mapped["User"] = relationship(
        back_populates="created_tasks",
        foreign_keys=[creator_id],
    )
