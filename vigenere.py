import string as s

class Vigenere():

    def __init__(self) -> None:
        self.alphabet = list(s.ascii_uppercase)
        self.eng_probabilities = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
        self.pt_probabilities = [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]

    def key_pattern(self, key, text):
        if not all(c.upper() in self.alphabet for c in key):
            raise ValueError('Chave inválida')
        if len(key) > len(text):
            return key[:len(text)] 

        new_key = ""
        i = 0

        for _ in text:
            new_key += key[i]
            i = (i + 1) % len(key)

        return new_key.upper()

    def crypt_decrypt(self, key, text, option):
        if option == 'C' and (len(text) <= 0 or len(key) < 2):
            raise ValueError('Tamanho do texto ou da chave inválido')
        elif option == 'D' and (len(text) <= 0 or len(key) < 1):
            raise ValueError('Tamanho do texto ou da chave inválido')

        if option != 'C' and option != 'D':
            raise ValueError('Opção inválida!')

        text = text.upper()
        new_key = self.key_pattern(key, text)
        text_ans = ""
        i = 0

        for letter in text:
            if letter in self.alphabet:
                if option == 'C': 
                    text_ans += self.alphabet[((ord(letter) + ord(new_key[i])) % 26)]
                else:
                    text_ans += self.alphabet[(ord(letter) - ord(new_key[i]) % 26 + 26) % 26]
                i += 1
            else:
                text_ans += letter

        return text_ans


    def clean_text(self, text):
        text_ans = ""
        for letter in text:
            if letter.upper() in self.alphabet:
                text_ans += letter
        return text_ans
        
    def key_size(self, text):
        text = self.clean_text(text)
        spacing = []
    
        for i in range(len(text)-2):
            trigram = text[i] + text[i+1] + text[i+2]
            for j in range(i+1, len(text)-2):
                aux = text[j] + text[j+1] + text[j+2]
                if aux == trigram:
                    spacing.append((trigram, j-i))
        
        spacing = list(set(spacing))

        freq_mod = {}

        for _, space in spacing:
            for i in range(2,21):
                if space % i == 0: 
                    freq_mod[i] = freq_mod.get(i, 0) + 1
        
        key_size = (0,0)

        freq_mod = dict(sorted(freq_mod.items(), key=lambda item: item[0]))

        print("Tamanhos de chave possiveis: ")
        for key, value in freq_mod.items():
            if value >= key_size[1]:
                key_size = (key,value)
            print("Tamanho:", key, "-- Quantidade:", value)

        print("Tamanho provavel da chave: ", key_size[0]) 
        ans = input("Voce deseja continuar com esse tamanho da chave? (S/N)\n>>> ")  
        if ans.lower() == 'n':
            aux = int(input("Digite o tamanho da chave desejado (entre 2 e 20).\n>>> "))
            while aux > 20 or aux < 2:
                aux = int(input("Tamanho Invalido. Digite um numero entre 2 e 20.\n>>> "))
            return aux
        
        return key_size[0]

    def discover_letter(self, probability, language):
        letter = ''
        tot_diff = 1e9

        for i in range(26):
            aux_diff = 0
            for j in range(26):
                if language == 'EN':
                    aux_diff += abs(probability[(i+j) % 26] - self.eng_probabilities[j]);             
                else:
                    aux_diff += abs(probability[(i+j) % 26] - self.pt_probabilities[j]); 

            if aux_diff < tot_diff:
                letter = self.alphabet[i]
                tot_diff = aux_diff

        return letter

    def break_keyword(self, key, text, language):
        text = self.clean_text(text)
        keyword = ""

        for i in range(key):
            total = 0
            frequency_text = {}
            probability_text = []
            for j in range(i, len(text), key):
                frequency_text[text[j]] = frequency_text.get(text[j], 0) + 1
                total += 1

            for letter in self.alphabet:
                aux = frequency_text.get(letter, 0)/total*100
                probability_text.append(aux)

            keyword += self.discover_letter(probability_text, language)
            
        return keyword
