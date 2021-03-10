import itertools
import re
import torch


class ParsingError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def error(message, line):
    raise ParsingError("[line {}] {}".format(line + 1, message))


rest_code = -10


class KernParser:
    def __init__(self):
        sharps = ["f#", "c#", "g#", "d#", "a#", "e#", "b#"]
        flats = ["b-", "e-", "a-", "d-", "g-", "c-", "f-"]
        self.key_sigs = (
            [""]
            + list(itertools.accumulate(sharps))
            + list(itertools.accumulate(flats))
        )
        self.rest_code = rest_code
        self.time_sigs = {"M3/4": (3, 4), "M4/4": (4, 4), "M3/2": (3, 2)}
        self.german_title_comment = "!!!OTL@@DE:"

    def is_interpretation_record(self, line):
        return line[0] == "*"

    def is_comment_record(self, line):
        return line[0] == "!"

    def is_data_record(self, line):
        return not (self.is_interpretation_record(line) or self.is_comment_record(line))

    def get_key_signature(self, lines):
        for line in lines:
            if self.is_interpretation_record(line) and "*k[" in line:
                for key_sig in self.key_sigs:
                    if "*k[" + key_sig + "]" in line:
                        return key_sig
        return None

    def get_time_signature(self, lines):
        for line in lines:
            if self.is_interpretation_record(line):
                for time_sig in self.time_sigs:
                    if time_sig in line:
                        return self.time_sigs[time_sig]
        return None

    def get_german_title(self, lines):
        for line in lines:
            if self.german_title_comment in line:
                return line.replace(self.german_title_comment, "").strip()
        return None


class Note:
    def __init__(self, note_str, lineno):

        self.pitch_map = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}

        try:

            # Set duration in terms of number of bars.
            note_len = int(re.search("([0-9]+)", note_str).group(1))
            if note_len == 0:
                self.duration = 2
            else:
                self.duration = 1 / note_len

            # Handle dotted notes.
            if "." in note_str:
                self.duration *= 1.5

            # Get pitch from rest of the note.
            self.midi_code = self.parse_pitch(note_str, lineno)
        except Exception:
            error("Unable to handle input '%s'" % note_str, lineno)

    def parse_pitch(self, item, lineno):

        if re.search("r", item):
            return rest_code

        note = re.search("([a-gA-G]+)", item)
        if not note:
            error("Unhandled non-note non-rest item: %s" % item, lineno)
        note = note.group(1)

        pitch = note[0].lower()
        if pitch == note[0]:  # middle C or higher
            octave = 3 + len(note)
        else:  # below middle C
            octave = 4 - len(note)

        sharp = re.search(r"(\#+)", item)
        flat = re.search(r"(\-+)", item)
        if sharp and flat:
            error("Note cannot be sharp and flat.", lineno)
        sharp = len(sharp.group(1)) if sharp else 0
        flat = len(flat.group(1)) if flat else 0

        midi_code = 60 + 12 * (octave - 4) + self.pitch_map[pitch] + sharp - flat

        return midi_code


class KernSpine:
    def __init__(self, grid_size=16):
        self.notes = []
        if grid_size in [1, 2, 4, 8, 16]:
            self.grid_size = grid_size
        else:
            raise ValueError("grid_size must be 1, 2, 4, 8, or 16!")

        self.len = 0

    def append(self, note):
        self.notes.append(note)
        self.len += int(note.duration * self.grid_size)

    def to_tensor(self, num_pitches, offset=0):

        output = torch.zeros(num_pitches, self.len + 1, dtype=torch.int32)

        index = 0
        for note in self.notes:
            num_steps = int(note.duration * self.grid_size)
            if note.midi_code != rest_code:
                for t in range(num_steps):
                    output[offset + note.midi_code, index + t] = 1
            index += num_steps

        # End of sequence code = 0.
        output[0, index] = 1

        return output

