# voice.py
import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import os

# Initialize pygame mixer for audio playback
pygame.mixer.init()

async def _generate_and_play(text):
    """Internal async function to handle TTS and playback."""
    # We use a deep, authoritative male voice (en-US-ChristopherNeural)
    # You can change this to "en-GB-RyanNeural" for a British Zeus
    voice = "en-US-ChristopherNeural"
    output_file = "temp_voice.mp3"

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(output_file)
    except Exception as e:
        print(f"TTS Error: {e}")

def speak(text):
    """Converts text to speech using high-quality neural voices."""
    print(f"Zeus: {text}")
    try:
        # Run the async TTS function in a synchronous wrapper
        asyncio.run(_generate_and_play(text))
    except Exception as e:
        print(f"Voice Error: {e}")

def listen():
    """Hyper-sensitive listening for low-volume environments."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 30
    recognizer.pause_threshold = 0.6

    with sr.Microphone() as source:
        print("\nListening... 🎙️")
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
            print("Processing speech... ⚙️")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Listening Error: {e}")
            return None
