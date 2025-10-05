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
    # メモの詳細説明。このフィールドは任意で入力可能です。
    # description: str = Field(default="",
    #         description="メモの内容についての追加情報。任意で記入できます。",
    #         example="会議で話すトピック：プロジェクトの進捗状況")

# メモ情報を表すスキーマ
class ExpenseSchema(InsertAndUpdateExpenseSchema):
    # メモの一意識別子。データベースでユニークな主キーとして使用されます。
    expense_id: datetime = Field(...,
            description="収支を一意に識別するID番号。",
            example=datetime.now())

# レスポンスで使用する結果用スキーマ
class ResponseSchema(BaseModel):
    # 処理結果のメッセージ。このフィールドは必須です。
    message: str = Field(...,
        description="API操作の結果を説明するメッセージ。",
        example="情報更新に成功しました。")