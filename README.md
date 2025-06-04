# Contextify
A application for connecting news to your interests

## Running the application
1. Copy `.env.example`, fill it in, and rename the copy to `.env`
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python run_app.py
```

This will:
- Generate your interest profile from browser history
- Fetch the latest news
- Start the Streamlit app