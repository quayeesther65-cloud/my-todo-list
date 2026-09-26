
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


app = FastAPI()


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


def get_connection():
    connection = sqlite3.connect("todos.db")
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    cursor = connection.execute("SELECT COUNT(*) AS count FROM todos")
    count = cursor.fetchone()["count"]

    if count == 0:
        todos = [
            (
                "Complete Python Assignment",
                "Finish the Python exercises and submit them on time.",
                1
            ),
            (
                "Study Mathematics",
                "Review sequences, series and integration.",
                0
            ),
            (
                "Work on DataBloom Project",
                "Continue working on the group disease detection project.",
                0
            ),
            (
                "Read Economics Notes",
                "Review important economics concepts from class.",
                1
            ),
            (
                "Practice Data Analysis",
                "Practice Python and data analysis skills.",
                0
            )
        ]

        connection.executemany(
            """
            INSERT INTO todos (title, description, completed)
            VALUES (?, ?, ?)
            """,
            todos
        )

    connection.commit()
    connection.close()


@app.get("/")
def home():
    return {"message": "Todo API is running"}


@app.get("/todos", response_model=list[Todo])
def get_todos():
    connection = get_connection()

    cursor = connection.execute("SELECT * FROM todos")
    rows = cursor.fetchall()

    connection.close()

    todos_list = [
        Todo(**dict(row))
        for row in rows
    ]

    return todos_list


initialize_database()
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO todos (title, description, completed)
        VALUES (?, ?, 0)
        """,
        (todo.title, todo.description)
    )

    todo.id = cursor.lastrowid
    connection.commit()
    connection.close()

    return todo(id=todo.id, title=todo.title, description=todo.description, completed=False)

@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    connection = get_connection()

    connection.execute(
        """
        UPDATE todos
        SET title = ?, description = ?, completed = ?
        WHERE id = ?
        """,
        (todo.title, todo.description, int(todo.completed), todo_id)
    )

    connection.commit()
    connection.close()

    return todo(id=todo_id, title=todo.title, description=todo.description, completed=todo.completed)