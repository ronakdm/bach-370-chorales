import itertools
import re


class ParsingError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def error(message, line):
    raise ParsingError("[line {}] {}".format(line + 1, message))


class KernParser:
    def __init__(self):
        sharps = ["f#", "c#", "g#", "d#", "a#", "e#", "b#"]
        flats = ["b-", "e-", "a-", "d-", "g-", "c-", "f-"]
        self.key_sigs = (
            [""]
            + list(itertools.accumulate(sharps))
            + list(itertools.accumulate(flats))
        )
        # TODO: check if other time signatures besides 3/4 and 4/4 are present.
        self.time_sigs = {"M3/4": (3, 4), "M4/4": (4, 4)}
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

    def get_time_signature(self, lines):
        for line in lines:
            if self.is_interpretation_record(line):
                for time_sig in self.time_sigs:
                    if time_sig in line:
                        return self.time_sigs[time_sig]

    def get_german_title(self, lines):
        for line in lines:
            if self.german_title_comment in line:
                return line.replace(self.german_title_comment, "").strip()


class Note:
    def __init__(self, note_str, lineno):

        self.pitch_map = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}

        if note_str != ".":
            if note_str[0] == "[":
                self.duration = 1 / int(note_str[1])
                item = note_str[2:]
            else:
                self.duration = 1 / int(note_str[0])
                item = note_str[1:]
            self.midi_code = self.parse_pitch(item, lineno)

    def set_attr(self, note_str, lineno, duration):
        """
        To be used when we encounter a ".". We initially set the note as empty.
        Then, after the duration is resolved (at the end of a barline), we can set its attributes.
        """
        self.duration = duration
        item = note_str[2:] if note_str[0] == "[" else note_str[1:]
        self.midi_code = self.parse_pitch(item, lineno)

    def parse_pitch(self, item, lineno):

        if item[0] == "r":
            return "rest"

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
    def __init__(self):
        self.notes = []

    def append(self, note):
        self.notes.append(note)

    def to_numpy(self):
        # TODO: Once note representation is decided.
        pass

    def to_tensor(self):
        # TODO: Once note representation is decided.
        pass
