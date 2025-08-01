from db import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    Priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Todo id={self.id} title={self.title} completed={self.completed}>"