import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def get_ai_insights(prompt):

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return str(e)