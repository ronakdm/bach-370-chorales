from bach_chorale import BachChorale
import numpy as np

num_chorales = 371
min_note = np.inf
max_note = -np.inf

chorales = []
for i in range(num_chorales):
    # For some reason, Chorale 150 does not exist. ¯\_(ツ)_/¯
    if i != 149:
        try:
            file_path = f"kern/chor{i+1:03d}.krn"
            chorale = BachChorale(file_path)

            min_note = min(min_note, chorale.min_note)
            max_note = max(max_note, chorale.max_note)

            chorales.append(chorale)
        except Exception as err:
            print(f"[Chorale {i+1}]")
            raise err

print(min_note)
print(max_note)

