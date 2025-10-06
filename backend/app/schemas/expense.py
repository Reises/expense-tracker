from pydantic import BaseModel, Field
from datetime import datetime

# ==================================================
# スキーマ定義
# ==================================================
# 登録・更新で使用するスキーマ
class InsertAndUpdateExpenseSchema(BaseModel):
    # 金額。このフィールドは必須です。
    amount: int = Field(...,
            description="金額を入力してください。少なくとも1円以上必要です。",
            example=1)
    date: datetime = Field(...,
            description="日付を入力してください。",
            example="YYYY/MM/DD")
    type: str = Field(...,
            description="収支を選択してください。",
            example="expense")
    category: str = Field(...,
            description="カテゴリを選択してください。",
            example="その他")

# 収支情報を表すスキーマ
class ExpenseSchema(InsertAndUpdateExpenseSchema):
    # 収支の一意識別子。データベースでユニークな主キーとして使用されます。
    expense_id: int = Field(...,
            description="収支を一意に識別するID番号。",
            example=123)

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    # 処理結果のメッセージ。このフィールドは必須です。
    message: str = Field(...,
        description="API操作の結果を説明するメッセージ。",
        example="情報更新に成功しました。")