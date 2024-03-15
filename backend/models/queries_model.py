from pydantic import BaseModel

class QueriesModel(BaseModel):
    persistent_cough: str
    labored_breathing: str 
    recent_fever: str
    chest_pain: str
    nasal_congestion: str 


class AnswersModel(BaseModel):
    response: str


