from pydantic import BaseModel
from typing import List

class TrendRequest(BaseModel):
    keywords: List[str]
