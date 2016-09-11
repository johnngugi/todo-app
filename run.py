import os
from app import create_app, db
app = create_app(os.getenv('FLASK_CONFIG') or 'production')

if __name__ == '__main__':
    app.run()
