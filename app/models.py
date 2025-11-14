from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampedModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class MessageBase(SQLModel):
    author: str = Field(min_length=1, max_length=100, nullable=False)
    content: str = Field(min_length=1, max_length=2000, nullable=False)


class Message(MessageBase, TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    created_at: datetime


class PostBase(SQLModel):
    title: str = Field(min_length=1, max_length=150, nullable=False)
    body: str = Field(min_length=1, max_length=5000, nullable=False)


class Post(PostBase, TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    created_at: datetime


class TodoBase(SQLModel):
    description: str = Field(min_length=1, max_length=1000, nullable=False)
    completed: bool = Field(default=False)


class TodoItem(TodoBase, TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TodoCreate(SQLModel):
    description: str


class TodoRead(TodoBase):
    id: int
    created_at: datetime


class GroceryBase(SQLModel):
    name: str = Field(min_length=1, max_length=200, nullable=False)
    quantity: str = Field(default="1", max_length=100)
    checked: bool = Field(default=False)


class GroceryItem(GroceryBase, TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class GroceryCreate(SQLModel):
    name: str
    quantity: str = "1"


class GroceryRead(GroceryBase):
    id: int
    created_at: datetime


class IngredientBase(SQLModel):
    name: str = Field(min_length=1, max_length=200, nullable=False)
    amount: str = Field(default="", max_length=200)
    location: str = Field(default="", max_length=200)


class Ingredient(IngredientBase, TimestampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class IngredientCreate(SQLModel):
    name: str
    amount: str = ""
    location: str = ""


class IngredientRead(IngredientBase):
    id: int
    created_at: datetime


class RecognitionResult(SQLModel):
    items: list[IngredientRead]
    raw_text: str
