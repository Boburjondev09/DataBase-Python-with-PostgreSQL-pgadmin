from sqlalchemy import Column, Integer, String, Text
from database import Base

class UserItem(Base):
    __tablename__ = "user_items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True, nullable=False)
    user_surname = Column(String, index=True, nullable=False)
    item_name = Column(String, index=True, nullable=False)
    item_description = Column(Text)
