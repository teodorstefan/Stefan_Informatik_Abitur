import argparse
from load_alphabet import load_alphabet
from decryption_fitness import decryption_fitness, load_reference as _load_reference


def decrypt_ceasar(encrypted_text, alphabet):
    index = {ch: i for i, ch in enumerate(alphabet)}
    n = len(alphabet)
    results = []

    for shift in range(n):
        decrypted = ''.join(
            alphabet[(index[ch] - shift) % n] if ch in index else ch
            for ch in encrypted_text
        )
        results.append((shift, decrypted))

    return results


def main(input_file, output_file):
    alphabet = load_alphabet()

    with open(input_file, 'r', encoding='utf-8') as f:
        encrypted_text = f.read()

    results = decrypt_ceasar(encrypted_text, alphabet)

    ref2 = _load_reference(2)
    ref3 = _load_reference(3)
    ref4 = _load_reference(4)
    scored = sorted(
        [(shift, text, decryption_fitness(text, ref2=ref2, ref3=ref3, ref4=ref4)) for shift, text in results],
        key=lambda x: (x[2]['2'] + x[2]['3'] + x[2]['4']),
        reverse=False
    )

    separator = '-' * len(encrypted_text) * 2
    simple_separator = ':' * 10
    print(f'\nDecryped Ceasar\nGenerated {len(scored)} possible decryptions to {output_file}\n{separator}')
    with open(output_file, 'w', encoding='utf-8') as f:
        for shift, text, fitness in scored:
            line = f'\n{separator}\nshift={shift} | 2-gramm={fitness["2"]:.2f}% | 3-gramm={fitness["3"]:.2f}% | 4-gramm={fitness["4"]:.2f}%\n{simple_separator}\n{text}\n{separator}'
            print(line)
            f.write(line)

    print(f'\nExported {len(scored)} results -> {output_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brute-force Caesar decryption for all shifts')
    parser.add_argument('-i', '--input', required=True, help='path to encrypted file')
    parser.add_argument('-o', '--output', default='../data_sources/decrypted_ceasar.txt', help='path to output file')
    args = parser.parse_args()
    main(args.input, args.output)
