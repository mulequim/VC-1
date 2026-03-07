import streamlit as st

# Tabela baseada na sua foto
def get_pressao_nominal(temp):
    dados = {
        50: 1950, 40: 1880, 30: 1810, 20: 1740, 10: 1660,
        0: 1610, -10: 1540, -20: 1465, -30: 1395, -40: 1325
    }
    return dados.get(temp)

st.set_page_config(page_title="Check Porta VC-1", page_icon="✈️")
st.title("✈️ Check Porta VC-1")
st.subheader("Verificação de Pressão")

# Entrada da temperatura
temp_input = st.number_input("Digite a temperatura (°C):", value=20, step=1, min_value=-40, max_value=50)

if st.button("Calcular Limites"):
    pressao = get_pressao_nominal(temp_input)
    
    if pressao:
        tolerancia = pressao * 0.05
        minimo = pressao - tolerancia
        maximo = pressao + tolerancia
        
        st.write(f"---")
        st.metric("Pressão Nominal", f"{pressao} PSI")
        
        col1, col2 = st.columns(2)
        col1.metric("Mínimo (-5%)", f"{minimo:.0f} PSI")
        col2.metric("Máximo (+5%)", f"{maximo:.0f} PSI")
        
        st.info(f"Intervalo de segurança: {minimo:.0f} a {maximo:.0f} PSI")
    else:
        st.error("Temperatura não encontrada na tabela.")

st.caption("Desenvolvido por Miguel - Software ñ Oficial.")
