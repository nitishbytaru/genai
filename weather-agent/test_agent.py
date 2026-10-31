
from app.agent import chat_with_agent

while True:
    message = input("\nYou: ").strip()

    if message.lower() in {"exit", "quit"}:
        break

    if not message:
        continue

    try:
        answer = chat_with_agent(message)
        print(f"\nWeather Agent: {answer}")
    except Exception as exc:
        print(f"\nError: {exc}")
