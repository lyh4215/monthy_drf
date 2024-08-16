from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class PandaticNudge(BaseModel):
    date: datetime = Field(description="when to do")
    title: str = Field(description="title of the nudge")
    page : str = Field(description="the action to be taken")
    iconItem: str = Field(description="icon item representing the nudge")

    def __str__(self):
        return f"{self.date} | {self.title} | {self.page}"
class PandaticNudgeList(BaseModel):
    nudges: List[PandaticNudge] = Field(description="the list of the nudge")

    def append(self, nudge: PandaticNudge):
        self.nudges.append(nudge)

    def __str__(self):
        return "\n".join([nudge.__str__() for nudge in self.nudges])
    
class PandaticPersona(BaseModel):
    persona: str = Field(description="persona")

class PandaticDepressionRate(BaseModel):
    depression_rate: float = Field(description="depression rate")