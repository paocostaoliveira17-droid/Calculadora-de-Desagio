# Calculadora de Juros Simples

# ==========================================================
# Calculadora de Empréstimo com Juros Simples + Tarifas Fixas
# - Prazo em dias (convertido para meses)
# - Juros e tarifas descontados antecipadamente
# - Mostra valor nominal, líquido e lucro total
# Autor: ChatGPT (GPT-5)
# ==========================================================

def juros_simples(capital, taxa_mensal, dias):
    """Calcula juros simples convertendo dias em meses (30 dias = 1 mês)"""
    meses = dias / 30
    juros = capital * taxa_mensal * meses
    return juros, meses

def calculadora_emprestimo_simples_dias():
    print("=== Calculadora de Empréstimo com Juros Simples (prazo em dias) ===\n")

    # Entradas do usuário
    valor_nominal = float(input("Digite o valor nominal do empréstimo (R$): "))
    taxa = float(input("Digite a taxa de juros ao mês (%): ")) / 100
    dias = float(input("Digite o prazo total do empréstimo (em dias): "))
    tarifa_total = float(input("Digite o valor total das tarifas fixas (R$): "))

    # --- Cálculo dos juros simples ---
    juros, meses = juros_simples(valor_nominal, taxa, dias)

    # --- Valor líquido (juros e tarifas descontados) ---
    valor_liquido = valor_nominal - juros - tarifa_total

    # --- Valor a pagar e lucro ---
    valor_a_pagar = valor_nominal
    lucro_total = valor_a_pagar - valor_liquido

    # --- Exibição dos resultados ---
    print("\n===== RESULTADOS =====")
    print(f"Valor nominal (emprestado): R$ {valor_nominal:,.2f}")
    print(f"Valor líquido recebido pelo tomador: R$ {valor_liquido:,.2f}")
    print(f"Valor total a pagar no final: R$ {valor_a_pagar:,.2f}")
    print(f"Lucro total (juros + tarifas): R$ {lucro_total:,.2f}")

    print("\n=== Detalhamento ===")
    print(f"→ Prazo total: {dias:.0f} dias ({meses:.2f} meses)")
    print(f"→ Taxa de juros simples: {taxa * 100:.2f}% ao mês")
    print(f"→ Juros acumulados: R$ {juros:,.2f}")
    print(f"→ Tarifas fixas descontadas: R$ {tarifa_total:,.2f}")

# Executar o programa
if __name__ == "__main__":
    calculadora_emprestimo_simples_dias()
