from AI_CHAT.memory import (
    initialize_memory,
    add_user_message,
    add_ai_message,
    get_chat_history
)

# from AI_CHAT.ollama_helper import chat_with_ollama
# used gemini instead ollama for deployment
from AI_CHAT.gemini_helper_chatbot import chat_with_gemini  




from AI_CHAT.prompts import MINDPULSE_PROMPT


def get_ai_reply(user_message,student_profile):
    # Initialize memory
    initialize_memory(MINDPULSE_PROMPT)
    # Add user message
    add_user_message(

    f"""

    Student Profile:

    {student_profile}

    ----------------------------

    Student Question:

    {user_message}

    """

    )

    # Get history
    history = get_chat_history()
    # Call Ollama and gets reply from llama through ollama
    # reply = chat_with_ollama(history)

    # change to gemini for deployment
    # if u change to gemini comment the above line and use this
    reply = chat_with_gemini(history)
    # Save AI reply
    add_ai_message(reply)
    # Return answer
    return reply["content"]




# -----------------------------------------------------------------------------------------
# from AI_CHAT.ollama_helper import chat_with_ollama
# from AI_CHAT.prompts import MINDPULSE_PROMPT
# # both are my own files

# def get_ai_reply(user_message):
#     messages = [
#     {
#         "role": "system",
#         "content": MINDPULSE_PROMPT
#     }
# ]
#     messages.append(
#     {
#         "role": "user",
#         "content": user_message
#     }
# )
#     reply = chat_with_ollama(messages)
#     # fetches reply from ollama helper file

#     return reply["content"]

# the above code works but it does not have memory of prev convo





