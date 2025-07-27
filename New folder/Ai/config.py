import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-fallback-key-for-dev'
    # Default to development settings
    DEBUG = True
    TESTING = False
    # You might have different database URIs for development, testing, production
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # Example for your AES keys (still recommend environment variables for production)
    AES_ENCRYPTION_KEY_STRING = "e36581506fde7939670430d04d8d7242"# This will be loaded as UTF-8 bytes
    AES_IV_STRING = "20f92fa82d3305b2" # This will be loaded as UTF-8 bytes

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # In production, these should come from environment variables or KMS
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:pass@host:port/dbname'
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') # Mandatory in prod
    # You'd typically fetch AES_KEY_STRING/IV_STRING from a KMS here