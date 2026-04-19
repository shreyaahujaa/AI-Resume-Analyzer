from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile

from utils import (
    extract_text,
    extract_keywords,
    extract_skills,
    score_resume,
    get_ai_feedback
)

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # Save file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            file_path = tmp.name

        # Extract text
        text = extract_text(file_path)

        
        print("TEXT:", text[:500])

        if not text:
            return {"error": "No text found in resume"}

        # Extract data
        skills = extract_skills(text)
        keywords = extract_keywords(text)
        score = score_resume(skills)
        feedback = get_ai_feedback(text)

        return {
            "score": score,
            "skills": skills,
            "keywords": keywords[:20],
            "feedback": feedback
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": "Something went wrong"}