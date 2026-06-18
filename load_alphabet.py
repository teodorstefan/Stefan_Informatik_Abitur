import csv
from pathlib import Path

DEFAULT_GRAMMS = Path(__file__).parent.parent / 'data_sources' / 'gramms' / '1_gramms.csv'


def load_alphabet(gramms_file=DEFAULT_GRAMMS):
    chars = []
    with open(gramms_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and len(row[0]) == 1:
                chars.append(row[0])
    chars.sort()
    return chars
