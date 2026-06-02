import streamlit as st
import pandas as pd
import os
from datetime import datetime
import os

# =====================================
# CONFIGURAÇÃO DO STREAMLIT
# =====================================
st.set_page_config(
    page_title="Bolão do Churrasco",
    page_icon="⚽",
    layout="centered"
)

# =====================================
# CONFIGURAÇÕES DO JOGO
# =====================================
TIME_A = "Brasil"
TIME_B = "Marrocos"

VALOR_APOSTA = 80
PERCENTUAL_PREMIO = 0.40

ENCERRAMENTO = datetime(2026, 6, 13, 19, 0)

# =====================================
# ARQUIVO (SIMPLIFICADO - SEM ERRO DE PATH)
# =====================================
import os

ARQUIVO = os.path.join(os.getcwd(), "palpites.csv")

# =====================================
# TÍTULO
# =====================================
st.title("⚽ Bolão do Churrasco")

st.subheader(f"{TIME_A} x {TIME_B}")

st.caption(
    f"Encerramento: {ENCERRAMENTO.strftime('%d/%m/%Y %H:%M')}"
)

# =====================================
# CARREGAR DADOS
# =====================================
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
    participantes = len(df)
else:
    participantes = 0

premio = participantes * VALOR_APOSTA * PERCENTUAL_PREMIO

col1, col2 = st.columns(2)

with col1:
    st.metric("👥 Participantes", participantes)

with col2:
    st.metric("🏆 Prêmio Atual", f"R$ {premio:.2f}")

# =====================================
# CONTAGEM REGRESSIVA
# =====================================
agora = datetime.now()

if agora < ENCERRAMENTO:
    restante = ENCERRAMENTO - agora
    dias = restante.days
    horas = restante.seconds // 3600
    minutos = (restante.seconds % 3600) // 60

    st.info(f"⏰ Encerramento em {dias}d {horas}h {minutos}min")
else:
    st.error("🚫 As apostas estão encerradas.")
    st.stop()

st.markdown("---")

# =====================================
# FORMULÁRIO
# =====================================
nome = st.text_input("Nome")

col1, col2 = st.columns(2)

with col1:
    gols_a = st.number_input(f"Gols {TIME_A}", 0, 20, 0)

with col2:
    gols_b = st.number_input(f"Gols {TIME_B}", 0, 20, 0)

primeiro_gol = st.radio(
    "Quem fará o primeiro gol?",
    [TIME_A, TIME_B]
)

minuto = st.number_input(
    "Minuto do primeiro gol",
    min_value=1,
    max_value=120,
    value=1
)

# =====================================
# SALVAR PALPITE
# =====================================
if st.button("Enviar Palpite"):

    if nome.strip() == "":
        st.error("Informe seu nome.")
        st.stop()

    # evita nome duplicado
    if os.path.exists(ARQUIVO):
        df_existente = pd.read_csv(ARQUIVO)
        nomes = df_existente["Nome"].astype(str).str.lower().str.strip()

        if nome.lower().strip() in nomes.values:
            st.error("Você já fez um palpite.")
            st.stop()

    novo_palpite = pd.DataFrame([{
        "Nome": nome,
        "GolsA": gols_a,
        "GolsB": gols_b,
        "PrimeiroGol": primeiro_gol,
        "Minuto": minuto,
        "DataHora": datetime.now()
    }])

    # salva ou cria arquivo automaticamente
    novo_palpite.to_csv(
        ARQUIVO,
        mode="a",
        header=not os.path.exists(ARQUIVO),
        index=False
    )

    st.success("✅ Palpite registrado com sucesso!")
    st.balloons()
