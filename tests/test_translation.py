"""
Tests for the Healthcare Translation Web App translation functionality.
"""
import pytest
import base64
from unittest.mock import patch, MagicMock
from app.translation import translate_text

@pytest.fixture
def mock_openai_response():
    """Create a mock response for the OpenAI API."""
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Translated text"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    return mock_response

@patch('openai.chat.completions.create')
def test_translate_text(mock_openai_create, mock_openai_response):
    """Test that the translate_text function calls OpenAI and returns the expected result."""
    # Setup the mock
    mock_openai_create.return_value = mock_openai_response
    
    # Call the function
    result = translate_text("Hello", "en", "es")
    
    # Check that OpenAI was called with the expected parameters
    mock_openai_create.assert_called_once()
    call_args = mock_openai_create.call_args[1]
    assert call_args['model'] == "gpt-4o"
    assert len(call_args['messages']) == 2
    assert call_args['messages'][0]['role'] == "system"
    assert "Hello" in call_args['messages'][1]['content']
    assert call_args['temperature'] == 0.3
    
    # Check the result
    assert result == "Translated text"

@patch('openai.chat.completions.create')
def test_translate_text_error_handling(mock_openai_create):
    """Test that the translate_text function handles errors properly."""
    # Setup the mock to raise an exception
    mock_openai_create.side_effect = Exception("API error")
    
    # Check that the function raises an exception with the expected message
    with pytest.raises(Exception) as excinfo:
        translate_text("Hello", "en", "es")
    
    assert "Translation failed" in str(excinfo.value)