from __future__ import annotations

from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .database import get_session, init_db
from .models import (
    GroceryCreate,
    GroceryItem,
    GroceryRead,
    Ingredient,
    IngredientCreate,
    IngredientRead,
    Message,
    MessageCreate,
    MessageRead,
    Post,
    PostCreate,
    PostRead,
    RecognitionResult,
    TodoCreate,
    TodoItem,
    TodoRead,
)

try:
    from .openai_client import encode_image, request_ingredient_list
except Exception:  # pragma: no cover - allow app to run without OpenAI
    encode_image = None
    request_ingredient_list = None

app = FastAPI(title="Home Nexus", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/messages", response_model=List[MessageRead])
def list_messages(session: Session = Depends(get_session)) -> List[MessageRead]:
    statement = select(Message).order_by(Message.created_at.desc())
    return list(session.exec(statement))


@app.post("/api/messages", response_model=MessageRead, status_code=201)
def create_message(payload: MessageCreate, session: Session = Depends(get_session)) -> MessageRead:
    message = Message.from_orm(payload)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@app.delete("/api/messages/{message_id}", status_code=204)
def delete_message(message_id: int, session: Session = Depends(get_session)) -> None:
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    session.delete(message)
    session.commit()


@app.get("/api/posts", response_model=List[PostRead])
def list_posts(session: Session = Depends(get_session)) -> List[PostRead]:
    statement = select(Post).order_by(Post.created_at.desc())
    return list(session.exec(statement))


@app.post("/api/posts", response_model=PostRead, status_code=201)
def create_post(payload: PostCreate, session: Session = Depends(get_session)) -> PostRead:
    post = Post.from_orm(payload)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@app.delete("/api/posts/{post_id}", status_code=204)
def delete_post(post_id: int, session: Session = Depends(get_session)) -> None:
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()


@app.get("/api/todos", response_model=List[TodoRead])
def list_todos(session: Session = Depends(get_session)) -> List[TodoRead]:
    statement = select(TodoItem).order_by(TodoItem.created_at.desc())
    return list(session.exec(statement))


@app.post("/api/todos", response_model=TodoRead, status_code=201)
def create_todo(payload: TodoCreate, session: Session = Depends(get_session)) -> TodoRead:
    todo = TodoItem(description=payload.description)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.patch("/api/todos/{todo_id}", response_model=TodoRead)
def toggle_todo(todo_id: int, session: Session = Depends(get_session)) -> TodoRead:
    todo = session.get(TodoItem, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo.completed = not todo.completed
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, session: Session = Depends(get_session)) -> None:
    todo = session.get(TodoItem, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    session.delete(todo)
    session.commit()


@app.get("/api/groceries", response_model=List[GroceryRead])
def list_groceries(session: Session = Depends(get_session)) -> List[GroceryRead]:
    statement = select(GroceryItem).order_by(GroceryItem.created_at.desc())
    return list(session.exec(statement))


@app.post("/api/groceries", response_model=GroceryRead, status_code=201)
def create_grocery(payload: GroceryCreate, session: Session = Depends(get_session)) -> GroceryRead:
    grocery = GroceryItem(name=payload.name, quantity=payload.quantity)
    session.add(grocery)
    session.commit()
    session.refresh(grocery)
    return grocery


@app.patch("/api/groceries/{grocery_id}", response_model=GroceryRead)
def toggle_grocery(grocery_id: int, session: Session = Depends(get_session)) -> GroceryRead:
    grocery = session.get(GroceryItem, grocery_id)
    if not grocery:
        raise HTTPException(status_code=404, detail="Grocery item not found")
    grocery.checked = not grocery.checked
    session.add(grocery)
    session.commit()
    session.refresh(grocery)
    return grocery


@app.delete("/api/groceries/{grocery_id}", status_code=204)
def delete_grocery(grocery_id: int, session: Session = Depends(get_session)) -> None:
    grocery = session.get(GroceryItem, grocery_id)
    if not grocery:
        raise HTTPException(status_code=404, detail="Grocery item not found")
    session.delete(grocery)
    session.commit()


@app.get("/api/pantry", response_model=List[IngredientRead])
def list_ingredients(session: Session = Depends(get_session)) -> List[IngredientRead]:
    statement = select(Ingredient).order_by(Ingredient.created_at.desc())
    return list(session.exec(statement))


@app.post("/api/pantry", response_model=IngredientRead, status_code=201)
def create_ingredient(payload: IngredientCreate, session: Session = Depends(get_session)) -> IngredientRead:
    ingredient = Ingredient.from_orm(payload)
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient


@app.delete("/api/pantry/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, session: Session = Depends(get_session)) -> None:
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ingredient)
    session.commit()


@app.post("/api/pantry/recognize", response_model=RecognitionResult)
async def recognize_ingredients(
    image: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> RecognitionResult:
    if encode_image is None or request_ingredient_list is None:
        raise HTTPException(
            status_code=500,
            detail="Vision recognition is not configured. Install the openai package and set OPENAI_API_KEY.",
        )

    file_bytes = await image.read()
    image_b64 = encode_image(file_bytes)
    result_dict = request_ingredient_list(image_b64)

    created_items: list[IngredientRead] = []
    for item in result_dict.get("items", []):
        name = item.get("name")
        if not name:
            continue
        ingredient = Ingredient(
            name=name,
            amount=item.get("amount", ""),
            location=item.get("location", ""),
        )
        session.add(ingredient)
        session.commit()
        session.refresh(ingredient)
        created_items.append(IngredientRead.from_orm(ingredient))

    return RecognitionResult(items=created_items, raw_text=result_dict.get("raw_text", ""))


app.mount("/", StaticFiles(directory="static", html=True), name="static")
