import itertools


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
    def __init__(self, note_str):
        # TODO: parse these from string.
        self.letter = None
        self.octave = None
        self.pitch = None
        self.duration = None


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
