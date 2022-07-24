from xmlrpc.client import Boolean
from pydantic import BaseModel, conlist, condecimal, constr, Field
from typing import Optional, List
from enum import Enum

class StagesEnum(str, Enum):
    pending = "Pending"
    reviewing = "Reviewing"
    shortlisted = "Shortlisted"
    interviewing = "Interviewing"
    advanced_interviewing = "Advanced Interviewing"
    rejected = "Rejected"
    offered = "Offered"
    hired = "Hired"

class CreateApplication(BaseModel):
    email: str

    class Config:
        orm_mode = True

class Application(BaseModel):
    jobid: str
    email: str
    stage: StagesEnum
    has_resume: bool
    actions: List[str]

    class Config:
        orm_mode = True

class ListApplications(BaseModel):
    count: int
    applications: List[Application]
    
    class Config:
        orm_mode = True
