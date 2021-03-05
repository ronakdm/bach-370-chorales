from bach_chorale import BachChorale

for i in range(2):
    file_path = f"kern/chor00{i+1}.krn"
    c = BachChorale(file_path)
    print(c.key_signature)
    print(c.time_signature)
