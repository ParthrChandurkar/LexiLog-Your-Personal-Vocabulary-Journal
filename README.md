# LexiLog - Your Personal Vocabulary Journal

> A desktop vocabulary journal for capturing memorable words, phrases, and idioms from movies, then turning them into searchable notes, quiz practice, learning stats, and printable PDFs.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Tech Stack](#tech-stack)

---

## Overview

LexiLog helps movie lovers build vocabulary from real viewing moments. When a dialogue line, subtitle, or idiom stands out, you can save it with its meaning, source movie, context sentence, difficulty level, and review progress.

The working application is the Tkinter desktop app in `app.py`. The repository also includes `templates/web_app.html` as a static browser UI prototype; the API routes referenced by that prototype are not currently implemented in the Python app.

## At a Glance

| Area | What LexiLog Does |
|---|---|
| Capture | Save words, phrases, and idioms with meaning, movie source, context, and difficulty. |
| Review | Quiz yourself on unlearned entries and update review progress as you practice. |
| Explore | Search, filter, and inspect your vocabulary collection from a tabbed desktop interface. |
| Reflect | View learning statistics by type, difficulty, review count, and source movie. |
| Export | Generate a formatted PDF collection for offline revision or printing. |

---

## Features

- **Entry management** - Add, update, view, search, filter, and delete vocabulary entries.
- **Flexible entry types** - Organize content as words, phrases, or idioms.
- **Movie-based context** - Keep the original source movie and sentence context beside each meaning.
- **Difficulty tracking** - Mark entries as Easy, Medium, or Hard to guide review priority.
- **Interactive quiz mode** - Practice unlearned entries, reveal answers, and mark what you know.
- **Learning statistics** - Monitor totals, learned counts, difficulty breakdowns, most-reviewed entries, and movie-wise counts.
- **PDF export** - Generate a printable vocabulary collection with ReportLab.
- **MongoDB persistence** - Store entries in a MongoDB `vocabulary_db.words` collection.
- **Static web prototype** - Preview the browser UI draft in `templates/web_app.html`.

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
