from parser import KernParser, KernSpine, Note


class BachChorale:
    def __init__(self, file_path):

        self.parser = KernParser()
        self.file_path = file_path

        with open(file_path, "r") as f:
            lines = f.readlines()

            self.title = self.parser.get_german_title(lines)
            self.key_signature = self.parser.get_key_signature(lines)
            self.time_signature = self.parser.get_time_signature(lines)
            self.soprano, self.alto, self.tenor, self.bass = self.get_data(lines)

    def get_data(self, lines):
        min_note = 100000
        max_note = -100000
        extend_token = "."
        barline_token = "="

        bass, tenor, alto, soprano = KernSpine(), KernSpine(), KernSpine(), KernSpine()
        for i, spine in enumerate([bass, tenor, alto, soprano]):
            total_on_duration = 1  # How much of the measure has given notes.
            previous_note = None
            for lineno, line in enumerate(lines):
                if self.parser.is_data_record(line):
                    if line[0] != barline_token:
                        note_str = line.split()[i]

                        if note_str == extend_token:
                            if previous_note != extend_token:
                                # We have hit a string (".") that extends the previous notes.
                                # If the previous note is also an extension, then ignore this.
                                # Otherwise, we put a filler note in the spine, and resolve
                                # it's length after we have hit the barline.
                                note_to_extend = previous_note
                                extension = Note(note_str, lineno)
                                spine.append(extension)
                        else:
                            note = Note(note_str, lineno)
                            if note.midi_code != "rest":
                                min_note = min(min_note, note.midi_code)
                                max_note = max(max_note, note.midi_code)

                            total_on_duration += note.duration
                            spine.append(note)
                        previous_note = note_str
                    else:
                        # Resolve the lengths of extensions ("."). We must infer the length
                        # of durations based on the length of the measure.
                        try:
                            if int(total_on_duration) != 1:
                                # This means there is some space that was filled with dots.
                                duration = int(1 - total_on_duration)
                                extension.set_attr(note_to_extend, lineno, duration)
                            total_on_duration = 0
                        except Exception as err:
                            print("[ERROR] Line %d" % lineno)
                            raise err

        self.min_note = min_note
        self.max_note = max_note
        return soprano, alto, tenor, bass

    def to_numpy(self):
        pass

    def to_tensor(self):
        pass
