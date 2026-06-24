from ai import generate_summary
from ai import generate_tomorrow_plan

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import User, Task
from schemas import UserCreate, UserLogin, TaskCreate
from auth import hash_password, verify_password, create_access_token

app = FastAPI()

# Create Tables
Base.metadata.create_all(bind=engine)


# Database Session
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Home Route
@app.get("/")
def home():

    return {
        "message": "API Working"
    }


# Test Route
@app.get("/test")
def test():

    return {
        "message": "Working"
    }


# Register
@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }


# Login
@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=400,
            detail="Invalid username"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Create Task
@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    new_task = Task(
        title=task.title,
        completed=False,
        user_id=1
    )

    db.add(new_task)
    db.commit()

    return {
        "message": "Task created"
    }


# Get Tasks
@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).all()

    return tasks


# Complete Task
@app.put("/tasks/{task_id}")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.completed = True

    db.commit()

    return {
        "message": "Task completed"
    }


# AI Summary
@app.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).all()

    task_list = []

    for task in tasks:

        status = (
            "Completed"
            if task.completed
            else "Pending"
        )

        task_list.append(
            f"{task.title} - {status}"
        )

    summary = generate_summary(task_list)

    return {
        "summary": summary
    }

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted"
    }

# Tomorrow Plan
@app.get("/tomorrow-plan")
def tomorrow_plan(
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).all()

    task_list = [
        task.title
        for task in tasks
    ]

    plan = generate_tomorrow_plan(
        task_list
    )

    return {
        "plan": plan
    }