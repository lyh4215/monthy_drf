from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Nudge(BaseModel):
    when: datetime = Field(description="when to do")
    title: str = Field(description="title of the nudge")
    to_do: str = Field(description="the action to be taken")

    def __str__(self):
        return f"{self.when} | {self.title} | {self.to_do}"
class NudgeList(BaseModel):
    nudges: List[Nudge] = Field(description="the list of the nudge")

    def append(self, nudge: Nudge):
        self.nudges.append(nudge)

    def __str__(self):
        return "\n".join([nudge.__str__() for nudge in self.nudges])