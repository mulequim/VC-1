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

# --- Lógica de Cálculo Atualizada ---
def calcular_agua(check01, porc01, check02, porc02):
    # Regra: Tanque 01 é obrigatório para ter o 02 ativo
    # Se Tanque 01 desmarcado, tudo vira 0, independente do Tanque 02
    if not check01:
        return {"total": 0.0, "porc_total": 0.0, "tempo": 0.0}
    
    # Se Tanque 01 está ativo:
    litros_t1 = 200.0 if check01 and porc01 == 100 else (porc01 * 200 / 100)
    
    # Tanque 02 só entra na conta se check02 estiver ativo e o check01 também estiver
    litros_t2 = (170.0 if check02 and porc02 == 100 else (porc02 * 170 / 100)) if check02 else 0.0
    
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
        st.metric("Pressão Ideal", f"{p:.1f} PSI")
        st.write(f"Faixa: {p*0.95:.1f} a {p*1.05:.1f} PSI")

with tab2:
    st.subheader("Cálculo de Água Potável")
    
    # Tanque 01
    check01 = st.checkbox("Tanque 01 Cheio (200L)", True)
    porc01 = st.slider("Porcentagem Tanque 01", 0, 100, 100) if not check01 else 100
    
    # Tanque 02 - Só habilita se check01 estiver marcado
    if check01:
        check02 = st.checkbox("Tanque 02 Cheio (170L)", False)
        porc02 = st.slider("Porcentagem Tanque 02", 0, 100, 100) if not check02 else 100
    else:
        st.warning("Tanque 01 deve estar ativo para gerenciar o Tanque 02.")
        check02 = False
        porc02 = 0
    
    res = calcular_agua(check01, porc01, check02, porc02)
    
    st.write("---")
    st.metric("Total Água", f"{res['total']:.1f} L")
    st.metric("Nível Global", f"{res['porc_total']:.1f}%")
    st.metric("Tempo de Chuveiro", f"{res['tempo']:.1f} min")

st.markdown("---")
st.caption("Software não oficial desenvolvido por 2S MIGUEL.")
