# Calculadora de Juros Compostos

def juros_compostos(capital, taxa_mensal, meses):
    """Calcula juros compostos"""
    return capital * ((1 + taxa_mensal) ** meses - 1)

def calculadora_emprestimo_composto_dias():
    print("=== Calculadora de Empréstimo com Juros Compostos (prazo em dias) ===\n")

    # Entradas do usuário
    valor_nominal = float(input("Digite o valor nominal do empréstimo (R$): "))
    taxa = float(input("Digite a taxa de juros ao mês (%): ")) / 100
    dias = float(input("Digite o prazo total do empréstimo (em dias): "))
    tarifa_total = float(input("Digite o valor total das tarifas fixas (R$): "))

    # Conversão do prazo para meses
    meses = dias / 30

    # Cálculo dos juros compostos 
    juros = juros_compostos(valor_nominal, taxa, meses)

    # Valor líquido recebido pelo tomador
    valor_liquido = valor_nominal - juros - tarifa_total

    # Valor a pagar e lucro total 
    valor_a_pagar = valor_nominal
    lucro_total = valor_a_pagar - valor_liquido

    # Exibição dos resultados
    print("\n===== RESULTADOS =====")
    print(f"Valor nominal (emprestado): R$ {valor_nominal:,.2f}")
    print(f"Valor líquido recebido pelo tomador: R$ {valor_liquido:,.2f}")
    print(f"Valor total a pagar no final: R$ {valor_a_pagar:,.2f}")
    print(f"Lucro total (juros + tarifas): R$ {lucro_total:,.2f}")

    print("\n=== Detalhamento ===")
    print(f"→ Prazo total: {dias:.0f} dias ({meses:.2f} meses)")
    print(f"→ Taxa de juros composta: {taxa * 100:.2f}% ao mês")
    print(f"→ Juros compostos acumulados: R$ {juros:,.2f}")
    print(f"→ Tarifas fixas descontadas: R$ {tarifa_total:,.2f}")

# Executar o programa
if __name__ == "__main__":
    calculadora_emprestimo_composto_dias()