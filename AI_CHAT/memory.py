from AI_CHAT.prompts import MINDPULSE_PROMPT

messages = []


# def initialize_memory():

#     global messages

#     if len(messages) == 0:

#         messages.append(
#             {
#                 "role":"system",
#                 "content":MINDPULSE_PROMPT
#             }
#         )
messages = []


def initialize_memory(system_prompt):

    global messages

    if len(messages) == 0:

        messages.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )

def add_user_message(user_message):

    global messages

    messages.append(
        {
            "role":"user",
            "content":user_message
        }
    )


def add_ai_message(ai_reply):

    global messages

    messages.append(ai_reply)


def get_chat_history():

    return messages