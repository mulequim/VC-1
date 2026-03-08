import streamlit as st

# --- MÓDULO DE LÓGICA (Controllers) ---

def calcular_pressao_porta(temp):
    # Lógica validada da porta VC-1
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

def calcular_agua(check01, porc01, check02, porc02):
    t1 = 100.0 if check01 else float(porc01)
    t2 = 100.0 if check02 else float(porc02)
    
    litros_t1 = (t1 * 200) / 100
    litros_t2 = (t2 * 170) / 100
    total = litros_t1 + litros_t2
    
    return {
        "total": total,
        "porc_total": (total * 100) / 370,
        "tempo": (total / 42.5) * 5
    }

# --- INTERFACE (Streamlit) ---

st.set_page_config(page_title="GTE Tools", layout="centered")
st.title("🧰 Ferramentas GTE")

tab1, tab2 = st.tabs(["✈️ Porta VC-1", "💧 Água (QTA)"])

with tab1:
    st.subheader("Verificação de Pressão")
    temp = st.number_input("Temperatura (°C):", -40.0, 50.0, 20.0, 0.1)
    if st.button("Calcular Porta"):
        p = calcular_pressao_porta(temp)
        st.metric("Pressão Ideal", f"{p:.1f} PSI")
        st.write(f"Faixa: {p*0.95:.1f} a {p*1.05:.1f} PSI")

with tab2:
    st.subheader("Cálculo de Água Potável")
    c1 = st.checkbox("Tanque 01 Cheio", True)
    p1 = st.slider("Porcentagem T1", 0, 100, 100) if not c1 else 100
    
    c2 = st.checkbox("Tanque 02 Cheio", False)
    p2 = st.slider("Porcentagem T2", 0, 100, 0) if not c2 else 100
    
    res = calcular_agua(c1, p1, c2, p2)
    
    st.write("---")
    st.metric("Total Água", f"{res['total']:.1f} L")
    st.metric("Porcentagem Total", f"{res['porc_total']:.1f}%")
    st.metric("Tempo Chuveiro", f"{res['tempo']:.1f} min")

st.markdown("---")
st.caption("Software não oficial desenvolvido por 2S MIGUEL.")
