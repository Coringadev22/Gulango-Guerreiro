# Gulango Guerreiro

This is a Django project for a medieval learning platform.

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file and adjust the values:
   ```bash
   cp .env.example .env
   # edit .env to set your secret key and other settings
   ```
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

The OpenAI integration requires setting the `OPENAI_API_KEY` environment variable.
