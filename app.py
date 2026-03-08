import streamlit as st

def calcular_pressao_mulequim(temp):
    # Lógica baseada na sua classe de controle
    if temp >= 40.0:
        proporcao = int(temp) - 40
        pressao = 1880 + (proporcao * 7)
    elif temp >= 30.0:
        proporcao = int(temp) - 30
        pressao = 1810 + (proporcao * 7)
    elif temp >= 20.0:
        proporcao = int(temp) - 20
        pressao = 1740 + (proporcao * 7)
    elif temp >= 10.0:
        proporcao = int(temp) - 10
        pressao = 1660 + (proporcao * 8)
    elif temp >= 0.0:
        proporcao = int(temp) - 0
        pressao = 1610 + (proporcao * 5)
    elif temp >= -10.0:
        proporcao = (int(temp) * -1) - 0
        pressao = 1610 - (proporcao * 7)
    elif temp >= -20.0:
        proporcao = (int(temp) * -1) - 10
        pressao = 1540 - (proporcao * 7.5) # Mantendo o cálculo da sua classe
    elif temp >= -30.0:
        proporcao = (int(temp) * -1) - 20
        pressao = 1465 - (proporcao * 7)
    else: # -40.0 até -30.0
        proporcao = (int(temp) * -1) - 30
        pressao = 1395 - (proporcao * 7)
        
    return pressao

st.set_page_config(page_title="Check Porta VC-1", page_icon="✈️")
st.title("✈️ Check Porta VC-1")

temp_input = st.number_input("Digite a temperatura (°C):", value=20.0, step=0.1)

if st.button("Calcular Limites"):
    if -40 <= temp_input <= 50:
        pressao_ideal = calcular_pressao_mulequim(temp_input)
        
        # Margem de +- 5%
        minimo = pressao_ideal * 0.95
        maximo = pressao_ideal * 1.05
        
        st.write("---")
        st.metric("Pressão Nominal Calculada", f"{pressao_ideal:.1f} PSI")
        
        col1, col2 = st.columns(2)
        col1.metric("Mínimo (-5%)", f"{minimo:.1f} PSI")
        col2.metric("Máximo (+5%)", f"{maximo:.1f} PSI")
        
        st.info(f"Faixa de trabalho: {minimo:.1f} a {maximo:.1f} PSI")
    else:
        st.error("Erro: Insira uma temperatura entre -40°C e +50°C.")

st.caption("Sistema de verificação de portas para o VC-1. Software não oficial desenvolvido por 2S MIGUEL.")
