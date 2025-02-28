"""
Configuration settings for the Healthcare Translation Web App.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    DEBUG = False
    TESTING = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    # In production, ensure SECRET_KEY is properly set
    if not os.environ.get('SECRET_KEY') or os.environ.get('SECRET_KEY') == 'dev-key-for-development-only':
        raise ValueError("SECRET_KEY environment variable not set or using default value in production")

    # In production, ensure GEMINI_API_KEY is set
    if not os.environ.get('GEMINI_API_KEY'):
        raise ValueError("GEMINI_API_KEY environment variable not set in production")

# Set the configuration based on the environment
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Default to the base config
Config = config_by_name.get(os.environ.get('FLASK_ENV', 'development'), DevelopmentConfig)