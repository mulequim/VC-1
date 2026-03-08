import streamlit as st

# --- MÓDULO DE LÓGICA (Controllers) ---

def calcular_pressao_porta(temp):
    if temp >= 40.0: pressao = 1880 + ((int(temp) - 40) * 7)
    elif temp >= 30.0: pressao = 1810 + ((int(temp) - 30) * 7)
    elif temp >= 20.0: pressao = 1740 + ((int(temp) - 20) * 7)
    elif temp >= 10.0: pressao = 1660 + ((int(temp) - 10) * 8)
    elif temp >= 0.0: pressao = 1610 + (int(temp) * 5)
    elif temp >= -10.0: pressao = 1610 - (abs(int(temp)) * 7)
    elif temp >= -20.0: pressao = 1540 - ((abs(int(temp)) - 10) * 7.5)
    elif temp >= -30.0: pressao = 1465 - ((abs(int(temp)) - 20) * 7)
    else: pressao = 1395 - ((abs(int(temp)) - 30) * 7)
    return pressao

def calcular_agua(porc01, porc02):
    # A função agora apenas recebe as porcentagens e calcula direto
    litros_t1 = (porc01 * 200) / 100
    litros_t2 = (porc02 * 170) / 100
    
    total = litros_t1 + litros_t2
    porc_total = (total * 100) / 370
    tempo = (total / 42.5) * 5 if total > 0 else 0.0
    
    return {"total": total, "porc_total": porc_total, "tempo": tempo}

# --- INTERFACE (Streamlit) ---

st.set_page_config(page_title="GTE Tools", layout="centered")
st.title("🧰 Ferramentas GTE")

tab1, tab2 = st.tabs(["✈️ Porta VC-1", "💧 Água (QTA)"])

with tab1:
    st.subheader("Verificação de Pressão")
    temp = st.number_input("Temperatura (°C):", -40.0, 50.0, 20.0, 0.1)
    if st.button("Calcular Porta"):
        p = calcular_pressao_porta(temp)
        st.metric("Pressão Nominal Calculada", f"{p:.1f} PSI")
        
        col1, col2 = st.columns(2)
        col1.metric("Mínimo (-5%)", f"{p*0.95:.1f} PSI")
        col2.metric("Máximo (+5%)", f"{p*1.05:.1f} PSI")

with tab2:
    st.subheader("Cálculo de Água Potável")
    
    # Tanque 01
    check01_cheio = st.checkbox("Tanque 01 Cheio (200L)", True)
    if not check01_cheio:
        porc01 = st.slider("Porcentagem Tanque 01", 0, 100, 50, key="p1")
    else:
        porc01 = 100
    
    # Tanque 02 - Regra: Só libera se o Tanque 01 tiver alguma água
    if porc01 > 0:
        check02_cheio = st.checkbox("Tanque 02 Cheio (170L)", False)
        if not check02_cheio:
            porc02 = st.slider("Porcentagem Tanque 02", 0, 100, 0, key="p2")
        else:
            porc02 = 100
    else:
        st.warning("O Tanque 01 precisa ter água para habilitar o Tanque 02.")
        porc02 = 0
    
    res = calcular_agua(porc01, porc02)
    
    st.write("---")
    st.metric("Total Água", f"{res['total']:.1f} L")
    st.metric("Nível Global", f"{res['porc_total']:.1f}%")
    st.metric("Tempo de Chuveiro", f"{res['tempo']:.1f} min")

st.markdown("---")
st.caption("Sistema de verificação de portas para o VC-1. Software não oficial desenvolvido por 2S MIGUEL.")
