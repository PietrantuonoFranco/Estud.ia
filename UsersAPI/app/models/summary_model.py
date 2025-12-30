from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Summary(Base):
    __tablename__ = "summary"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    notebook_id = Column(Integer, ForeignKey("notebook.id"), nullable=False)
    notebook_users_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    notebook = relationship("Notebook", back_populates="summaries")
    user = relationship("User")
