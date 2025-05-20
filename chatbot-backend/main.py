from fastapi import FastAPI
from util.speech_to_text import speech_to_text_function


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "chatbot api"}

