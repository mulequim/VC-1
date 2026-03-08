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

TROLLEY_PESOS = {
    "Trolley Grande Vazio 27kg": 27,
    "Trolley Grande com Louça s/Comissaria 64kg": 64,
    "Trolley Grande com Louça c/Comissaria 81kg": 81,
    "Trolley Grande com Material Descartável c/Comissaria 60kg": 60,
    "Trolley Pequeno Vazio 15kg": 15,
    "Trolley Pequeno com Louça c/Comissaria 44kg": 44,
    "Trolley Pequeno com Material Descartável c/Comissaria 30kg": 30,
}

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

    # Inicializa variáveis para evitar NameError
    peso_dianteira = 0
    peso_pr = 0

    # --- Galley Traseira ---
    st.markdown("### Galley Traseira")
    limite_espacos_traseira = 5
    espacos_traseira = 0
    peso_traseira = 0
    
    # Trolleys
    qtd_grande_vazio = st.number_input("Trolley Grande Vazio (27kg)", min_value=0, max_value=5, step=1)
    qtd_grande_louca_sc = st.number_input("Trolley Grande com Louça s/Comissaria (64kg)", min_value=0, max_value=5, step=1)
    qtd_grande_louca_cc = st.number_input("Trolley Grande com Louça c/Comissaria (81kg)", min_value=0, max_value=5, step=1)
    qtd_grande_desc = st.number_input("Trolley Grande com Material Descartável c/Comissaria (60kg)", min_value=0, max_value=5, step=1)
    
    qtd_peq_vazio = st.number_input("Trolley Pequeno Vazio (15kg)", min_value=0, max_value=10, step=1)
    qtd_peq_louca_cc = st.number_input("Trolley Pequeno com Louça c/Comissaria (44kg)", min_value=0, max_value=10, step=1)
    qtd_peq_desc = st.number_input("Trolley Pequeno com Material Descartável c/Comissaria (30kg)", min_value=0, max_value=10, step=1)
    
    permitir_um_pequeno = st.checkbox("Permitir espaço com apenas 1 trolley pequeno")
    
    # Cálculo de espaços
    num_grandes = qtd_grande_vazio + qtd_grande_louca_sc + qtd_grande_louca_cc + qtd_grande_desc
    num_pequenos = qtd_peq_vazio + qtd_peq_louca_cc + qtd_peq_desc
    
    if permitir_um_pequeno:
        espacos_traseira = num_grandes + (num_pequenos / 2)
    else:
        espacos_traseira = num_grandes + (num_pequenos // 2)
    
    # Fornos Traseiros
    st.markdown("#### Fornos Traseiros")
    qtd_forno_15 = st.number_input("Forno Completo com Louça (15kg)", min_value=0, max_value=3, step=1, key="forno_15_traseira")
    qtd_forno_8 = st.number_input("Forno Completo Descartável (8kg)", min_value=0, max_value=3, step=1, key="forno_8_traseira")
    
    valido_fornos = True
    if qtd_forno_15 == 3 and qtd_forno_8 > 0:
        valido_fornos = False
    elif qtd_forno_8 == 3 and qtd_forno_15 > 0:
        valido_fornos = False
    elif qtd_forno_15 + qtd_forno_8 > 3:
        valido_fornos = False
    
    if not valido_fornos:
        st.error("Combinação inválida: máximo 3 fornos, respeitando exclusividade entre 15kg e 8kg.")
        peso_fornos_traseira = 0
    else:
        peso_fornos_traseira = (qtd_forno_15 * 15) + (qtd_forno_8 * 8)
    
    # Validação final da galley traseira
    if espacos_traseira > limite_espacos_traseira:
        st.error("Galley Traseira suporta no máximo 5 espaços.")
        peso_traseira = 0
    else:
        peso_traseira = (
            qtd_grande_vazio * 27 +
            qtd_grande_louca_sc * 64 +
            qtd_grande_louca_cc * 81 +
            qtd_grande_desc * 60 +
            qtd_peq_vazio * 15 +
            qtd_peq_louca_cc * 44 +
            qtd_peq_desc * 30 +
            peso_fornos_traseira
        )
    
    st.metric("Peso Galley Traseira", f"{peso_traseira} kg")

    # --- Total ---
    total_galleys = peso_dianteira + peso_pr + peso_traseira
    st.success(f"**Total das Galleys: {total_galleys} kg**")




# --- Rodapé ---
st.divider()
st.caption("Ferramentas de Apoio ao Comissário do VC-1.")
st.caption("Software não oficial desenvolvido por 2S MIGUEL.")

