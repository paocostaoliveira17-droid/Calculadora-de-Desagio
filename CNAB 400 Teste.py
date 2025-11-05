from datetime import datetime

# --- Configurações / constantes específicas do Bradesco ---
CODIGO_BANCO = "237"
CARTEIRA = "09"  # exemplo, pode variar conforme convênio cadastrado no Bradesco
CONVENIO = "12345678901234567890"  # código do convênio que o Bradesco informa
AGENCIA = "1234"
AGENCIA_DV = "0"
CONTA = "1234567"
CONTA_DV = "0"
NOME_EMPRESA = "Minha Empresa LTDA"
NOME_BANCO = "BRADESCO"
TIPO_SERVICO = "01"  # cobrança
LITERAL_SERVICO = "COBRANCA"
VERSAO_REMESSA_SEQ = 1  # numero de remessa sequencial

# --- Funções de geração de remessa ---

def gerar_header(remessa_seq):
    data_arquivo = datetime.now().strftime('%d%m%y')  # ou ddmmaa conforme manual
    header = ''
    header += '0'                                   # posição 1: registro header
    header += '1'                                   # posição 2: identificacao do arquivo remessa
    header += 'REMESSA'.ljust(7)                    # literal “REMESSA” posições 3 a 9
    header += TIPO_SERVICO                          # posições 10-11
    header += LITERAL_SERVICO.ljust(15)             # pos 12-26
    header += CONVENIO.rjust(20, '0')               # pos 27-46 => código da empresa / convênio :contentReference[oaicite:5]{index=5}
    header += NOME_EMPRESA.ljust(30)                 # pos 47-76 => nome da empresa
    header += CODIGO_BANCO                         # pos 77-79
    header += NOME_BANCO.ljust(15)                   # pos 80-94
    header += data_arquivo                          # pos 95-100 => data da gravação do arquivo :contentReference[oaicite:6]{index=6}
    header += ' ' * 8                               # pos 101-108 (brancos/conforme layout)
    # número sequencial de remessa no header
    header += str(remessa_seq).rjust(7, '0')        # pos 109-115 aprox – ajustar posição conforme manual
    header += ' ' * (400 - len(header) - 6)         # deixa espaço até os últimos 6 caracteres
    header += '000001'                              # sequencial de registro header = 1 no primeiro
    assert len(header) == 400, f"Header tem {len(header)} caracteres"
    return header

def gerar_detalhe(item, seq):
    """
    item: dict com chaves como:
        nosso_numero (str),
        documento (str),
        vencimento (datetime),
        valor (float),
        sacado_nome (str),
        sacado_documento (CPF/CNPJ),
        ocorrencia (codigo inicial ou zero),
        juros_mora, multa, desconto etc.
    seq: número sequencial do detalhe (registro).
    """
    detalhe = ''
    detalhe += '1'                                   # registro detalhe tipo 1
    detalhe += CODIGO_BANCO                         # pos 2-4
    # posições para agência, conta, convênio etc
    detalhe += AGENCIA.rjust(5, '0')                 # agência beneficiária
    detalhe += AGENCIA_DV                           # dígito verificador agência, se aplicável
    detalhe += CONTA.rjust(12, '0')                  # conta beneficiária
    detalhe += CONTA_DV                              # digito da conta
    # Nosso número conforme layout, preencher posições definidas
    detalhe += item['nosso_numero'].rjust(11, '0')   # exemplo de campo “Nosso Número” sem dígito verificador
    # outros campos fixos / variáveis:
    detalhe += item['documento'].ljust(15)           # número do documento de cobrança
    detalhe += item['vencimento'].strftime('%d%m%y') # data de vencimento
    valor_centavos = int(round(item['valor'] * 100))
    detalhe += f"{valor_centavos:013d}"             # valor do título sem ponto ou vírgula
    # continue preenchendo outros campos do layout do Bradesco:
    # espécie do título, aceite, data de emissão
    detalhe += item.get('especie', '02')             # por exemplo
    detalhe += item.get('aceite', 'N')                # N ou A
    detalhe += datetime.now().strftime('%d%m%y')     # data de emissão
    # instruções (juros, multa, descontos) nos campos apropriados
    # exemplo: juros mora
    detalhe += item.get('juros_mora_codigo', '0')      # código de juros mora
    detalhe += item.get('juros_mora_data', '000000')    # se necessário
    detalhe += item.get('juros_mora_valor', '0000000000000')  # etc
    # desconto
    detalhe += item.get('desconto_codigo', '0')
    detalhe += item.get('desconto_data', '000000')
    detalhe += item.get('desconto_valor', '0000000000000')
    # preenchimentos de campos restantes até sacado
    detalhe += item['sacado_nome'].ljust(30)
    detalhe += item.get('sacado_documento','').rjust(14, '0')  # CPF ou CNPJ
    # mais campos de endereço ou complemento se exigido
    detalhe += ' ' * (400 - len(detalhe) - 6)
    detalhe += f"{seq:06d}"                          # número sequencial do detalhe
    assert len(detalhe) == 400, f"Detalhe tem {len(detalhe)} caracteres"
    return detalhe

def gerar_trailer(total_registros, remessa_seq):
    trailer = ''
    trailer += '9'
    # muitos campos brancos ou zeros conforme layout
    trailer += ' ' * (400 - len(trailer) - 6)
    trailer += f"{remessa_seq:06d}"
    assert len(trailer) == 400, f"Trailer tem {len(trailer)} caracteres"
    return trailer

# --- Leitura de retorno Bradesco CNAB 400 ---

def ler_retorno_bradesco(caminho_arquivo):
    registros = []
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            if len(linha) < 400:
                linha = linha.rstrip('\n')
                # algumas vezes pode haver quebra; você pode validar ou ignorar essas linhas
            tipo = linha[0]
            if tipo == '1':  # detalhe
                # Exemplos de posições: (essas posições são apenas ilustrativas; validar no manual)
                nosso_numero = linha[62:73].strip()  # exemplo de posição do nosso número no retorno Bradesco :contentReference[oaicite:7]{index=7}
                valor_pago = int(linha[153:166]) / 100.0  # campo valor pago
                data_credito = linha[117:123]  # data de crédito ou liquidação
                ocorrencia = linha[108:110]    # código de ocorrência
                registros.append({
                    'nosso_numero': nosso_numero,
                    'valor_pago': valor_pago,
                    'data_credito': data_credito,
                    'ocorrencia': ocorrencia,
                    'linha': linha
                })
    return registros

# --- Função de conciliação entre remessa e retorno ---

def conciliacao(remessa_itens, retorno_itens):
    mapa = {item['nosso_numero']: item for item in remessa_itens}
    conciliados = []
    divergentes = []
    
    for ret in retorno_itens:
        nn = ret['nosso_numero']
        if nn in mapa:
            rem = mapa[nn]
            if abs(rem['valor'] - ret['valor_pago']) < 0.01:
                conciliados.append((rem, ret))
            else:
                divergentes.append((rem, ret, 'valor divergente'))
        else:
            divergentes.append((None, ret, 'não encontrado na remessa'))
    
    # Remessas que não retornaram
    for rem in remessa_itens:
        if rem['nosso_numero'] not in [r['nosso_numero'] for r in retorno_itens]:
            divergentes.append((rem, None, 'não apareceu no retorno'))
    
    return conciliados, divergentes

# --- Exemplo de uso ---

def exemplo():
    # montar remessa
    remessa_seq = VERSAO_REMESSA_SEQ
    remessa_itens = [
        {
            'nosso_numero': '00012345678',
            'documento': '0001',
            'vencimento': datetime(2025, 10, 30),
            'valor': 150.75,
            'sacado_nome': 'Fulano de Tal',
            'sacado_documento': '12345678901',
            # outros campos opcionais
        },
        {
            'nosso_numero': '00012345679',
            'documento': '0002',
            'vencimento': datetime(2025, 11, 10),
            'valor': 250.00,
            'sacado_nome': 'Beltrano Silva',
            'sacado_documento': '10987654321',
        }
    ]
    
    linhas = []
    linhas.append(gerar_header(remessa_seq))
    seq = 1
    for item in remessa_itens:
        linhas.append(gerar_detalhe(item, seq))
        seq += 1
    linhas.append(gerar_trailer(len(remessa_itens), remessa_seq))
    
    # grava arquivo remessa
    nome_arquivo = f"remessa_bradesco_cnab400_{remessa_seq}.txt"
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for l in linhas:
            f.write(l + '\n')
    print(f"Arquivo remessa gerado: {nome_arquivo}")
    
    