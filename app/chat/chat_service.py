def create_chat_session():
    return []


def add_message(history, user_message, assistant_message):
    history.append(
        {
            "user": user_message,
            "assistant": assistant_message
        }
    )

    return history


def format_chat_history(history):
    if not history:
        return "No previous conversation."

    lines = []

    for message in history:
        lines.append(f"User: {message['user']}")
        lines.append(f"Assistant: {message['assistant']}")

    return "\n".join(lines)