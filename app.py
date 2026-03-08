import streamlit as st

# =========================
# Funções de Cálculo Porta VC-1
# =========================

def calcular_pressao(temp: float) -> int:
    t = int(temp)
    if temp >= 40.0:
        return 1880 + ((t - 40) * 7)
    elif temp >= 30.0:
        return 1810 + ((t - 30) * 7)
    elif temp >= 20.0:
        return 1740 + ((t - 20) * 7)
    elif temp >= 10.0:
        return 1660 + ((t - 10) * 8)
    elif temp >= 0.0:
        return 1610 + (t * 5)
    elif temp >= -10.0:
        return 1610 - (abs(t) * 7)
    elif temp >= -20.0:
        return 1540 - ((abs(t) - 10) * 7.5)
    elif temp >= -30.0:
        return 1465 - ((abs(t) - 20) * 7)
    else:
        return 1395 - ((abs(t) - 30) * 7)

def calcular_margens(pressao: int) -> tuple:
    minimo = round(pressao * 0.95)
    maximo = round(pressao * 1.05)
    return minimo, maximo

# =========================
# Funções de Cálculo Água QTA
# =========================

def litros_tanque(porcentagem: int, capacidade: int) -> float:
    return (porcentagem / 100) * capacidade

def calcular_agua(t1_pct: int, t2_pct: int) -> dict:
    tanque1 = litros_tanque(t1_pct, 200)
    tanque2 = litros_tanque(t2_pct, 170)
    total = tanque1 + tanque2
    nivel_global = (total * 100) / 370 if total > 0 else 0
    tempo_chuveiro = (total / 42.5) * 5 if total > 0 else 0
    return {
        "tanque1": tanque1,
        "tanque2": tanque2,
        "total": total,
        "nivel_global": nivel_global,
        "tempo_chuveiro": tempo_chuveiro
    }

# =========================
# Pesos de Trolleys e Fornos
# =========================

FORNO_PESOS = {
    "Completo com Louça 15kg": 15,
    "Completo Descartável 8kg": 8,
}

# =========================
# Callbacks de Sincronização Água
# =========================

def sync_checkbox_t1():
    st.session_state.t1_pct = 100 if st.session_state.t1_full else 0

def sync_slider_t1():
    st.session_state.t1_full = (st.session_state.t1_pct == 100)

def sync_checkbox_t2():
    st.session_state.t2_pct = 100 if st.session_state.t2_full else 0

def sync_slider_t2():
    st.session_state.t2_full = (st.session_state.t2_pct == 100)

# =========================
# Interface Streamlit
# =========================

st.set_page_config(layout="centered")
st.title("Ferramentas Comissários VC-1")

tab1, tab2, tab3 = st.tabs(["✈️ Pressão Porta", "💧 Água (QTA)", "🍽️ Peso nas Galleys"])

# --- Aba 1: Porta VC-1 ---
with tab1:
    st.subheader("Cálculo de Pressão da Porta VC-1")
    temp = st.number_input("Temperatura ambiente (°C)", -40.0, 50.0, step=0.1)
    if st.button("Calcular Porta"):
        pressao = calcular_pressao(temp)
        minimo, maximo = calcular_margens(pressao)
        st.success(f"Pressão Nominal: {pressao} PSI")
        col1, col2 = st.columns(2)
        col1.metric("Mínimo (-5%)", f"{minimo} PSI")
        col2.metric("Máximo (+5%)", f"{maximo} PSI")

# --- Aba 2: Água QTA ---
with tab2:
    st.subheader("Controle de Água Potável")

    # Inicialização de estados
    if "t1_full" not in st.session_state:
        st.session_state.t1_full = False
    if "t1_pct" not in st.session_state:
        st.session_state.t1_pct = 0
    if "t2_full" not in st.session_state:
        st.session_state.t2_full = False
    if "t2_pct" not in st.session_state:
        st.session_state.t2_pct = 0

    # Tanque 01
    st.checkbox("Tanque 01 Cheio", key="t1_full", on_change=sync_checkbox_t1)
    st.slider("Tanque 01 (%)", 0, 100, key="t1_pct", on_change=sync_slider_t1)

    # Tanque 02 (bloqueado se Tanque 01 < 100%)
    if st.session_state.t1_pct == 100:
        st.checkbox("Tanque 02 Cheio", key="t2_full", on_change=sync_checkbox_t2)
        st.slider("Tanque 02 (%)", 0, 100, key="t2_pct", on_change=sync_slider_t2)
    else:
        st.session_state.t2_pct = 0
        st.session_state.t2_full = False
        st.info("Tanque 02 só pode ser utilizado quando o Tanque 01 estiver 100% cheio.")

    # Cálculos
    dados = calcular_agua(st.session_state.t1_pct, st.session_state.t2_pct)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Água (L)", f"{dados['total']:.1f} L")
    col2.metric("Nível Global (%)", f"{dados['nivel_global']:.1f}%")
    if dados["total"] > 0:
        col3.metric("Tempo de Chuveiro", f"{dados['tempo_chuveiro']:.1f} min")

# --- Aba 3: Peso nas Galleys ---
with tab3:
    st.subheader("Controle de Peso nas Galleys")

    # --- Galley Dianteira ---
    st.markdown("### Galley Dianteira")
    qtd_grande_dianteira = st.number_input("Trolleys Grandes (27-81kg)", min_value=0, max_value=2, step=1, key="galley_dianteira_grande")
    qtd_pequeno_dianteira = st.number_input("Trolleys Pequenos (15-44kg)", min_value=0, max_value=4, step=1, key="galley_dianteira_pequeno")
    forno_dianteira = st.selectbox("Forno Dianteira", options=["Nenhum"] + list(FORNO_PESOS.keys()), key="galley_dianteira_forno")

    espacos_dianteira = qtd_grande_dianteira + (qtd_pequeno_dianteira // 2)
    if espacos_dianteira > 2 or (qtd_pequeno_dianteira % 2 != 0):
        st.error("Galley Dianteira suporta no máximo 2 espaços (2 grandes ou 4 pequenos, ou 1 grande + 2 pequenos).")
        peso_dianteira = 0
    else:
        peso_dianteira = (qtd_grande_dianteira * 64) + (qtd_pequeno_dianteira * 44)  # exemplo com pesos médios
        if forno_dianteira != "Nenhum":
            peso_dianteira += FORNO_PESOS[forno_dianteira]
    st.metric("Peso Galley Dianteira", f"{peso_dianteira} kg")

    # --- Galley PR ---
    st.markdown("### Galley PR")
    peso_pr = st.number_input("Peso manual (kg)", min_value=0, step=1, key="galley_pr_peso")
    st.metric("Peso Galley PR", f"{peso_pr} kg")

    # --- Galley Traseira ---
    st.markdown("### Galley Traseira")
    qtd_grande_traseira = st.number_input("Trolleys Grandes (27-81kg)", min_value=0, max_value=5, step=1, key="galley_traseira_grande")
    qtd_pequeno_traseira = st.number_input("Trolleys Pequenos (15-44kg)", min_value=0, max_value=10, step=1, key="galley_traseira_pequeno")
    fornos_traseira = st.multiselect("Selecione os Fornos (até 3)", options=list(FORNO_PESOS.keys()), key="galley_traseira_fornos")

    espacos_traseira = qtd_grande_traseira + (qtd_pequeno_traseira // 2)
    if espacos_traseira > 5
