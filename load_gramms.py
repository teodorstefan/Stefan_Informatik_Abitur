def load_gramms(gramm_length=3):
    with open('../data_sources/gramms.txt', 'r', encoding='utf-8') as f:
        gramms = {}
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                gramms[parts[0]] = float(parts[1])
    return gramms