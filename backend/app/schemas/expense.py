from pydantic import BaseModel, Field
from datetime import datetime

class InsertAndUpdateExpenseSchema(BaseModel):
    amount: int = Field(..., ge=1, description="金額を入力してください。")
    date: datetime = Field(..., description="日付を入力してください。")
    type: str = Field(..., description="収支タイプを指定してください（例: income / expense）")
    category: str = Field(..., description="カテゴリを指定してください。")


class ExpenseSchema(InsertAndUpdateExpenseSchema):
    expense_id: int = Field(..., description="収支を一意に識別するID番号。")


class ResponseSchema(BaseModel):
    message: str = Field(..., example="操作が成功しました。")
