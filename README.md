# Implementação da Cifra de Vigenère

Este trabalho explora a cifra de Vigenère, tendo duas partes: o cifrado/decifrador e o ataque de recuperação de senha por análise de frequência.

## Membros
* Kléber Rodrigues da Costa Júnior - 200053680
* Maria Eduarda Carvalho Santos - 190092556

## Como executar o projeto

O projeto pode ser executado executando a seguinte linha de comando no terminal:

```python3 main.py```

### Parte I: cifrador/decifrador
O cifrador recebe uma senha e uma mensagem que é cifrada segundo a cifra de Vigenère, gerando um criptograma, enquanto o decifrador recebe uma senha e um criptograma que é decifrado segundo a cifra de Vigenère, recuperando uma mensagem.

### Parte II: ataque de recuperação de senha por análise de frequência
Serão fornecidas duas mensagens cifradas (uma em português e outra em inglês) com senhas diferentes. Cada uma das mensagens deve ser utilizada para recuperar a senha geradora do keystream usado na cifração e então decifradas.
