from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Data format
class Note(BaseModel):
    content: str


# Home
@app.get("/")
def home():
    return {"message": "Notebook backend is working!"}


# Get all notes
@app.get("/notes")
def get_notes():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM notes")

    result = cursor.fetchall()

    cursor.close()

    return result


# Add a note
@app.post("/notes")
def add_note(note: Note):

    cursor = db.cursor()

    query = "INSERT INTO notes (content) VALUES (%s)"

    cursor.execute(query, (note.content,))

    db.commit()

    cursor.close()

    return {"message": "Note added successfully!"}


# Delete a note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):

    cursor = db.cursor()

    query = "DELETE FROM notes WHERE id = %s"

    cursor.execute(query, (note_id,))

    db.commit()

    cursor.close()

    return {"message": "Note deleted successfully!"}


# Update a note
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):

    cursor = db.cursor()

    query = "UPDATE notes SET content = %s WHERE id = %s"

    cursor.execute(query, (note.content, note_id))

    db.commit()

    cursor.close()

    return {"message": "Note updated successfully!"}