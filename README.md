# Uzbekistan itinerary (Streamlit)

Simple Streamlit app showing a May 2026 calendar with May 1–10 clickable, and an itinerary panel.

## Run

```bash
cd uzbekistan_itinerary_streamlit
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- The "weather forecast" text is a placeholder (no external API calls).
- Clicking a day uses a `?day=` query parameter, so the URL is shareable (e.g. `?day=7`).
