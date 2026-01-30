from pydantic import BaseModel
from typing import Optional
from datetime import date

class GitHubTokenRequest(BaseModel):
    token: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
