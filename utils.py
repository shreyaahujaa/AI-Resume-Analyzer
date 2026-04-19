import pdfplumber
import spacy
from groq import Groq

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Groq client
client = Groq(api_key="Groq_key")

# Extract text from PDF
def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        print("PDF ERROR:", e)

    return text


# Skills list
skills_list = [
    "python", "java", "c++", "sql", "html", "css",
    "javascript", "react", "node", "machine learning",
    "deep learning", "nlp", "data analysis", "excel",
    "tensorflow", "pandas", "numpy"
]

# Extract skills
def extract_skills(text):
    text = text.lower()
    found = []

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    return list(set(found))


# Extract keywords
def extract_keywords(text):
    doc = nlp(text)
    return list(set([
        token.text.lower()
        for token in doc
        if token.is_alpha and not token.is_stop
    ]))


# Score
def score_resume(skills):
    return min(len(skills) * 15, 100)


# AI Feedback (Groq)
def get_ai_feedback(text):
    try:
        prompt = f"""
Analyze this resume and give output in CLEAN FORMAT:

Use this structure:

### Strengths
- point 1
- point 2

### Weaknesses
- point 1
- point 2

### Suggestions
- point 1
- point 2

Resume:
{text[:1500]}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("GROQ ERROR:", e)
        return "AI feedback not available"