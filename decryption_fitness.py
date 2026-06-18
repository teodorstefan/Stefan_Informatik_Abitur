import csv
from generate_gramms import count_gramms, generate_output_file_path

def load_reference(length):
    ref = {}
    with open(generate_output_file_path(length), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) >= 3:
                ref[row[0]] = float(row[2])
    return ref


def _fitness(text, length, reference):
    counts = count_gramms(text, length)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    known = sum(count for gramm, count in counts.items() if gramm in reference)
    return round(known / total * 100, 2)


def decryption_fitness(text, ref2=None, ref3=None, ref4=None):
    if ref2 is None:
        ref2 = load_reference(2)
    if ref3 is None:
        ref3 = load_reference(3)
    if ref4 is None:
        ref4 = load_reference(4)
    return {
        '2': _fitness(text, 2, ref2),
        '3': _fitness(text, 3, ref3),
        '4': _fitness(text, 4, ref4)
    }
