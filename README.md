# LexiLog — Your Personal Vocabulary Journal

> A personal vocabulary journal to collect words, phrases & idioms — straight from the movies you watch. Add meanings, context, and difficulty levels. Quiz yourself, track stats, and export your collection as a PDF. Build your lexicon, one scene at a time.

---

## Overview

LexiLog is a desktop + web vocabulary tracker built for movie lovers who want to grow and improvise their English vocabulary organically. Every time you encounter an unfamiliar word, phrase, or idiom while watching a film, you can log it instantly — along with its meaning, the movie it came from, a usage example, and its difficulty level. Over time, LexiLog becomes your personal lexicon, searchable, quizzable, and exportable.

---

## Features

- **Add Entries** — Log words, phrases, or idioms with meaning, source movie, context sentence, and difficulty (Easy / Medium / Hard)
- **View & Search** — Browse your full collection in a sortable table; filter by type or search by keyword
- **Quiz Mode** — Test yourself interactively to reinforce what you've learned
- **Statistics** — See your collection growth, difficulty breakdown, and review counts
- **Export to PDF** — Generate a beautifully formatted PDF of your vocabulary collection, grouped by type
- **MongoDB Backend** — All entries are persisted in a MongoDB Atlas cloud database
- **Web Interface** — Accessible via browser at `http://127.0.0.1:3000`

---

## Project Structure

```
LexiLog/
├── app.py              # Main Python application (Tkinter GUI + Flask server)
├── VocabApp.bat        # Windows launcher — double-click to run
├── templates/
│   └── web_app.html    # Web interface (browser UI)
└── .vscode/
    └── launch.json     # VS Code debug config for Chrome
```

---

## Requirements

- Python 3.8+
- MongoDB Atlas account (or local MongoDB instance)
- The following Python packages:

```
pip install pymongo reportlab flask
```

---

## Getting Started

### 1. Clone or download the project

```bash
git clone https://github.com/ParthrChandurkar/LexiLog-Your-Personal-Vocabulary-Journal.git

```

### 2. Configure MongoDB

In `app.py`, update the connection string with your own MongoDB Atlas URI:

```python
self.client = pymongo.MongoClient("your-mongodb-connection-string")
```

### 3. Run the app

**Option A — Windows (easiest):**
Double-click `VocabApp.bat`

**Option B — Terminal:**
```bash
python app.py
```

**Option C — Web interface:**
Start the server, then open your browser at:
```
http://127.0.0.1:3000/templates/web_app.html
```

---

## How to Use

1. Go to the **Add Entry** tab
2. Select the type: Word, Phrase, or Idiom
3. Fill in the word, its meaning, the movie name, a usage sentence, and difficulty
4. Hit **Save Entry**
5. Browse your entries in the **View All** tab
6. Test your knowledge in **Quiz Mode**
7. Export your full collection from the **Export PDF** tab

---

## Tech Stack

| Layer | Technology |
|---|---|
| Desktop GUI | Python, Tkinter |
| Web UI | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| Database | MongoDB Atlas |
| PDF Export | ReportLab |

---

## License

MIT License — free to use, modify, and share.
