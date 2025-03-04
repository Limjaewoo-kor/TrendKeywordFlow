from pydantic import BaseModel

class BlogPostRequest(BaseModel):
    title: str
    url: str
    content: str
    description: str
    searchKeyword: str
    platform: str
