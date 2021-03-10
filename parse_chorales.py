from bach_chorale import BachChorale
import numpy as np
import torch
import pickle

num_chorales = 371
min_note = np.inf
max_note = -np.inf
max_len = 0

chorales = []
for i in range(num_chorales):
    # For some reason, Chorale 150 does not exist. ¯\_(ツ)_/¯
    if i != 149:
        try:
            file_path = f"kern/chor{i+1:03d}.krn"
            chorale = BachChorale(file_path)

            min_note = min(min_note, chorale.min_note)
            max_note = max(max_note, chorale.max_note)
            max_len = max(max_len, chorale.len)

            chorales.append(chorale)
        except Exception as err:
            print(f"[Chorale {i+1}]")
            raise err

print("Max chorale length (in 16th notes):", max_len)
print("Minimum midi code:", min_note)
print("Maximum midi code:", max_note)

# Midi codes for a piano go from 21-108,
# So we make the tensor indexable with actual midi code.
# See https://newt.phys.unsw.edu.au/jw/notes.html
num_pitches = 108 + 1
chorales_tensor = torch.zeros(num_chorales, 4, num_pitches, max_len, dtype=torch.int32)
for i, chorale in enumerate(chorales):
    try:
        chorales_tensor[i] = chorale.to_tensor(num_pitches, max_len)
    except Exception as err:
        print(f"[Chorale {i+1}]")
        raise err

pickle.dump(chorales_tensor, open("chorales_tensor.p", "wb"))

