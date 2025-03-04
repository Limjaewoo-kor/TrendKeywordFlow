from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..core.database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    introduction = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    conclusion = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("blog_posts.id"))

    post = relationship("BlogPost", back_populates="template")
