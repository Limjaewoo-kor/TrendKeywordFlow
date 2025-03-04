from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(100), nullable=False)
    post_id = Column(Integer, ForeignKey("blog_posts.id"))

    post = relationship("BlogPost", back_populates="keywords")
