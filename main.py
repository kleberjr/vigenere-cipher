import string
from unicodedata import normalize, category
from vigenere import cifraDeVigenere

# funcao auxiliar de leitura de arquivo para quebra da cifra de vigenere por analise de frequencia
def read_file():
    filename = input('Digite o nome do arquivo que esta contida a mensagem (o arquivo tem que esta na pasta /Testes).\n>>> ')
    try:
        with open(f'Testes/{filename}', encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f'ERRO: O arquivo {filename} nao existe')
        return None

# funcao auxiliar que transforma os caracteres em maiusculas, alem de eliminar os espacos, pontuacoes e numeros
def sanitize(msg): 
    msg = msg.replace(' ','')
    msg = ''.join([i for i in msg if not i.isdigit()])
    msg = msg.translate(str.maketrans('','', string.punctuation))
    msg = ''.join(char for char in normalize('NFD', msg) if category(char) != 'Mn')
    msg = msg.upper()

    return msg

# Alinha a chave com o texto para garantir que cada caractere do texto original seja cifrado com algum caractere
def get_keystream(msg, key):
    key = list(key)

    if len(msg) == len(key): 
        return(key) 
    
    for i in range(len(msg) - len(key)): 
        key.append(key[i % len(key)]) 
    
    return("".join(key)) 

# cifra a mensagem
def cipher(msg, key):
    ciphered_msg = []

    msg = sanitize(msg)
    keystream = sanitize(get_keystream(msg, key))

    for idx, char in enumerate(msg):
        # (Pi + Ki) % tamanho do alfabeto
        char_pos = (letter_to_number[char] + letter_to_number[keystream[idx]]) % len(alphabet)
        # Pega a letra correspondente a do texto cifrado
        ciphered_msg.append(number_to_letter[char_pos])
    
    return("".join(ciphered_msg))

# decrifra a mensagem
def decipher(ciphered_msg, key):
    original_msg = []
    gaps = 0

    ciphered_msg = sanitize(ciphered_msg)
    keystream = sanitize(get_keystream(ciphered_msg, key))

    for idx, char in enumerate(ciphered_msg):
        if char not in alphabet:
            original_msg.append(char)
            gaps += 1
            continue

        # (Pi - Ki) % tamanho do alfabeto
        number = (letter_to_number[char] - letter_to_number[keystream[(idx - gaps) % len(keystream)]]) % len(alphabet)
        # Pega a letra correspondente a do texto original
        original_msg.append(number_to_letter[number])
    
    return("".join(original_msg))

vigenere = cifraDeVigenere()

if __name__ == "__main__":
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # The zip function return tuples like ('A', 0), ('B', 1)... 
    letter_to_number = dict(zip(alphabet, range(len(alphabet))))
    number_to_letter = dict(zip(range(len(alphabet)), alphabet))

    while True:
        print("===================================")
        print("[c] Cifrar\n[d] Decifrar\n[a] Atacar\n[s] Sair")
        print("===================================\n\n")
        
        action = (input(" > ")[0])
        
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

        elif action == "a":
            mensagem = read_file()
            if mensagem:
                language = input("A mensagem esta em portugues ou ingles (PT/EN)?\n>>> ")
                end = False

                while not end:
                    key_size = vigenere.key_size(mensagem)
                    keyword = vigenere.break_keyword(key_size, mensagem.upper(), language)

                    print("Palavra-chave obtida: ", keyword)
                    print("Mensagem decriptografada:")
                    print(vigenere.crypt_decrypt(keyword, mensagem, 'D'))

                    ans = input("Deseja refazer o ataque com outro tamanho de chave (S/N)?\n>>> ")
                    end = (True if ans.upper() == 'N' else False)

        elif action == "s":
            break
        else:
            print("Opção inválida! Digite uma entrada válida\n")

        input()