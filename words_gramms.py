import argparse
import csv


def generate_words_gramms(input_file, output_file):
    words = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for row in csv.reader(f, delimiter='\t'):
            if len(row) < 3:
                continue
            word, count = row[1].strip(), int(row[2].strip())
            words.append((word, count))

    total = sum(count for _, count in words)
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'count', 'percentage'])
        for word, count in words:
            writer.writerow([word, count, f'{count / total * 100:.4f}'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate gramms from word frequency list')
    parser.add_argument('-i', '--input', type=str, default='../data_sources/words/german-word-list-total.csv', help='path to word list CSV')
    parser.add_argument('-o', '--output', type=str, default='../data_sources/gramms/words_gramms.csv', help='path to output CSV')
    args = parser.parse_args()
    generate_words_gramms(args.input, args.output)
