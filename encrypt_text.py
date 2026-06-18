import argparse
import random
from load_alphabet import load_alphabet


def log_alphabet(title,alphabet):
    # entries = ' '.join(f'{i}:{repr(ch)}' for i, ch in enumerate(alphabet))
    entries = ' '.join(alphabet)
    print(f'{title}: {len(alphabet)} entries')
    print(f'{entries}')


def shift_keys(alphabet, shift):
    n = len(alphabet)
    shift = shift % n
    return alphabet[shift:] + alphabet[:shift]


def shuffle_keys(alphabet):
    key = alphabet[:]
    random.shuffle(key)
    return key


def encrypt(text, alphabet, key):
    index = {ch: i for i, ch in enumerate(alphabet)}
    return ''.join(key[index[ch]] if ch in index else ch for ch in text)


def main(input_file, output_file, gramms_file=None, method='c', shift=3):
    alphabet = load_alphabet() if gramms_file is None else load_alphabet(gramms_file)
    separator = '-' * len(alphabet) * 2
    print(f'\n{separator}')
    method_name = 'Not defined'
    if method == 'c':
        key = shift_keys(alphabet, shift)
        method_name = 'Caesar'
    elif method == 'm':
        key = shuffle_keys(alphabet)
        method_name = 'Monoalphabetic'
    print(f'Encryption method: {method_name} | shift={shift if method=="c" else "N/A"}')
    print(f'{separator}')
    log_alphabet('Alphabet', alphabet)
    log_alphabet(f'{method_name} Key', key)
    print(f'{separator}\n')
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    encrypted = encrypt(text, alphabet, key)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted)

    print(f'Input:{input_file}\n{separator}\n{text}\n{separator}\n')
    print(f'Output:{output_file}\n{separator}\n{encrypted}\n{separator}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt text using Caesar or monoalphabetic cipher')
    parser.add_argument('-i', '--input', required=True, help='path to input text file')
    parser.add_argument('-o', '--output', required=True, help='path to output encrypted file')
    parser.add_argument('-m', '--method', choices=['c', 'm'], required=True, help='c=Caesar, m=monoalphabetic')
    parser.add_argument('-s', '--shift', type=int, default=3, help='shift amount for Caesar')
    args = parser.parse_args()
    main(args.input, args.output, None, args.method, args.shift)
