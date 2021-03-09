from parser import Note

filename = "kern/chor001.krn"

notes = []
for note_str in ["4GG", "4d", "[4g", "4b"]:
    print(Note(note_str, 0).midi_code)

