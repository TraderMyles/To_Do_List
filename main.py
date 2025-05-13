from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database"
todos = []

class Todo(BaseModel):
    title: str
    completed: bool = False

class TodoStatus(BaseModel):
    completed: bool

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def add_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo added", "todo": todo}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if 0 <= todo_id < len(todos):
        deleted = todos.pop(todo_id)
        return {"message": "Todo deleted", "todo": deleted}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}")
def update_todo_status(todo_id: int, status: TodoStatus):
    if 0 <= todo_id < len(todos):
        todos[todo_id].completed = status.completed
        return {
            "message": f"Todo marked as {'complete' if status.completed else 'incomplete'}",
            "todo": todos[todo_id]
        }
    raise HTTPException(status_code=404, detail="Todo not found")
