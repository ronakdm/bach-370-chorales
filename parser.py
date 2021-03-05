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

    def is_interpretation_record(line):
        return line[0] == "*"

    def is_comment_record(line):
        return line[0] == "!"

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


class BachChorale:
    def __init__(self, file_path):

        self.parser = KernParser()

        with open(file_path, "r") as f:
            lines = f.readlines()

            self.title = self.parser.get_german_title(lines)
            self.key_signature = self.parser.get_key_signature(lines)
            self.time_signature = self.parser.get_time_signature(lines)

    def to_numpy(self):
        pass

    def to_torch(self):
        pass
