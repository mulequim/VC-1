import streamlit as st
import numpy as np

# Função para encontrar a pressão exata via interpolação linear
def calcular_pressao(temp):
    # Temperaturas e Pressões da sua tabela
    temps = np.array([50, 40, 30, 20, 10, 0, -10, -20, -30, -40])
    press = np.array([1950, 1880, 1810, 1740, 1660, 1610, 1540, 1465, 1395, 1325])
    
    # Faz a interpolação linear
    return np.interp(temp, temps, press)

st.set_page_config(page_title="Check Porta VC-1", page_icon="✈️")
st.title("✈️ Check Porta VC-1")

# Entrada da temperatura (aceitando números decimais)
temp_input = st.number_input("Digite a temperatura (°C):", value=20.0, step=0.1)

if st.button("Calcular Limites"):
    if -40 <= temp_input <= 50:
        pressao_ideal = calcular_pressao(temp_input)
        tolerancia = pressao_ideal * 0.05
        
        minimo = pressao_ideal - tolerancia
        maximo = pressao_ideal + tolerancia
        
        st.write("---")
        st.metric("Pressão Ideal Calculada", f"{pressao_ideal:.1f} PSI")
        
        col1, col2 = st.columns(2)
        col1.metric("Mínimo (-5%)", f"{minimo:.1f} PSI")
        col2.metric("Máximo (+5%)", f"{maximo:.1f} PSI")
        
        st.info(f"Faixa de trabalho: {minimo:.1f} a {maximo:.1f} PSI")
    else:
        st.error("Erro: Insira uma temperatura entre -40°C e +50°C.")

st.caption("Sistema de verificação para o GTE.")
