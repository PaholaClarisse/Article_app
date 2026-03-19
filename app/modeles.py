from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Classe Utilisateur (La base)
class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable = False)
    content = Column(Text, nullable = False)
    author = Column(String(100), unique=True, index=True)
    category = Column(String(50), nullable = True)
    tags = Column(String(200), nullable = True) 
    created_at = Column(DateTime(timezone=True), server_default =func.now())