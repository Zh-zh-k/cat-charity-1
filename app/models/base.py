from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class InvestmentBase(Base):
    __abstract__ = True

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive',
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_not_greater_than_full_amount',
        ),
    )

    full_amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested})'
        )
