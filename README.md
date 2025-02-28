# Healthcare Translation Web App

A real-time, multilingual translation application designed for healthcare settings to facilitate communication between patients and providers who speak different languages.

## Features

- **Voice-to-Text**: Convert spoken input into text transcripts with enhanced accuracy for medical terminology
- **Real-Time Translation**: Translate conversations between multiple languages in real-time
- **Audio Playback**: Listen to translations with the click of a button
- **Mobile-First Design**: Optimized for both mobile and desktop use
- **Dual Transcript Display**: View both original and translated text simultaneously

## Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Translation**: OpenAI GPT/Google Gemini API
- **Text-to-Speech**: Edge TTS
- **Speech Recognition**: Web Speech API

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Gemini API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Translation-Web-App.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Running the Application

1. Start the development server:
   ```bash
   python run.py
   ```

2. Open your browser and navigate to `http://localhost:8000`

### Using Docker

1. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

2. Open your browser and navigate to `http://localhost:8000`

## Usage Guide

1. **Select Languages**: Choose the patient's language and the provider's language from the dropdowns
2. **Start Recording**: Click the "Start Recording" button and speak into your device's microphone
3. **View Transcription**: As you speak, your words will be transcribed in real-time
4. **Stop Recording**: Click "Stop Recording" when finished speaking
5. **View Translation**: The translated text will appear in the opposite panel
6. **Audio Playback**: Click the "Play Audio" button to hear the translation spoken aloud

## Security and Privacy

- Speech processing happens on the client device before being sent for translation
- No patient data is permanently stored
- Basic security measures are implemented to protect user privacy
- This application is not HIPAA-compliant and should not be used for sensitive patient information

## License

This project is licensed under the Apache License - see the LICENSE file for details.

## Acknowledgments

- Google for providing the translation API
- Edge TTS for text-to-speech capabilities
- Web Speech API for speech recognition