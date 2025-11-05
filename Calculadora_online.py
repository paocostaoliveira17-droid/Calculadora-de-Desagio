# Calculadora Online
import streamlit as st

st.set_page_config(page_title="Calculadora de Deságio Utility", layout="centered")
st.title("Calculadora de Deságio Utility")


# Entradas
st.subheader("Dados do de Deságio")
valor_nominal = st.number_input("Valor nominal (R$)", min_value=0.0, value=1000.0, step=100.0)
taxa = st.number_input("Taxa de juros ao mês (%)", min_value=0.0, value=5.0, step=0.1) / 100
dias = st.number_input("Prazo total (dias)", min_value=1, value=45, step=1)
tarifa_total = st.number_input("Tarifas fixas (R$)", min_value=0.0, value=20.0, step=1.0)

# Conversão de dias para meses
meses = dias / 30

# Funções de cálculo
def calcular_juros_simples(capital, taxa, meses):
    return capital * taxa * meses

def calcular_juros_compostos(capital, taxa, meses):
    return capital * ((1 + taxa) ** meses - 1)

# Juros simples e compostos
juros_s = calcular_juros_simples(valor_nominal, taxa, meses)
juros_c = calcular_juros_compostos(valor_nominal, taxa, meses)


# Juros mistos ajustado

if dias < 30:
    # Prazo < 30 dias juros simples
    juros_misto = calcular_juros_simples(valor_nominal, taxa, meses)
    tipo_juros = "Simples (prazo < 30 dias)"
else:
    # Prazo >= 30 dias  juros compostos
    juros_misto = calcular_juros_compostos(valor_nominal, taxa, meses)
    tipo_juros = "Compostos (prazo ≥ 30 dias)"


# Valor líquido e lucro
valor_liquido_simples = valor_nominal - juros_s - tarifa_total
valor_liquido_composto = valor_nominal - juros_c - tarifa_total
valor_liquido_misto = valor_nominal - juros_misto - tarifa_total

lucro_simples = valor_nominal - valor_liquido_simples
lucro_composto = valor_nominal - valor_liquido_composto
lucro_misto = valor_nominal - valor_liquido_misto

# Resultados
st.subheader("Resultados")

st.markdown("### Juros Simples")
st.write(f"Valor líquido recebido pelo cedente: R$ {valor_liquido_simples:,.2f}")
st.write(f"Receita total (juros + tarifas): R$ {lucro_simples:,.2f}")
st.write(f"Juros simples acumulados: R$ {juros_s:,.2f}")

st.markdown("### Juros Compostos")
st.write(f"Valor líquido recebido pelo cedente: R$ {valor_liquido_composto:,.2f}")
st.write(f"Receita total (juros + tarifas): R$ {lucro_composto:,.2f}")
st.write(f"Juros compostos acumulados: R$ {juros_c:,.2f}")

st.markdown("### Juros Mistos (Simples <30d / Compostos ≥30d)")
st.write(f"Tipo de juros aplicado: {tipo_juros}")
st.write(f"Valor líquido recebido pelo cedente: R$ {valor_liquido_misto:,.2f}")
st.write(f"Lucro total (juros + tarifas): R$ {lucro_misto:,.2f}")
st.write(f"Juros mistos acumulados: R$ {juros_misto:,.2f}")


# Detalhamento-
st.subheader("Detalhamento do empréstimo")
st.write(f"Prazo total: {dias:.0f} dias ({meses:.2f} meses)")
st.write(f"Taxa de juros: {taxa*100:.2f}% ao mês")
st.write(f"Tarifas fixas descontadas: R$ {tarifa_total:,.2f}")

# Digitar no terminal : streamlit run Calculadora_online.py

