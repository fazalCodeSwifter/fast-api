from pydantic import BaseModel

# Dependency Inversion & Single Responsibility
class BaseAbstractModel(BaseModel):
    title: str
    description: str | None = None
    price: float

class ItemCreate(BaseAbstractModel):
    pass # Data coming from user

class Item(BaseAbstractModel):
    id: int # Data going to user (with ID)