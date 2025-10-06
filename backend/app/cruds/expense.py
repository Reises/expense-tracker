from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import app.schemas.expense as expense_schema
import app.models.expense as expense_model
from datetime import datetime

# ==================================================
# 非同期CRUD処理
# ==================================================
# 新規登録
async def insert_expense(
        db_session: AsyncSession,
        expense_data: expense_schema.InsertAndUpdateExpenseSchema) -> expense_model.Expense:
    """
        新しいメモをデータベースに登録する関数
        Args:
        db_session (AsyncSession): 非同期DBセッション
        expense_data (InsertAndUpdateExpenseSchema): 作成するメモのデータ
        Returns:
        Expense: 作成されたメモのモデル
    """
    print("=== 新規登録：開始 ===")
    #expense_dataを使って新しいオブジェクトを作成し、辞書形式に変換
    new_expense = expense_model.Expense(**expense_data.model_dump())
    # DBに追加
    db_session.add(new_expense)
    await db_session.commit()
    # DBから引数のオブジェクトに対応する最新データが取得され、そのオブジェクトの属性が更新される
    await db_session.refresh(new_expense)
    print(">>> データ追加完了")
    return new_expense

# 全件取得
async def get_expenses(db_session: AsyncSession) -> list[expense_model.Expense]:
    """
        データベースから全てのメモを取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
        Returns:
            list[Expense]: 取得された全てのメモのリスト
    """
    print("=== 全件取得：開始 ===")
    # DBからすべてのメモを選択するSQLクエリを実行
    result = await db_session.execute(select(expense_model.Expense))
    # クエリの結果をスカラー値として取得し、すべての結果をリストとして返す
    # scalars():クエリ結果の各行を個別のオブジェクトとして抽出
    expenses = result.scalars().all()
    print(">>> データ全件取得完了")
    return expenses

# 1件取得
async def get_expense_by_id(db_session: AsyncSession,
        expense_id: int) -> expense_model.Expense | None:
    """
        データベースから特定のメモを1件取得する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            expense_id (int): 取得するメモのID（プライマリキー）
        Returns:
            expense | None: 取得されたメモのモデル、メモが存在しない場合はNoneを返す
    """
    print("=== １件取得：開始 ===")
    result = await db_session.execute(
    select(expense_model.Expense).where(expense_model.Expense.expense_id == expense_id))
    expense = result.scalars().first()
    print(">>> データ取得完了")
    return expense

# 更新処理
async def update_expense(
        db_session: AsyncSession,
        expense_id: int,
        target_data: expense_schema.InsertAndUpdateExpenseSchema) -> expense_model.Expense | None:
    """
        データベースのメモを更新する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            expense_id (int): 更新するメモのID（プライマリキー）
            target_data (InsertAndUpdateexpenseSchema): 更新するデータ
        Returns:
            expense | None: 更新されたメモのモデル、メモが存在しない場合はNoneを返す
    """
    print("=== データ更新：開始 ===")
    expense = await get_expense_by_id(db_session, expense_id)
    if expense:
        expense.expense_id = target_data.expense_id
        expense.amount = target_data.amount
        expense.date = target_data.date
        expense.type = target_data.type
        expense.category = target_data.category
        await db_session.commit()
        await db_session.refresh(expense)
        print(">>> データ更新完了")
        
    return expense

# 削除処理
async def delete_expense(
        db_session: AsyncSession, expense_id: int
        ) -> expense_model.Expense | None:
    """
        データベースのメモを削除する関数
        Args:
            db_session (AsyncSession): 非同期DBセッション
            expense_id (int): 削除するメモのID（プライマリキー）
        Returns:
            expense | None: 削除されたメモのモデル、メモが存在しない場合はNoneを返す
    """
    print("=== データ削除：開始 ===")
    expense = await get_expense_by_id(db_session, expense_id)
    if expense:
        await db_session.delete(expense)
        await db_session.commit()
        print(">>> データ削除完了")
    
    return expense