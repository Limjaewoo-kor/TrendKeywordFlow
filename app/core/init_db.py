from .database import engine, Base
from ..models.blog_post import BlogPost
from ..models.keyword import Keyword
from ..models.summary import Summary
from ..models.template import Template

def init_db():
    Base.metadata.create_all(bind=engine)
