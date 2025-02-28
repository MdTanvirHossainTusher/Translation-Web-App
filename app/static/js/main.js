/**
 * Healthcare Translator Application
 * Main JavaScript functionality for the real-time healthcare translation web application.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const startRecordingBtn = document.getElementById('start-recording');
    const stopRecordingBtn = document.getElementById('stop-recording');
    const originalTranscript = document.getElementById('original-transcript');
    const translatedTranscript = document.getElementById('translated-transcript');
    const playOriginalBtn = document.getElementById('play-original');
    const playTranslationBtn = document.getElementById('play-translation');
    const sourceLangSelect = document.getElementById('source-language');
    const targetLangSelect = document.getElementById('target-language');
    const sourceLangDisplay = document.getElementById('source-language-display');
    const targetLangDisplay = document.getElementById('target-language-display');
    const swapLangsBtn = document.getElementById('swap-languages');
    const translationStatus = document.getElementById('translation-status');
    const loadingOverlay = document.getElementById('loading-overlay');
    const errorNotification = document.getElementById('error-notification');
    const dismissErrorBtn = document.getElementById('dismiss-error');
    const currentYearEl = document.getElementById('current-year');

    // Set current year in footer
    currentYearEl.textContent = new Date().getFullYear();

    // Speech recognition variables
    let recognition = null;
    let isRecording = false;
    let currentTranscript = '';
    let currentTranslation = '';

    // Initialize the SpeechRecognition API with browser compatibility
    function initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            showError('Speech recognition is not supported in your browser. Please try Chrome, Edge, or Safari.');
            startRecordingBtn.disabled = true;
            return false;
        }
        
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        
        // Set the language based on the selected source language
        recognition.lang = getLanguageCode(sourceLangSelect.value);
        
        // Handle results event
        recognition.onresult = (event) => {
            let interimTranscript = '';
            
            // Combine results from all recognition attempts
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    currentTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }
            
            // Update the transcript display with current and interim text
            originalTranscript.innerHTML = `
                <div class="final">${currentTranscript}</div>
                <div class="interim">${interimTranscript}</div>
            `;
            
            // Enable the play button if there's something to play
            playOriginalBtn.disabled = !(currentTranscript.trim().length > 0);
            
            // Automatically translate after a brief pause in speaking
            debounceTranslate();
        };
        
        // Handle errors
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            showError(`Speech recognition error: ${event.error}`);
            stopRecording();
        };
        
        return true;
    }

    // Translation with debounce to avoid too many requests
    let translateTimeout = null;
    const debounceTranslate = () => {
        clearTimeout(translateTimeout);
        translateTimeout = setTimeout(() => {
            if (currentTranscript.trim().length > 0) {
                translateText(currentTranscript);
            }
        }, 1000); // Wait 1 second after speech pauses
    };

    // Start recording
    function startRecording() {
        // Initialize or reinitialize speech recognition if needed
        if (!recognition) {
            if (!initSpeechRecognition()) {
                return; // Exit if speech recognition can't be initialized
            }
        } else {
            // Update the language
            recognition.lang = getLanguageCode(sourceLangSelect.value);
        }
        
        try {
            recognition.start();
            isRecording = true;
            updateUIForRecording(true);
            translationStatus.textContent = 'Listening...';
        } catch (error) {
            console.error('Error starting speech recognition:', error);
            showError('Failed to start recording. Please refresh the page and try again.');
        }
    }

    // Stop recording
    function stopRecording() {
        if (recognition && isRecording) {
            try {
                recognition.stop();
                isRecording = false;
                updateUIForRecording(false);
                translationStatus.textContent = 'Processing final translation...';
                
                // Trigger a final translation
                if (currentTranscript.trim().length > 0) {
                    clearTimeout(translateTimeout);
                    translateText(currentTranscript, true);
                } else {
                    translationStatus.textContent = 'No speech detected';
                }
            } catch (error) {
                console.error('Error stopping speech recognition:', error);
            }
        }
    }

    // Update UI elements based on recording state
    function updateUIForRecording(isRecording) {
        startRecordingBtn.disabled = isRecording;
        stopRecordingBtn.disabled = !isRecording;
        
        // Disable language selection during recording
        sourceLangSelect.disabled = isRecording;
        targetLangSelect.disabled = isRecording;
        swapLangsBtn.disabled = isRecording;
        
        // Visual indication of recording state
        if (isRecording) {
            startRecordingBtn.classList.add('recording');
            document.body.classList.add('is-recording');
        } else {
            startRecordingBtn.classList.remove('recording');
            document.body.classList.remove('is-recording');
        }
    }

    // Translate text using the server API
    async function translateText(text, isFinal = false) {
        try {
            if (!text.trim()) return;
            
            translationStatus.textContent = 'Translating...';
            
            if (isFinal) {
                showLoading(true);
            }
            
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    source_lang: sourceLangSelect.value,
                    target_lang: targetLangSelect.value,
                }),
            });
            
            if (!response.ok) {
                throw new Error(`Translation API error: ${response.status}`);
            }
            
            const data = await response.json();
            currentTranslation = data.translated_text;
            
            // Update the translation display
            translatedTranscript.textContent = currentTranslation;
            
            // Enable the play translation button
            playTranslationBtn.disabled = false;
            
            // Update status
            translationStatus.textContent = isFinal ? 'Translation complete' : 'Translation updated';
            
            if (isFinal) {
                showLoading(false);
            }
        } catch (error) {
            console.error('Translation error:', error);
            translationStatus.textContent = 'Translation failed';
            showError('Translation failed. Please try again.');
            
            if (isFinal) {
                showLoading(false);
            }
        }
    }

    // Text-to-speech function
    async function textToSpeech(text, language) {
        try {
            showLoading(true);
            
            const response = await fetch('/api/text-to-speech', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    language: language,
                }),
            });
            
            if (!response.ok) {
                throw new Error(`Text-to-speech API error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Play the audio
            const audio = new Audio(data.audio_data_url);
            audio.onended = () => {
                showLoading(false);
            };
            audio.onerror = () => {
                showError('Failed to play audio. Please try again.');
                showLoading(false);
            };
            
            await audio.play();
        } catch (error) {
            console.error('Text-to-speech error:', error);
            showError('Failed to generate or play speech. Please try again.');
            showLoading(false);
        }
    }

    // Convert language code to full locale code for speech recognition
    function getLanguageCode(langCode) {
        const langMap = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-BR',
            'ru': 'ru-RU',
            'zh': 'zh-CN',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'ar': 'ar-SA',
            'hi': 'hi-IN',
            // Add more as needed
        };
        
        return langMap[langCode] || 'en-US';
    }

    // Swap source and target languages
    function swapLanguages() {
        const sourceVal = sourceLangSelect.value;
        const targetVal = targetLangSelect.value;
        
        sourceLangSelect.value = targetVal;
        targetLangSelect.value = sourceVal;
        
        updateLanguageDisplay();
        
        // Clear transcripts when languages are swapped
        clearTranscripts();
    }

    // Update language display elements
    function updateLanguageDisplay() {
        const getLanguageName = (select) => {
            return select.options[select.selectedIndex].text.split(' ')[0];
        };
        
        sourceLangDisplay.textContent = `(${getLanguageName(sourceLangSelect)})`;
        targetLangDisplay.textContent = `(${getLanguageName(targetLangSelect)})`;
    }

    // Clear transcripts and reset state
    function clearTranscripts() {
        currentTranscript = '';
        currentTranslation = '';
        originalTranscript.innerHTML = '';
        translatedTranscript.textContent = '';
        playOriginalBtn.disabled = true;
        playTranslationBtn.disabled = true;
        translationStatus.textContent = 'Ready for translation';
    }

    // Show/hide loading overlay
    function showLoading(show) {
        if (show) {
            loadingOverlay.classList.remove('hidden');
        } else {
            loadingOverlay.classList.add('hidden');
        }
    }

    // Show error notification
    function showError(message) {
        const errorText = errorNotification.querySelector('p');
        errorText.textContent = message;
        errorNotification.classList.remove('hidden');
    }

    // Dismiss error notification
    function dismissError() {
        errorNotification.classList.add('hidden');
    }

    // Event listeners
    startRecordingBtn.addEventListener('click', startRecording);
    stopRecordingBtn.addEventListener('click', stopRecording);
    
    playOriginalBtn.addEventListener('click', () => {
        if (currentTranscript.trim()) {
            textToSpeech(currentTranscript, sourceLangSelect.value);
        }
    });
    
    playTranslationBtn.addEventListener('click', () => {
        if (currentTranslation.trim()) {
            textToSpeech(currentTranslation, targetLangSelect.value);
        }
    });
    
    swapLangsBtn.addEventListener('click', swapLanguages);
    
    sourceLangSelect.addEventListener('change', () => {
        updateLanguageDisplay();
        clearTranscripts();
        
        // If recording, stop and restart with new language
        if (isRecording) {
            stopRecording();
            setTimeout(() => {
                startRecording();
            }, 300);
        }
    });
    
    targetLangSelect.addEventListener('change', () => {
        updateLanguageDisplay();
        
        // Clear just the translation, keep the original
        currentTranslation = '';
        translatedTranscript.textContent = '';
        playTranslationBtn.disabled = true;
        
        // Retranslate if there's existing content
        if (currentTranscript.trim()) {
            translateText(currentTranscript);
        }
    });
    
    dismissErrorBtn.addEventListener('click', dismissError);

    // Check for browser compatibility on page load
    if (!(window.SpeechRecognition || window.webkitSpeechRecognition)) {
        showError('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
        startRecordingBtn.disabled = true;
    }

    // Initialize language display
    updateLanguageDisplay();
});