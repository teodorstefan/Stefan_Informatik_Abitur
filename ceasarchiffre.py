import string

original_text = str(input("Verschluesseln sie einen Text"))

shift = int(input("Bitte nenne sie einen Verschiebungswert")) % 26
#ändere Später zu einer Variable die man eintippen kann
alphabet = string.ascii_letters

shifted = alphabet[shift:] + alphabet[:shift]

table = str.maketrans(alphabet,shifted)

encrypted = original_text.translate(table)

print(encrypted)