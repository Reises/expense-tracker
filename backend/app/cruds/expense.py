from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.expense import InsertAndUpdateExpenseSchema
from app.models.expense import Expense
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# ==================================================
# CRUD処理
# ==================================================

async def insert_expense(
    db_session: AsyncSession,
    expense_data: InsertAndUpdateExpenseSchema
) -> Expense:
    """支出データを新規登録"""
    new_expense = Expense(**expense_data.model_dump())
    db_session.add(new_expense)
    await db_session.commit()
    await db_session.refresh(new_expense)
    logger.info("新規登録: expense_id=%s, category=%s", new_expense.expense_id, new_expense.category)
    return new_expense


async def get_expenses(db_session: AsyncSession) -> List[Expense]:
    """全件取得"""
    result = await db_session.execute(select(Expense))
    expenses = result.scalars().all()
    logger.info("全件取得: %d件", len(expenses))
    return expenses


async def get_expense_by_id(
    db_session: AsyncSession,
    expense_id: int
) -> Optional[Expense]:
    """ID指定で1件取得"""
    result = await db_session.execute(
        select(Expense).where(Expense.expense_id == expense_id)
    )
    expense = result.scalars().first()
    if expense:
        logger.debug("データ取得成功: expense_id=%s", expense_id)
    else:
        logger.debug("データ未検出: expense_id=%s", expense_id)
    return expense


async def update_expense(
    db_session: AsyncSession,
    expense_id: int,
    target_data: InsertAndUpdateExpenseSchema
) -> Optional[Expense]:
    """既存データを更新"""
    expense = await get_expense_by_id(db_session, expense_id)
    if not expense:
        logger.warning("更新失敗: expense_id=%s が存在しません", expense_id)
        return None

    for field, value in target_data.model_dump().items():
        setattr(expense, field, value)

    await db_session.commit()
    await db_session.refresh(expense)
    logger.info("更新完了: expense_id=%s", expense_id)
    return expense


async def delete_expense(
    db_session: AsyncSession,
    expense_id: int
) -> Optional[Expense]:
    """指定IDのデータを削除"""
    expense = await get_expense_by_id(db_session, expense_id)
    if not expense:
        logger.warning("削除失敗: expense_id=%s が存在しません", expense_id)
        return None

    await db_session.delete(expense)
    await db_session.commit()
    logger.info("削除完了: expense_id=%s", expense_id)
    return expense
