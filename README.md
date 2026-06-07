# LexiLog - Your Personal Vocabulary Journal

> A personal vocabulary journal to collect words, phrases, and idioms from the movies you watch. Add meanings, context, and difficulty levels. Quiz yourself, track stats, and export your collection as a PDF.

---

## Overview

LexiLog is a desktop vocabulary tracker for movie lovers who want to grow their English vocabulary organically. Every time you encounter an unfamiliar word, phrase, or idiom while watching a film, you can log it with its meaning, source movie, usage context, and difficulty level.

The current runnable application is the Tkinter app in `app.py`. The repository also includes `templates/web_app.html` as a static browser UI prototype, but the REST API routes referenced by that file are not currently implemented in the Python app.

---

## Features

- **Add Entries** - Log words, phrases, or idioms with meaning, source movie, context sentence, and difficulty.
- **View and Search** - Browse the full collection and search by word, meaning, or movie.
- **Quiz Mode** - Practice unlearned entries and update review progress.
- **Statistics** - See totals, learned counts, difficulty breakdowns, most-reviewed entries, and movie-wise counts.
- **Export to PDF** - Generate a formatted vocabulary collection with ReportLab.
- **MongoDB Persistence** - Store entries in a MongoDB `vocabulary_db.words` collection.
- **Static Web Prototype** - Inspect the browser UI draft in `templates/web_app.html`.

---

## Architecture

![LexiLog architecture diagram](assets/architecture.svg)

---

## Data Flow

1. The user starts the app through `VocabApp.bat` or by running `app.py`.
2. The Tkinter tabs call methods on the `VocabularyApp` controller.
3. Entries are saved, searched, updated, deleted, and counted in MongoDB.
4. Quiz and review actions update review counters and learned status.
5. PDF export reads selected entries and renders a vocabulary collection file.

---

## Project Structure

```text
LexiLog/
|-- app.py                    # Main Tkinter app, MongoDB logic, quiz/stats, PDF export
|-- VocabApp.bat              # Windows launcher
|-- assets/
|   `-- architecture.svg      # README architecture diagram
|-- templates/
|   `-- web_app.html          # Static browser UI prototype
`-- .vscode/
    `-- launch.json           # VS Code debug config
```

---

## Requirements

- Python 3.8+
- MongoDB Atlas account or local MongoDB instance
- Python packages:

```bash
pip install pymongo reportlab
```

---

## Getting Started

### 1. Clone the project

```bash
git clone https://github.com/ParthrChandurkar/LexiLog-Your-Personal-Vocabulary-Journal.git
cd LexiLog-Your-Personal-Vocabulary-Journal
```

### 2. Configure MongoDB

In `app.py`, update the connection string with your own MongoDB URI:

```python
self.client = pymongo.MongoClient("your-mongodb-connection-string")
```

### 3. Run the desktop app

Windows:

```text
Double-click VocabApp.bat
```

Terminal:

```bash
python app.py
```

Optional: open `templates/web_app.html` to view the browser UI prototype. It needs matching backend API routes before it can work as a live web app.

---

## How to Use

1. Go to the **Add Entry** tab.
2. Select the type: Word, Phrase, or Idiom.
3. Fill in the word, meaning, movie name, usage context, and difficulty.
4. Save the entry.
5. Browse entries in the **View All** tab.
6. Practice from **Quiz Mode**.
7. Export your collection from the **Export PDF** tab.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Desktop GUI | Python, Tkinter |
| App Logic | Python `VocabularyApp` class |
| Prototype Web UI | HTML, CSS, JavaScript |
| Database | MongoDB Atlas |
| PDF Export | ReportLab |

---

## License

MIT License - free to use, modify, and share.
