from bach_chorale import BachChorale
import numpy as np
import torch
import pickle

num_chorales = 371
min_note = np.inf
max_note = -np.inf
total_len = 0

chorales = []
for i in range(num_chorales):
    # For some reason, Chorale 150 does not exist. ¯\_(ツ)_/¯
    # Chorales 86, 195, 247, 305 seems to have been annotated slightly wrong,
    # or have something in the soprano line that I cannot parse.
    if i + 1 not in [150, 86, 195, 247, 305]:
        try:
            file_path = f"kern/chor{i+1:03d}.krn"
            chorale = BachChorale(file_path)

            min_note = min(min_note, chorale.min_note)
            max_note = max(max_note, chorale.max_note)
            total_len += chorale.len

            chorales.append(chorale)

        except Exception as err:
            print(f"[Chorale {i+1}]")
            raise err

print("Total chorale length (in 16th notes):", total_len)
print("Minimum midi code:", min_note)
print("Maximum midi code:", max_note)

pickle.dump(chorales, open("chorales.p", "wb"))

chorales = pickle.load(open("chorales.p", "rb"))

# Midi codes for a piano go from 21-108,
# So we make the tensor indexable with actual midi code.
# See https://newt.phys.unsw.edu.au/jw/notes.html
num_pitches = 108 + 1

# Length is length of each sequence plus the "end of sentence" token.
chorales_tensor = torch.zeros(
    4, num_pitches, total_len + len(chorales), dtype=torch.int32
)
index = 0
for i, chorale in enumerate(chorales):
    try:
        chorales_tensor[:, :, index : index + (chorale.len + 1)] = chorale.to_tensor(
            num_pitches
        )
        index += chorale.len + 1
    except Exception as err:
        print("Bass length:", chorale.bass.len)
        print("Tenor length:", chorale.tenor.len)
        print("Alto length:", chorale.alto.len)
        print("Soprano length:", chorale.soprano.len)
        print(f"[Chorale {chorale.number}]")
        raise err

pickle.dump(chorales_tensor, open("chorales_tensor.p", "wb"))

