from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.expense import InsertAndUpdateExpenseSchema, ExpenseSchema, ResponseSchema
from app.cruds import expense as expense_crud
from app.db import get_dbsession

router = APIRouter(tags=["expenses"], prefix="/expenses")

# ==================================================
# 支出エンドポイント
# ==================================================

@router.post("/", response_model=ExpenseSchema)
async def create_expense(
    expense: InsertAndUpdateExpenseSchema,
    db: AsyncSession = Depends(get_dbsession)
):
    created = await expense_crud.insert_expense(db, expense)
    return created


@router.get("/", response_model=list[ExpenseSchema])
async def list_expenses(db: AsyncSession = Depends(get_dbsession)):
    return await expense_crud.get_expenses(db)


@router.get("/{expense_id}", response_model=ExpenseSchema)
async def read_expense(expense_id: int, db: AsyncSession = Depends(get_dbsession)):
    expense = await expense_crud.get_expense_by_id(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="支出が見つかりません。")
    return expense


@router.put("/{expense_id}", response_model=ResponseSchema)
async def update_expense(
    expense_id: int,
    expense: InsertAndUpdateExpenseSchema,
    db: AsyncSession = Depends(get_dbsession)
):
    updated = await expense_crud.update_expense(db, expense_id, expense)
    if not updated:
        raise HTTPException(status_code=404, detail="更新対象が見つかりません。")
    return ResponseSchema(message="支出が正常に更新されました。")


@router.delete("/{expense_id}", response_model=ResponseSchema)
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_dbsession)):
    deleted = await expense_crud.delete_expense(db, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="削除対象が見つかりません。")
    return ResponseSchema(message="支出が正常に削除されました。")
