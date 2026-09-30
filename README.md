# LexiLog

LexiLog is a Python desktop vocabulary journal for recording words, meanings, examples, and review progress. It stores entries in MongoDB and includes a separate HTML prototype for previewing the interface in a browser.

## Features

- Add, edit, delete, search, and filter vocabulary entries
- Track mastery and review status
- Practice saved words and export vocabulary data
- MongoDB-backed persistence
- Tkinter desktop interface and PDF export through ReportLab

## Architecture

`app.py` contains the desktop interface, application logic, and MongoDB access. `templates/web_app.html` is a standalone browser prototype; it is not the primary application and does not replace the Python desktop client.

## Getting Started

Prerequisites: Python 3, MongoDB, and Tk support.

```bash
python -m venv .venv
python -m pip install pymongo reportlab
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

The included `VocabApp.bat` contains an absolute path from the original development machine. Update that path before using the launcher, or run `python app.py` directly.

## Configuration

`app.py` currently contains a hardcoded MongoDB connection string. Replace it with an environment-based value and rotate the exposed database credential before running or publishing the application. This README does not reproduce that credential.

## Limitations

- Dependencies are not pinned in a requirements file.
- Automated tests are not included.
- The desktop application and browser prototype are separate implementations.
- The current source requires manual secret-remediation work; this README change intentionally does not modify application code.

