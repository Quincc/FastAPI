# shorturl_app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import random
import string

app = FastAPI()

# Модель для входных данных
class URLRequest(BaseModel):
    url: str

# Инициализация базы данных
def init_db():
    with sqlite3.connect("shorturl.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                short_id TEXT PRIMARY KEY,
                full_url TEXT NOT NULL,
                visits INTEGER DEFAULT 0
            )
        """)
        conn.commit()

init_db()

# Генерация короткого идентификатора
def generate_short_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_id = generate_short_id()
    with sqlite3.connect("shorturl.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (short_id, full_url) VALUES (?, ?)", (short_id, request.url))
        conn.commit()
        return {"short_id": short_id, "url": request.url}

@app.get("/{short_id}")
def redirect(short_id: str):
    with sqlite3.connect("shorturl.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT full_url FROM urls WHERE short_id = ?", (short_id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="shorturl_app not found")
        cursor.execute("UPDATE urls SET visits = visits + 1 WHERE short_id = ?", (short_id,))
        conn.commit()
        return {"message": "Redirect to", "url": result[0]}

@app.get("/stats/{short_id}")
def stats(short_id: str):
    with sqlite3.connect("shorturl.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT full_url, visits FROM urls WHERE short_id = ?", (short_id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="shorturl_app not found")
        return {"full_url": result[0], "visits": result[1]}
