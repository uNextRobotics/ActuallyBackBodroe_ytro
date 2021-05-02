from pydantic import BaseModel


class User(BaseModel):
    UserId: str
    SberId: int
    Name: str
    Age: int
    Gender: str
    Active: int


class Progres(BaseModel):
    UserId: str
    Date: str
    Completed: bool


class Categoriya(BaseModel):
    Name: str
