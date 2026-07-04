# reusable function
import ollama


def chat_with_ollama(chat_history, model="llama3.2:3b"):
    # this sec means that we r givin entire convo to llm so that it generates next reply
    response = ollama.chat(
        model=model,
        messages=chat_history
    )

    return response["message"]


# actual function of this file is:
# receives the conversation (chat_history) from chat_engine file
# sends it to Ollama
# Returns the AI's reply



'''chat_engine.py
     │
     │  "Here's the conversation"
     ▼
    ollama_helper.py
     │
     │  Sends it to Ollama
     ▼
    Ollama
     │
     │  "Here's the reply"
     ▼
    ollama_helper.py
     │
     │  Returns the reply
     ▼
    chat_engine.py'''

'''prompts.py
      │
      ▼
    Gets System Prompt

    memory.py
      │
      ▼
    Gets Chat History

    ollama_helper.py
      │
      ▼
    Gets AI Reply'''