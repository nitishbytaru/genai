
import os
import subprocess
import speech_recognition as sr

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

MODEL = os.environ["GEMINI_MODEL"]
TTS_MODEL = "gemini-3.8-flash-tts"


def generate_speech(text):
    print("\n" + "=" * 50)
    print("[TTS] Generating speech using Gemini...")
    print("=" * 50)

    response = client.models.generate_content(
        model=TTS_MODEL,
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            )
        )
    )

    # Extract generated audio
    audio_data = None

    for part in response.parts:
        if part.inline_data:
            audio_data = part.inline_data.data
            break

    if not audio_data:
        raise RuntimeError("Gemini did not return audio data.")

    # Save generated audio
    audio_file = "response.wav"

    with open(audio_file, "wb") as file:
        file.write(audio_data)

    print("[TTS] Speech generated successfully!")
    print(f"[TTS] Audio saved to {audio_file}")

    # Play audio
    print("[TTS] Playing assistant response...")

    subprocess.run(
        ["aplay", audio_file],
        check=True
    )

    print("[TTS] Audio playback completed!")


def main():
    r = sr.Recognizer()

    r.energy_threshold = 100
    r.dynamic_energy_threshold = False
    r.pause_threshold = 1

    try:
        with sr.Microphone(device_index=11) as source:

            print("\n" + "=" * 50)
            print("[MIC] Microphone opened successfully!")
            print("[MIC] Energy threshold:", r.energy_threshold)
            print("[MIC] Listening... Speak now!")
            print("=" * 50)

            audio = r.listen(
                source,
                timeout=10,
                phrase_time_limit=8
            )

            print("\n[STT] Processing audio...")

            stt = r.recognize_google(audio)

            print("[STT] Speech recognized successfully!")
            print(f"[USER] You said: {stt}")

            print("\n" + "=" * 50)
            print("[LLM] Initializing Gemini chat...")
            print("=" * 50)

            chat = client.chats.create(
                model=MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        """You are an expert voice agent assistant.
                        Respond naturally and conversationally,
                        as if speaking directly to the user.
                        Keep responses concise and easy to understand."""
                    )
                )
            )

            print("[LLM] Gemini chat initialized!")
            print(f"[LLM] Model: {MODEL}")

            print("\n[LLM] Sending user message to Gemini...")

            response = chat.send_message(stt)

            assistant_text = response.text

            print("[LLM] Response received successfully!")
            print(f"\n[ASSISTANT] {assistant_text}")

            # Convert Gemini response into speech
            generate_speech(assistant_text)

            print("\n" + "=" * 50)
            print("[SUCCESS] Voice agent processing completed!")
            print("=" * 50)

    except sr.WaitTimeoutError:
        print("[ERROR] No speech detected within 10 seconds.")

    except sr.UnknownValueError:
        print("[ERROR] Could not understand the audio.")

    except sr.RequestError as error:
        print("[STT ERROR]", error)

    except Exception as error:
        print("[ERROR]", error)


if __name__ == "__main__":
    main()
