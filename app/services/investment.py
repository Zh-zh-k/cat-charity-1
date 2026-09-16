from datetime import datetime

from app.models.base import InvestmentBase


def close_invested_object(obj: InvestmentBase) -> None:
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


def invest(
    target: InvestmentBase,
    sources: list[InvestmentBase],
) -> InvestmentBase:
    for source in sources:
        target_free = target.full_amount - target.invested_amount
        source_free = source.full_amount - source.invested_amount

        amount = min(target_free, source_free)

        target.invested_amount += amount
        source.invested_amount += amount

        close_invested_object(source)
        close_invested_object(target)

        if target.fully_invested:
            break

    return target
