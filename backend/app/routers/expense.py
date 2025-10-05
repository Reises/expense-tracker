from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.expense import InsertAndUpdateExpenseSchema, ExpenseSchema, ResponseSchema
import app.cruds.expense as expense_crud
import app.db as db

# ルーターを作成し、タグとURLパスのプレフィックスを設定
router = APIRouter(tags=["expenses"], prefix="/expenses")

# ==================================================
# メモ用のエンドポイント
# ==================================================
# メモ新規登録のエンドポイント
@router.post("/", response_model=ResponseSchema)
async def create_expense(expense: InsertAndUpdateExpenseSchema,
                    db: AsyncSession = Depends(db.get_dbsession)):
    try:
        # 新しいメモをデータベースに登録
        await expense_crud.insert_expense(db, expense)
        return ResponseSchema(message="メモが正常に登録されました")
    except Exception as e:
        # 登録に失敗した場合、HTTP 400エラーを返す
        raise HTTPException(status_code=400, detail="メモの登録に失敗しました。")

# メモ情報全件取得のエンドポイント
@router.get("/", response_model=list[ExpenseSchema])
async def get_expenses_list(db: AsyncSession = Depends(db.get_dbsession)):
    # 全てのメモをデータベースから取得
    expenses = await expense_crud.get_expenses(db)
    return expenses

# 特定のメモ情報取得のエンドポイント
@router.get("/{expense_id}", response_model=ExpenseSchema)
async def get_expense_detail(expense_id: int,
                    db: AsyncSession = Depends(db.get_dbsession)):
    # 指定されたIDのメモをデータベースから取得
    expense = await expense_crud.get_expense_by_id(db, expense_id)
    if not expense:
        # メモが見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="メモが見つかりません")
    return expense

# 特定のメモを更新するエンドポイント
@router.put("/{expense_id}", response_model=ResponseSchema)
async def modify_expense(expense_id: int, expense: InsertAndUpdateExpenseSchema,
                    db: AsyncSession = Depends(db.get_dbsession)):
    # 指定されたIDのメモを新しいデータで更新
    updated_expense = await expense_crud.update_expense(db, expense_id, expense)
    if not updated_expense:
        # 更新対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="更新対象が見つかりません")
    return ResponseSchema(message="メモが正常に更新されました")

# 特定のメモを削除するエンドポイント
@router.delete("/{expense_id}", response_model=ResponseSchema)
async def remove_expense(expense_id: int,
                    db: AsyncSession = Depends(db.get_dbsession)):
    # 指定されたIDのメモをデータベースから削除
    result = await expense_crud.delete_expense(db, expense_id)
    if not result:
        # 削除対象が見つからない場合、HTTP 404エラーを返す
        raise HTTPException(status_code=404, detail="削除対象が見つかりません")
    return ResponseSchema(message="メモが正常に削除されました")