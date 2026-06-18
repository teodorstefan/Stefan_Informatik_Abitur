import argparse
import os
import re


def normalize_text(text):
    lines = []
    for line in text.splitlines():
        line = re.sub(r'^-\s+', '', line)
        line = re.sub(r' {2,}', ' ', line)
        lines.append(line)
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def normalize_texts(input_dir, output_file, min_paragraph_length=100):
    paragraphs = []
    for filename in sorted(os.listdir(input_dir)):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        normalized = normalize_text(content)
        for p in normalized.split('\n\n'):
            p = p.strip().replace('\n', ' ')
            if len(p) >= min_paragraph_length:
                paragraphs.append(p)

    combined = ' '.join(paragraphs)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined)

    print(f'Wrote {len(paragraphs)} paragraphs to {output_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Normalize and combine text files')
    parser.add_argument('-i', '--input', type=str, default='../data_sources/dictionary', help='path to input directory')
    parser.add_argument('-o', '--output', type=str, default='../data_sources/training_text.txt', help='path to output file')
    parser.add_argument('-m', '--min-length', type=int, default=100, help='minimum paragraph length in characters')
    args = parser.parse_args()
    normalize_texts(args.input, args.output, args.min_length)
