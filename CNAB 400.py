from datetime import datetime

def gerar_linha_header(codigo_empresa, nome_empresa, data_geracao):
    return (
        '0' +                             # Código do registro
        '1' +                             # Tipo de operação (1 = Remessa)
        '2' +                             # Tipo de serviço (2 = Baixa)
        'REMESSA' +                       # Literal de remessa
        '01' +                            # Código do serviço
        'COBRANCA       ' +              # Literal do serviço
        f'{codigo_empresa:0>20}' +       # Código da empresa no banco
        f'{nome_empresa:<30}'[:30] +     # Nome da empresa
        '237' +                           # Código do banco (Bradesco)
        'BRADESCO       ' +              # Nome do banco
        data_geracao.strftime('%d%m%y') +# Data de geração
        ' ' * 294 +                      # Reservado
        '000001'                         # Número sequencial do registro
    )

def gerar_linha_detalhe(titulo, sequencial):
    return (
        '1' +                             # Código do registro
        f'{titulo["agencia"]:0>5}' +      # Agência do cedente
        '00' +                            # Zeros
        f'{titulo["conta"]:0>7}' +        # Conta do cedente
        f'{titulo["conta_dv"]}' +         # Dígito verificador da conta
        ' ' * 4 +                         # Reservado
        f'{titulo["nosso_numero"]:0>11}' +# Nosso número
        ' ' * 7 +                         # Reservado
        '01' +                            # Carteira
        ' ' * 4 +                         # Reservado
        f'{titulo["seu_numero"]:<10}'[:10] + # Seu número (número de controle do cedente)
        '000000' +                        # Data de vencimento fictícia
        '0000000000000' +                 # Valor fictício
        '237' +                           # Código do banco
        '00000' +                         # Agência cobradora
        '0' +                             # Dígito verificador
        '01' +                            # Espécie do título
        'N' +                             # Aceite
        datetime.now().strftime('%d%m%y')+ # Data de emissão
        '00' +                            # Instrução 1 (00 = sem instrução)
        '00' +                            # Instrução 2
        '000000' +                        # Juros de mora
        '000000' +                        # Data de desconto
        '0000000000000' +                 # Valor do desconto
        '0000000000000' +                 # Valor do IOF
        '0000000000000' +                 # Valor abatimento
        ' ' * 25 +                        # Identificação do pagador
        ' ' * 30 +                        # Nome do pagador
        ' ' * 10 +                        # Reservado
        ' ' * 40 +                        # Sacador/avalista
        ' ' * 12 +                        # Reservado
        f'{sequencial:0>6}'              # Número sequencial
    )

def gerar_linha_trailer(qtd_registros):
    return (
        '9' +                             # Código do registro
        ' ' * 393 +                       # Reservado
        f'{qtd_registros + 2:0>6}'       # Número sequencial (header + detalhes + trailer)
    )

def gerar_cnab400_baixa(boletos, codigo_empresa, nome_empresa, nome_arquivo):
    hoje = datetime.now()
    linhas = []

    # Header
    linhas.append(gerar_linha_header(codigo_empresa, nome_empresa, hoje))

    # Detalhes
    for idx, boleto in enumerate(boletos, start=2):
        linhas.append(gerar_linha_detalhe(boleto, idx))

    # Trailer
    linhas.append(gerar_linha_trailer(len(boletos)))

    # Escrever arquivo
    with open(nome_arquivo, 'w') as f:
        for linha in linhas:
            f.write(f'{linha:<400}'[:400] + '\r\n')

    print(f"Arquivo {nome_arquivo} gerado com sucesso.")

# --- Exemplo de uso:
boletos_para_baixa = [
    {
        "agencia": "0001",
        "conta": "123456",
        "conta_dv": "0",
        "nosso_numero": "12345678901",
        "seu_numero": "2561-1"
    },
    {
        "agencia": "1234",
        "conta": "56789",
        "conta_dv": "0",
        "nosso_numero": "12345678902",
        "seu_numero": "10002"
    }
]

gerar_cnab400_baixa(boletos_para_baixa, "12345678901234567890", "FIDC FACTIA", "cnab_baixa_4001.txt")

