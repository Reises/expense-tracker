from sqlalchemy import Column, Integer, String, DateTime
from ..db import Base #フォルダの階層が深いとその手前がモジュールになるため、相対パス指定する必要がある
from datetime import datetime

# ==================================
# モデル
# ==================================
# expenseテーブル用：モデル
class Expense(Base):
    # テーブル名
    __tablename__ = "expense"
    # id
    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    # 金額(未入力不可)
    amount = Column(Integer, nullable=False)
    # 日付
    date = Column(String(255))
    # 種類
    type = Column(String(20))
    # カテゴリ
    category = Column(String(20))