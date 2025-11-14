# Home Nexus

Home Nexus is a lightweight FastAPI-powered web application built for couples or families
who want a shared hub for day-to-day coordination. The project ships with a responsive
single-page interface designed to run nicely on mobile Safari so it can be saved to the
home screen on an iPhone.

## Features

- **Message board** – leave quick notes or reminders for one another.
- **Shared moments** – create longer posts to capture highlights or life updates.
- **To-do tracking** – add tasks, mark them complete, and remove them when finished.
- **Grocery list** – maintain a shared shopping list and track what you already bought.
- **Pantry & fridge inventory** – log ingredients manually or upload a photo for AI
  recognition that suggests what it sees and saves the items automatically.

## Getting started

### Requirements

- Python 3.11+
- (Optional) An OpenAI API key for the ingredient recognition feature.

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the app

```bash
uvicorn app.main:app --reload --port 8000
```

Visit [http://localhost:8000](http://localhost:8000) to open the interface.

### Configuring AI ingredient recognition

The `/api/pantry/recognize` endpoint uploads an image and forwards it to an OpenAI
vision-capable model (default: `gpt-4o-mini`). To enable it:

1. Install the optional dependency (already listed in `requirements.txt`).
2. Export your API key before starting the server:

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. (Optional) Override the default model:

   ```bash
   export OPENAI_VISION_MODEL="gpt-4o"
   ```

If these variables are not set, the backend will return a helpful error message and the
front-end status panel will display the issue.

### Database

The application uses SQLite by default (`data.db` in the project root) and automatically
creates the necessary tables at startup.

## Project structure

```
app/
  main.py             # FastAPI application and API routes
  database.py         # Database engine helpers
  models.py           # SQLModel models & response schemas
  openai_client.py    # Helper for invoking OpenAI's vision API
static/
  index.html          # Responsive single-page UI
  app.js              # Front-end logic communicating with the API
  styles.css          # Tailored styling with mobile-friendly layout
requirements.txt
```

## Production notes

- Configure HTTPS and authentication before exposing the app publicly.
- Consider swapping SQLite with PostgreSQL by adjusting `DATABASE_URL` in
  `app/database.py` for concurrent, multi-device access.
- The OpenAI call is synchronous; for heavy usage you may want to move it to a
  background task queue.
