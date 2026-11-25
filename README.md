# EduGuide Streamlit App

## Run locally
1. Install packages: `pip install -r requirements.txt`
2. Create `.streamlit/secrets.toml` with:
   `GROQ_API_KEY = "your_groq_api_key"`
3. Run: `streamlit run app.py`

## Deploy on Streamlit Community Cloud
1. Upload `app.py` and `requirements.txt` to a GitHub repository.
2. On Streamlit Community Cloud, create a new app and select that repository.
3. Set the main file path to `app.py`.
4. In App settings > Secrets, add:
   `GROQ_API_KEY = "your_groq_api_key"`
5. Save and deploy.

Never upload your API key to GitHub or put it directly in app.py.
