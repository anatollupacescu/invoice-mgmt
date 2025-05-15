from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from interpreter import Interpreter, InterpreterRepository

app = FastAPI()
repo = InterpreterRepository()

# Load interpreters from CSV on startup
try:
    repo.load_from_csv("interpreter.csv")
except Exception as e:
    print(f"Warning: Could not load interpreter.csv: {e}")

# Pydantic model for responses
class InterpreterResponse(BaseModel):
    id: int
    name: str
    language: str

@app.get("/interpreters", response_model=List[InterpreterResponse])
def list_interpreters():
    return [i.to_dict() for i in repo.list_all()]

@app.get("/interpreters/{id}", response_model=InterpreterResponse)
def get_interpreter(id: int):
    interpreter = repo.get(id)
    if interpreter:
        return interpreter.to_dict()
    raise HTTPException(status_code=404, detail="Interpreter not found")