import string

kryptografischer_text = str(input("Bitte schreiben Sie den zu entschluesselnden Text ein"))

alphabet = string.ascii_letters

for shift in range(0, -26, -1):
    shifted = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet,shifted)
    decrypted = kryptografischer_text.translate(table)
    print(decrypted)
    print("---")

