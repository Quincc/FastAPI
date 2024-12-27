# todo_app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Модель задачи
class TodoItem(BaseModel):
    title: str
    description: str = None
    completed: bool = False

# Инициализация базы данных
def init_db():
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL
            )
        """)
        conn.commit()

init_db()

@app.post("/items", response_model=TodoItem)
def create_item(item: TodoItem):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
                       (item.title, item.description, item.completed))
        conn.commit()
        return item

@app.get("/items", response_model=List[TodoItem])
def get_items():
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, description, completed FROM todos")
        items = cursor.fetchall()
        return [{"title": title, "description": description, "completed": completed} for title, description, completed in items]

@app.get("/items/{item_id}", response_model=TodoItem)
def get_item(item_id: int):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, description, completed FROM todos WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"title": item[0], "description": item[1], "completed": item[2]}

@app.put("/items/{item_id}", response_model=TodoItem)
def update_item(item_id: int, item: TodoItem):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
                       (item.title, item.description, item.completed, item_id))
        conn.commit()
        return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with sqlite3.connect("todo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (item_id,))
        conn.commit()
        return {"message": "Item deleted"}
