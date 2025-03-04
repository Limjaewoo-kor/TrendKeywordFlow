from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..core.database import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False)
    summary_text = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("blog_posts.id"))

    post = relationship("BlogPost", back_populates="summary")
