from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1000), nullable=False)
    url = Column(String(1000), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    searchkeyword = Column(Text, nullable=False)
    platform = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    keywords = relationship("Keyword", back_populates="post", cascade="all, delete")
    summary = relationship("Summary", back_populates="post", uselist=False, cascade="all, delete")
    template = relationship("Template", back_populates="post", uselist=False, cascade="all, delete")
