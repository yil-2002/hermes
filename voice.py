import os
import asyncio
import base64
import tempfile
import edge_tts
from loguru import logger
import aiohttp

# J.A.R.V.I.S. uchun standart ovoz (Formal British Male)
DEFAULT_VOICE = os.getenv("HERMES_TTS_VOICE", "en-GB-ThomasNeural")

async def generate_speech(text: str, voice: str = DEFAULT_VOICE) -> str:
    """
    Matnni edge-tts orqali asinxron ravishda MP3 faylga o'giradi.
    API kalit talab qilinmaydi.
    """
    try:
        # Fayl nomini generatsiya qilish
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file.close()
        
        logger.info(f"Generating TTS with voice: {voice}")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_file.name)
        
        return temp_file.name
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        return ""

async def transcribe_audio(audio_bytes: bytes, gemini_api_key: str) -> str:
    """
    OGG audio faylini base64 orqali Gemini'ga yuborib matnga o'giradi.
    Qo'shimcha Whisper API talab qilinmaydi.
    """
    if not gemini_api_key:
        logger.warning("GEMINI_API_KEY topilmadi. STT o'tkazib yuborildi.")
        return ""

    try:
        encoded_audio = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Gemini API orqali transkripsiya qilish (Omni Router arxitekturasi asosida)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Transcribe the following audio exactly as spoken in the original language. Only return the transcribed text, nothing else."},
                    {"inline_data": {
                        "mime_type": "audio/ogg",
                        "data": encoded_audio
                    }}
                ]
            }]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                result = await resp.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                return ""
    except Exception as e:
        logger.error(f"STT Error: {e}")
        return ""
