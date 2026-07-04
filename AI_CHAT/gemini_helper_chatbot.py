import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def chat_with_gemini(chat_history):

    prompt = ""

    for message in chat_history:

        if message["role"] == "system":
            prompt += f"System:\n{message['content']}\n\n"

        elif message["role"] == "user":
            prompt += f"User:\n{message['content']}\n\n"

        elif message["role"] == "assistant":
            prompt += f"Assistant:\n{message['content']}\n\n"

    response = model.generate_content(prompt)

    return {
        "role": "assistant",
        "content": response.text
    }