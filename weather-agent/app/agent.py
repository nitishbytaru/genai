import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

from app.weather import get_weather

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

MODEL = os.environ["GEMINI_MODEL"]

chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(        
    system_instruction=(
        "You are a friendly current-weather assistant. "
        "Use the get_weather tool whenever the user asks about current weather. "
        "Never invent weather data. Use only the tool results. "
        "If the location is ambiguous, ask the user to clarify. "
        "You support current weather only, not forecasts. "
        "For unrelated questions, respond conversationally. "
        "you should only respond for the weather related questions only for any other questions just say sorry i can provide this data "

        "When presenting weather, follow this exact format:\n"
        "🌤️ Current Weather in [City, Country]\n\n"
        "🌡️ Temperature: [temperature]°C\n"
        "🤗 Feels Like: [feels-like temperature]°C\n"
        "☁️ Condition: [condition]\n"
        "💧 Humidity: [humidity]%\n"
        "💨 Wind Speed: [wind speed] km/h\n\n"
        "🕒 Observed at: [local observation time]\n\n"

        "Replace every placeholder with the actual tool result. "
        "Use the location and observation time returned by the tool. "
        "Keep the response concise and easy to read. "
        "Do not add unnecessary notes or repeat the weather information."
        ),
        tools=[get_weather],
    )
)

def chat_with_agent(message:str) -> str:
    response = chat.send_message(message)
    return response.text or "I couldn't generate response"
