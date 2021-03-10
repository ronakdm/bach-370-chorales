from parser import KernParser, KernSpine, Note
import numpy as np
import torch
import re


class BachChorale:
    def __init__(self, file_path):

        self.parser = KernParser()
        self.number = int(re.search("([0-9]+)", file_path).group(1))
        self.len = 0

        with open(file_path, "r") as f:
            lines = f.readlines()

            self.title = self.parser.get_german_title(lines)
            self.key_signature = self.parser.get_key_signature(lines)
            self.time_signature = self.parser.get_time_signature(lines)
            self.soprano, self.alto, self.tenor, self.bass = self.get_data(lines)

    def get_data(self, lines):
        min_note = np.inf
        max_note = -np.inf
        bass, tenor, alto, soprano = KernSpine(), KernSpine(), KernSpine(), KernSpine()

        for lineno, line in enumerate(lines):
            if self.parser.is_data_record(line):
                # Note a barline.
                if line[0] != "=":
                    note_strs = line.split()
                    for i, spine in enumerate([bass, tenor, alto, soprano]):
                        note_str = note_strs[i]
                        # Not a placeholder.
                        if note_str[0] != ".":
                            note = Note(note_str, lineno)
                            if note.midi_code != self.parser.rest_code:
                                min_note = min(min_note, note.midi_code)
                                max_note = max(max_note, note.midi_code)

                            spine.append(note)

        self.min_note = int(min_note)
        self.max_note = int(max_note)

        # These should be the same but whatevs.
        self.len = np.max([bass.len, tenor.len, alto.len, soprano.len])

        return soprano, alto, tenor, bass

    def to_tensor(self, num_pitches, offset=0):

        output = torch.zeros(4, num_pitches, self.len + 1, dtype=torch.int32)

        for i, spine in enumerate([self.bass, self.tenor, self.alto, self.soprano]):
            output[i] = spine.to_tensor(num_pitches, offset=offset)

        return output
