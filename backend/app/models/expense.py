from sqlalchemy import Column, Integer, String
from app.db import Base

class Expense(Base):
    """支出データモデル"""
    __tablename__ = "expense"

    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    date = Column(String(255))
    type = Column(String(20))
    category = Column(String(20))
