import string
from unicodedata import normalize, category

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# The zip function return tuples like ('A', 0), ('B', 1)... 
letter_to_number = dict(zip(alphabet, range(len(alphabet))))
number_to_letter = dict(zip(range(len(alphabet)), alphabet))

# Makes it uppercase and eliminates all spaces, numbers and punctuation.
def sanitize(msg): 
    msg = msg.replace(' ','')
    msg = ''.join([i for i in msg if not i.isdigit()])
    msg = msg.translate(str.maketrans('','', string.punctuation))
    msg = ''.join(char for char in normalize('NFD', msg) if category(char) != 'Mn')
    msg = msg.upper()

    return msg

# Repeats the key until it fits the text
def get_keystream(msg, key):
    key = list(key)

    if len(msg) == len(key): 
        return(key) 
    
    for i in range(len(msg) - len(key)): 
        key.append(key[i % len(key)]) 
    
    return("".join(key)) 

# Cipher a message based on Vigenère Cipher
def cipher(msg, key):
    ciphered_msg = []

    msg = sanitize(msg)
    keystream = sanitize(get_keystream(msg, key))

    for idx, char in enumerate(msg):
        # Operação (Pi + Ki) % tamanho do alfabeto
        char_pos = (letter_to_number[char] + letter_to_number[keystream[idx]]) % len(alphabet)
        # Pega a mensagem correspondente
        ciphered_msg.append(number_to_letter[char_pos])
    
    return("".join(ciphered_msg))


def decipher(ciphered_msg, key, alphabet):
    return "decipher"

if __name__ == "__main__":
    while True:
        print("===================================")
        print("[c] Cifrar\n[d] Decifrar\n[a] Atacar")
        print("===================================\n\n")
        
        action = input(" > ")[0]
        
        print("\n")

        if action == "c":
            msg = input("Insira a mensagem:\n  > ")
            key = input("Insira a chave:\n  > ")

            ciphered_msg = cipher(msg, key) 

            print("\n>> Mensagem cifrada:", ciphered_msg) 

        elif action == "d":
            ciphered_msg = input("Insira a mensagem:\n  > ")
            key = input("Insira a chave:\n  > ")

            original_msg = decipher(ciphered_msg, key) 

            print("\n>> Mensagem decifrada:", original_msg) 

        else:
            break

        input()