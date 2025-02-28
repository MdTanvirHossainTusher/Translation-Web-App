"""
Translation and text-to-speech functionality for the Healthcare Translation Web App.
Uses Google's Gemini API for translation and edge-tts for text-to-speech.
"""
import os
import base64
import tempfile
import edge_tts
import asyncio
import google.generativeai as genai
from flask import current_app
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Map of language codes to edge-tts voices
LANGUAGE_TO_VOICE = {
    'en': 'en-US-ChristopherNeural',
    'es': 'es-ES-AlvaroNeural',
    'fr': 'fr-FR-HenriNeural',
    'de': 'de-DE-ConradNeural',
    'it': 'it-IT-DiegoNeural',
    'pt': 'pt-BR-AntonioNeural',
    'ru': 'ru-RU-DmitryNeural',
    'zh': 'zh-CN-YunxiNeural',
    'ja': 'ja-JP-KeitaNeural',
    'ko': 'ko-KR-InJoonNeural',
    'ar': 'ar-EG-ShakirNeural',
    'hi': 'hi-IN-MadhurNeural',
    'bn': 'bn-BD-NabanitaNeural'
    # Add more languages as needed
}

def translate_text(text, source_lang, target_lang):
    """
    Translate text using Google's Gemini model with specific focus on medical terminology.
    
    Args:
        text (str): The text to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
        
    Returns:
        str: Translated text
    """
    try:
        # Check if API key is set
        if not os.environ.get('GEMINI_API_KEY'):
            raise ValueError("GEMINI_API_KEY environment variable is not set")
            
        # Construct a prompt that emphasizes medical accuracy
        prompt = f"""Translate the following {source_lang} text to {target_lang}. 
This is for a healthcare conversation, so medical terminology must be translated accurately.
Maintain the original meaning, tone, and medical context.
Please respond ONLY with the translated text, no explanations or additional information.

Text to translate:
{text}"""

        # Use Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Generate the translation
        response = model.generate_content(prompt)
        
        # Extract the translated text from the response
        translated_text = response.text.strip()
        
        return translated_text
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise Exception(f"Translation failed: {str(e)}")

async def generate_speech(text, language):
    """
    Generate speech from text using edge-tts.
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code
        
    Returns:
        str: Base64-encoded audio data
    """
    try:
        # Get the appropriate voice for the language
        voice = LANGUAGE_TO_VOICE.get(language, 'en-US-ChristopherNeural')
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_filename = temp_file.name
        
        # Generate speech
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_filename)
        
        # Read the audio file and encode it to base64
        with open(temp_filename, "rb") as audio_file:
            audio_data = audio_file.read()
            base64_audio = base64.b64encode(audio_data).decode('utf-8')
        
        # Clean up the temporary file
        os.unlink(temp_filename)
        
        # Return the base64-encoded audio data as a data URL
        return f"data:audio/mp3;base64,{base64_audio}"
    
    except Exception as e:
        logger.error(f"Speech generation error: {str(e)}")
        raise Exception(f"Speech generation failed: {str(e)}")

def text_to_speech(text, language):
    """
    Synchronous wrapper for the asynchronous generate_speech function.
    
    Args:
        text (str): Text to convert to speech
        language (str): Language code
        
    Returns:
        str: Base64-encoded audio data
    """
    return asyncio.run(generate_speech(text, language))