from app import create_app
from config import DevelopmentConfig, ProductionConfig
import os

# You can choose which config to use based on an environment variable
# For development, you'll likely use DevelopmentConfig
# For production, you'll set FLASK_ENV to 'production' and use ProductionConfig
env = os.environ.get('FLASK_ENV', 'development')

if env == 'production':
    app = create_app(ProductionConfig)
else:
    app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    # This is for development purposes only.
    # For production, use a WSGI server like Gunicorn:
    # Example: gunicorn wsgi:app -w 4 -b 0.0.0.0:5000
    app.run(host='0.0.0.0', port=4000, debug=app.config['DEBUG'])