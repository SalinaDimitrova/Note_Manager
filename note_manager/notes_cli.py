import shlex
from typing import Any, Optional
from note_manager.notes_service import NoteService
from note_manager.db import init_db

def parse_command(command: str) -> tuple[Optional[str], Optional[list[str]]]:
    parts = shlex.split(command)

    if not parts:
        return None, None

    if parts[0] != "notes":
        print("Commands must start with 'notes'")
        return None, None

    if len(parts) < 2:
        print("Missing command (e.g. 'notes list')")
        return None, None

    if parts[1] in ["--help"]:
        return "help", []

    return parts[1], parts[2:]

def handle_help(*_: Any) -> None:
    print("Commands:")
    print('  notes add "title" "content"')
    print("  notes list")
    print("  notes show <id>")
    print("  notes delete <id>")
    print("  notes exit/quit")

def handle_add(service: NoteService, args: list[str]) -> None:
    if len(args) < 2:
        print('Usage: notes add "title" "content"')
        return

    title = args[0]
    # joins the content arguments and supports multiline content
    content = " ".join(args[1:])
    content = content.encode().decode("unicode_escape")

    try:
        note_id = service.add_note(title, content)
        print(f"Note added with ID {note_id}")
    except ValueError as e:
        print(e)

def handle_list(service: NoteService, *_: Any) -> None:
    notes = service.list_notes()

    if not notes:
        print("No notes found")
        return

    for note in notes:
        print(f"[{note['id']}] {note['title']}")

def handle_show(service: NoteService, args: list[str]) -> None:
    if len(args) < 1:
        print("Usage: notes show <id>")
        return

    try:
        note_id = int(args[0])
    except ValueError:
        print("ID must be a number")
        return

    note = service.get_note(note_id)

    if note:
        print(f"ID: {note['id']}")
        print(f"Title: {note['title']}")
        print(f"Content: {note['content']}")
    else:
        print("Note not found")

def handle_delete(service: NoteService, args: list[str]) -> None:
    if len(args) < 1:
        print("Usage: notes delete <id>")
        return

    try:
        note_id = int(args[0])
    except ValueError:
        print("ID must be a number")
        return

    deleted = service.delete_note(note_id)

    if deleted:
        print("Note deleted")
    else:
        print("Note not found")

def main() -> None:
    init_db()
    service = NoteService()

    COMMANDS = {
        "help": handle_help,
        "add": handle_add,
        "list": handle_list,
        "show": handle_show,
        "delete": handle_delete,
    }

    try:
        while True:
            try:
                print("Enter a command:")
                command = input().strip()

                if not command:
                    continue

                cmd, args = parse_command(command)

                if not cmd:
                    print("--- \n")
                    continue

                if cmd in ["exit", "quit"]:
                    print("Goodbye!")
                    break

                handler = COMMANDS.get(cmd)

                if handler:
                    handler(service, args)
                else:
                    print("Unknown command. Type 'notes help'")

            except Exception as e:
                print(f"Error: {e}")

            print("--- \n")
    finally:
        service.close()

if __name__ == "__main__":
    main()