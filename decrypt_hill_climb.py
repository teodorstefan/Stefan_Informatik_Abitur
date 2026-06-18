import argparse
import random
import os 
from load_alphabet import load_alphabet
from decryption_fitness import _fitness, load_reference


def apply_key(ciphertext, alphabet, key):
    mapping = {key[i]: alphabet[i] for i in range(len(alphabet))}
    return ''.join(mapping.get(ch, ch) for ch in ciphertext)


def total_score(fitness):
    return fitness['2'] + fitness['3'] + fitness['4']


def decrypt_hill_climb(encrypted_text, alphabet, reference, ngram_size, restart_counter, max_no_improve=1000):
    key = alphabet[:]
    random.shuffle(key)

    best_text = apply_key(encrypted_text, alphabet, key)
    best_score = _fitness(best_text, ngram_size, reference)
    best_key = key[:]

    no_improve = 0
    iteration = 0

    print(f'Starting score: {best_score:.2f}%')

    while no_improve < max_no_improve:
        i, j = random.sample(range(len(key)), 2)
        key[i], key[j] = key[j], key[i]

        candidate_text = apply_key(encrypted_text, alphabet, key)
        candidate_score = _fitness(candidate_text, ngram_size, reference)

        if candidate_score > best_score:
            best_score = candidate_score
            best_text = candidate_text
            best_key = key[:]
            no_improve = 0
            print(f'\rattempt={restart_counter} | iter={iteration} | {ngram_size}-gramm={best_score:.2f}% \033[K',end='', flush=True)
        else:
            key[i], key[j] = key[j], key[i]
            no_improve += 1

        iteration += 1

    return best_key, best_text, best_score, restart_counter


def main(input_file, output_file, ngram_size, max_no_improve, restarts):
    base, extension = os.path.splitext(output_file)
    output_file = f"{base}_{ngram_size}-gramm{extension}"
    alphabet = load_alphabet()
    reference = load_reference(ngram_size)

    with open(input_file, 'r', encoding='utf-8') as f:
        encrypted_text = f.read()

    print(f'Alphabet: {len(alphabet)} chars | ngram_size={ngram_size} | max_no_improve={max_no_improve} | restarts={restarts}')

    best_key, best_text, best_score, restart_counter = None, None, -1, 0
    for restart in range(restarts):
        print(f'\n--- Restart {restart + 1}/{restarts} ---')
        key, text, score, _ = decrypt_hill_climb(
            encrypted_text, alphabet, reference, ngram_size, (restart + 1), max_no_improve
        )
        if score > best_score:
            best_key, best_text, best_score = key, text, score
            print(f'\n\nNew best score: {best_score:.2f}%')

    separator = '-' * 60
    result = (
        f'attempt:    \t{restart_counter}\n'
        f'best score: \t{best_score:.2f}\n'
        f'alphabet:   \t{" ".join(alphabet)}\n'
        f'key:        \t{" ".join(alphabet)}\n'
        f'mapped:     \t{" ".join(best_key)}\n'
        f'{separator}\n'
        f'{best_text}\n'
        f'{separator}\n'
    )
    print(f'\n\nResult:\n{result}')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'Exported -> {output_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monoalphabetic cipher hill-climbing decryption')
    parser.add_argument('-i', '--input', required=True, help='path to encrypted file')
    parser.add_argument('-o', '--output', default='../data_sources/decrypted_hill_climb.txt', help='path to output file')
    parser.add_argument('-n', '--max-no-improve', type=int, default=1000, help='stop after N iterations without improvement')
    parser.add_argument('-s', '--ngram-size', type=int, default=3, help='size of n-grams to use for fitness evaluation')
    parser.add_argument('-r', '--restarts', type=int, default=5, help='number of restarts from different random keys')
    args = parser.parse_args()
    main(args.input, args.output, args.ngram_size, args.max_no_improve, args.restarts)
