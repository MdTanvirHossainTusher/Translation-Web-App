"""
Route definitions for the Healthcare Translation Web App.
"""
from flask import Blueprint, render_template, jsonify, request, current_app
import logging
from app.translation import translate_text, text_to_speech

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')

@main_bp.route('/user-guide')
def user_guide():
    """Render the user guide page."""
    return render_template('user_guide.html')

@main_bp.route('/api/translate', methods=['POST'])
def api_translate():
    """API endpoint to translate text."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        text = data.get('text')
        source_lang = data.get('source_lang')
        target_lang = data.get('target_lang')
        
        if not all([text, source_lang, target_lang]):
            return jsonify({"error": "Missing required fields: text, source_lang, or target_lang"}), 400
        
        # Log the translation request (but not the full text for privacy)
        logger.info(f"Translation request: {len(text)} chars from {source_lang} to {target_lang}")
        
        # Perform the translation
        translated_text = translate_text(text, source_lang, target_lang)
        
        return jsonify({
            "original_text": text,
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang
        })
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/api/text-to-speech', methods=['POST'])
def api_text_to_speech():
    """API endpoint to convert text to speech."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        text = data.get('text')
        language = data.get('language')
        
        if not all([text, language]):
            return jsonify({"error": "Missing required fields: text or language"}), 400
        
        # Log the TTS request
        logger.info(f"Text-to-speech request: {len(text)} chars in {language}")
        
        # Convert text to speech and get the audio data URL
        audio_data_url = text_to_speech(text, language)
        
        return jsonify({
            "audio_data_url": audio_data_url,
            "text": text,
            "language": language
        })
    
    except Exception as e:
        logger.error(f"Text-to-speech error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main_bp.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy"}), 200