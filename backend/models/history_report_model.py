import datetime
from pydantic import BaseModel

class History(BaseModel):
    description: str
    date: datetime


class Report(BaseModel):
    report_token: str
    date: datetime


