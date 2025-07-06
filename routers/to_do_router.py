# routers/todo.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from models.database import SessionLocal
from models.todo import Todo
from schemas.to_do_schemas import TodoResponse,TodoCreate,TodoUpdate

to_do_router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@to_do_router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

""""
@to_do_router.get("/", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()
"""""
@to_do_router.get("/{id}", response_model=TodoResponse)
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@to_do_router.put("/{id}", response_model=TodoResponse)
def update_todo(id: int, updated_data: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo

@to_do_router.delete("/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
@to_do_router.get("/", response_model=List[TodoResponse])
def get_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    completed: Optional[bool] = Query(None, description="Filter todos by completion status"),
    title_contains: Optional[str] = Query(None, description="Filter todos containing this text in title"),
    db: Session = Depends(get_db),
):
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if title_contains:
        query = query.filter(Todo.title.ilike(f"%{title_contains}%"))

    todos = query.offset(skip).limit(limit).all()
    return todos
