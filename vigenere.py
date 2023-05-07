import string as s

class cifraDeVigenere():

    # instanciacao de constantes utilizadas na analise de frequencia
    def __init__(self) -> None:
        self.alphabet = list(s.ascii_uppercase)
        self.prob_ingles = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
        self.prob_ptbr = [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]

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

    # funcao utilizada para criptografar ou descriptografar uma mensagem, dada uma chave
    def crypt_decrypt(self, key, text, option):
        if option == 'C' and (len(text) <= 0 or len(key) < 2):
            raise ValueError('Tamanho do texto ou da chave inválido')
        elif option == 'D' and (len(text) <= 0 or len(key) < 1):
            raise ValueError('Tamanho do texto ou da chave inválido')

        if option != 'C' and option != 'D':
            raise ValueError('Opção inválida!')

        text = text.upper()
        new_key = self.key_pattern(key, text)
        ans = ""
        i = 0

        for letter in text:
            if letter in self.alphabet:
                if option == 'C': 
                    ans += self.alphabet[((ord(letter) + ord(new_key[i])) % 26)]
                else:
                    ans += self.alphabet[(ord(letter) - ord(new_key[i]) % 26 + 26) % 26]
                i += 1
            else:
                ans += letter

        return ans

    # funcao auxiliar para transformar os caracteres da mensagem em letras maiusculas
    def clean_text(self, text):
        text_ans = ""
        for letter in text:
            if letter.upper() in self.alphabet:
                text_ans += letter
        return text_ans

    # funcao criada para calcular todas as possiveis chaves de tamanhos variaveis entre 2 e 20 caracteres que podem (ou nao) quebrar a   
    def key_size(self, text):
        text = self.clean_text(text)
        spacing = []
    
        for i in range(len(text)-2):                                            # dois lacos for sao abertos para compatrar triades de caracteres e analisar a repeticao de simbolos no texto cifrado
            trigram = text[i] + text[i+1] + text[i+2]
            for j in range(i+1, len(text)-2):
                aux = text[j] + text[j+1] + text[j+2]
                if aux == trigram:                                             # caso exista semelhanca entre as triades analisadas,
                    spacing.append((trigram, j-i))                             # deve-se colocar a triade e a distancia em que se encontram no texto cifrado
        
        spacing = list(set(spacing))

        freq_mod = {}

        for _, space in spacing:
            for i in range(2,21):
                if space % i == 0:                                             # se a distancia entre as triades de caracteres estiverem a uma distancia que varia de 2 a 20 unidades,
                    freq_mod[i] = freq_mod.get(i, 0) + 1                       # aumenta-se a quantidade de chaves que tem um determinado tamanho i
        
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
    
    # funcao auxiliar para descobrir qual letra do alfabeto pode corresponder a letra cifrada, dadas as frequencias de uso de cada letra em uma determinada lingua
    def discover_letter(self, probability, language):
        letter = ''
        tot_diff = 1e9                                                                  # setando a diferenca entre as probabilidades de ocorrencia das letras do texto cifrado com a probabilidade das letras na lingua selecionada

        for i in range(26):                                                             # dois lacos 'for' sao abertos para analisar duas letras unidas do texto cifrado, e assim, realizar a estimativa de quais letras este padrao corresponde
            aux_diff = 0
            for j in range(26):
                if language == 'EN':
                    aux_diff += abs(probability[(i+j) % 26] - self.prob_ingles[j]);    # calculando a diferenca entre as probabilidades de ocorrencia das duas letras do texto cifrado com a probabilidade de ocorrencia das duas letras em ingles         
                else:
                    aux_diff += abs(probability[(i+j) % 26] - self.prob_ptbr[j]);      # calculando a diferenca entre as probabilidades de ocorrencia das duas letras do texto cifrado com a probabilidade de ocorrencia das duas letras em portugues 

            if aux_diff < tot_diff:                                                    # se a diferenca entre as probabilidades anteriormente calculadas for menor que a grande diferenca setada inicialmente,
                letter = self.alphabet[i]                                              # a letra correspondente eh atualizada
                tot_diff = aux_diff                                                    # e a diferenca total tambem

        return letter                                                                  # quando nao for mais possivel atualizar a letra em decorrencia da variavel aux_diff, temos a letra correspondente a letra analisada no texto cifrado

    # funcao auxiliar para descobrir a chave do texto cifrado
    def break_keyword(self, key, text, language):
        text = self.clean_text(text)                                            # transforma os caracteres da mensagem em letras maiusculas
        keyword = ""                                                            # inicializando a chave como uma string vazia, a ser construida

        for i in range(key):
            total = 0
            frequency_text = {}                                                 # mapa para armazenar a frequencia das letras da mensagem
            probability_text = []                                               # vetor auxiliar que armazena as frequencias de cada letra do texto cifrado, dado o tamanho do texto
            for j in range(i, len(text), key):
                frequency_text[text[j]] = frequency_text.get(text[j], 0) + 1    # armazena a frequencia de cada letra do texto cifrado em uma mapa - lista de frequencias
                total += 1

            for letter in self.alphabet:
                aux = frequency_text.get(letter, 0)/total*100                   # realizando o calculo da frequencia de cada letra do texto cifrado, dado o tamanho do texto
                probability_text.append(aux)                                    # e colocando essas frequencias em um vetor de frequencias

            keyword += self.discover_letter(probability_text, language)         # construcao da chave por analise de frequencia
            
        return keyword                                                          # retornando a chave descoberta por analise de frequencia para descriptografar a mensagem
