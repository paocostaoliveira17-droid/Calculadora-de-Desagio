# Calculadora online 

import streamlit as st

# Título
st.title("Calculadora de Juros Compostos")

# Entradas do usuário
valor_nominal = st.number_input("Valor nominal (R$)", min_value=0.0, value=1000.0, step=100.0)
taxa = st.number_input("Taxa de juros ao mês (%)", min_value=0.0, value=5.0, step=0.1) / 100
dias = st.number_input("Prazo total (dias)", min_value=1, value=45, step=1)
tarifa_total = st.number_input("Tarifas fixas (R$)", min_value=0.0, value=20.0, step=1.0)

# Conversão de dias para meses
meses = dias / 30

# Juros compostos
juros = valor_nominal * ((1 + taxa) ** meses - 1)

# Valor líquido
valor_liquido = valor_nominal - juros - tarifa_total
lucro_total = valor_nominal - valor_liquido

# Resultados
st.subheader("Resultados")
st.write(f"Valor nominal: R$ {valor_nominal:,.2f}")
st.write(f"Valor líquido recebido: R$ {valor_liquido:,.2f}")
st.write(f"Lucro total (juros + tarifas): R$ {lucro_total:,.2f}")
st.write(f"Juros acumulados: R$ {juros:,.2f}")
st.write(f"Tarifas fixas: R$ {tarifa_total:,.2f}")
st.write(f"Prazo em meses: {meses:.2f}")
