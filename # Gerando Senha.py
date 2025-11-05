# Gerando Senha
import random
import string

def gerar_senha(tam=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(tam))
    return senha

print('Gerador de Senhas')
tamanho = int(input('Digite o tamanho da senha que deseja: '))
if tamanho < 8:
    print('O tamanho mínimo é 8. Vamos criar uma senha com 8 caracteres')
    tamanho = 8

senha_gerada = gerar_senha(tamanho)
print(f'Sua senha gerada é: {senha_gerada}')