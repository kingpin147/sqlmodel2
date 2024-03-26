from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine, select, Field 
from contextlib import asynccontextmanager
from typing import Optional
from sqlmodel2 import settings  # Importing database settings


# Define the model for the Task table
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True)


# Construct the connection string with the appropriate driver
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg2"
)

# Create the database engine
engine = create_engine(connection_string)


# Function to create the database and its tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Define an async context manager for application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    create_db_and_tables()
    yield
    

# Create the FastAPI app with the defined lifespan
app = FastAPI(lifespan=lifespan)


# Endpoint to create a new task
@app.post("/task/")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


# Endpoint to update an existing task
@app.put("/task/")
def update_tasks(task: Task):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task.id)
        results = session.exec(statement)
        db_task = results.one()

        db_task.content = task.content
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


# Endpoint to delete a task
@app.delete("/task/")
def delete_tasks(task: Task):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task.id)
        results = session.exec(statement)
        db_task = results.one()
        session.delete(db_task)
        session.commit()
        return "task deleted....."


# Endpoint to retrieve all tasks
@app.get("/task/")
def read_task():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks
