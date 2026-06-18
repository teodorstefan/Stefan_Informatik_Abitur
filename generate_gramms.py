import argparse
import csv
from collections import Counter
from pathlib import Path

def generate_output_file_path(length):
    return Path(__file__).parent.parent / 'data_sources' / 'gramms' / f'{length}_gramms.csv'

def count_gramms(text, length):
    counts = Counter()
    for i in range(len(text) - length + 1):
        counts[text[i:i+length]] += 1
    return counts


def write_gramms(counts, output):
    total = sum(counts.values())
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['gramm', 'count', 'percentage'])
        for gramm, count in counts.most_common():
            writer.writerow([gramm, count, f'{count / total * 100:.4f}'])


def generate_gramms(input, length):
    output_file_path = generate_output_file_path(length)
    with open(input, 'r', encoding='utf-8') as f:
        text = f.read()
    counts = count_gramms(text, length)
    write_gramms(counts, output_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate gramms for all the words in the dictionary')
    parser.add_argument('-i', '--input', type=str, default='../data_sources/normalized.txt', help='path to the normalized input file')
    parser.add_argument('-l', '--length', type=int, default=3, help='length of the gramms (2,3)')
    args = parser.parse_args()
    generate_gramms(args.input, args.length)