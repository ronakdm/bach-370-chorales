from bach_chorale import BachChorale

# num_chorales = 371
num_chorales = 10

chorales = []
for i in range(num_chorales):
    try:
        file_path = f"kern/chor00{i+1}.krn"
        chorales.append(BachChorale(file_path))
    except Exception as err:
        print(f"[ERROR] Chorale {i+1}")
        raise err

