import pytest
from note_manager.notes_service import NoteService

def setup_in_memory_db(service: NoteService) -> None:
    cursor = service.conn.cursor()
    cursor.execute("""
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL
        )
    """)
    service.conn.commit()

def create_service() -> NoteService:
    service = NoteService(":memory:")
    setup_in_memory_db(service)
    return service

#1. add note
def test_add_note():
    service = create_service()

    note_id = service.add_note("Test", "Content")

    assert note_id == 1

#2. list notes
def test_list_notes():
    service = create_service()

    service.add_note("Test", "Content")
    notes = service.list_notes()

    assert len(notes) == 1
    assert notes[0]["title"] == "Test"

#3. get note
def test_get_note():
    service = create_service()

    note_id = service.add_note("Test", "Content")
    note = service.get_note(note_id)

    assert note is not None
    assert note["id"] == note_id

#4. get non-existing note
def test_get_note_not_found():
    service = create_service()

    note = service.get_note(999)

    assert note is None

#5. delete note
def test_delete_note():
    service = create_service()

    note_id = service.add_note("Test", "Content")
    deleted = service.delete_note(note_id)

    assert deleted == 1

#6. delete non-existing note
def test_delete_note_not_found():
    service = create_service()

    deleted = service.delete_note(999)

    assert deleted == 0

#7. unique title constraint
def test_duplicate_title():
    service = create_service()

    service.add_note("Test", "Content")

    with pytest.raises(ValueError):
        service.add_note("Test", "Another content")

# 8. empty title
def test_empty_title():
    service = create_service()

    with pytest.raises(ValueError):
        service.add_note("", "Content")