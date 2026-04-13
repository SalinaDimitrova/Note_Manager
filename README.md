# 📝 Note Manager CLI

A simple command-line note-taking application written in Python.

This project demonstrates clean architecture, command-line interface design, and basic data persistence using SQLite.

---

## 🚀 Features

- Add notes with title and content
- List all notes
- View a note by ID
- Delete notes
- Help 
- Enforced unique titles (no duplicate notes)
- Interactive CLI mode (continuous command input)
- Persistent storage using SQLite

---

## 🛠️ Tech Stack

- Python 3
- SQLite (via built-in `sqlite3`)
- Pytest (for testing)

---

## 📂 Project Structure
```bash
NoteManager/
│
├── note_manager/
│ ├── __init__.py
│ ├── db.py
│ ├── notes_service.py
│ ├── notes_cli.py
│
├── tests/
│ └── test_notes_service.py
│
├── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone git@github.com:SalinaDimitrova/Note_Manager.git
cd NoteManager
```
---
## ▶️ Running the Application

Start the CLI application:

```bash
python note_manager/notes_cli.py

notes add "Meeting" "Discuss Q3 budget"
notes list
notes show 1
notes delete 1
notes exit/quit
```
---
## 🧪 Running Tests

This project includes unit tests for the service layer.

### Install dependencies

```bash
pip install pytest
pytest
```
- Tests are executed against an in-memory database (`:memory:`) for better isolation and performance
---
## 💡 Notes

- All commands must start with `notes`
- Titles must be unique
- The application runs in a continuous loop until you exit