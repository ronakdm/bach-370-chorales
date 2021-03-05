from parser import KernParser, KernSpine, Note


class BachChorale:
    def __init__(self, file_path):

        self.parser = KernParser()

        with open(file_path, "r") as f:
            lines = f.readlines()

            self.title = self.parser.get_german_title(lines)
            self.key_signature = self.parser.get_key_signature(lines)
            self.time_signature = self.parser.get_time_signature(lines)
            self.soprano, self.alto, self.tenor, self.bass = self.get_data(lines)

    def get_data(self, lines):
        bass, tenor, alto, soprano = KernSpine(), KernSpine(), KernSpine(), KernSpine()
        for line in lines:
            if self.parser.is_data_record(line):
                note_strs = line.split()
                for i, spine in enumerate([bass, tenor, alto, soprano]):
                    spine.append(Note(note_strs[i]))

        return soprano, alto, tenor, bass

    def to_numpy(self):
        pass

    def to_tensor(self):
        pass
