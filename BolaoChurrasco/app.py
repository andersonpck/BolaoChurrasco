import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =====================================
# CONFIGURAÇÕES DO STREAMLIT (TEM QUE SER PRIMEIRO)
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
BASE_DIR = os.path.dirname(os.path.abspath(_file_))
ARQUIVO = os.path.join(BASE_DIR, "palpites.csv")

ENCERRAMENTO = datetime(2026, 6, 13, 19, 0)

# =====================================
# PÁGINA
# =====================================
st.title("⚽ Bolão do Churrasco")

st.subheader(f"{BANDEIRA_A} {TIME_A} x {TIME_B} {BANDEIRA_B}")

st.caption(
    f"Encerramento: {ENCERRAMENTO.strftime('%d/%m/%Y %H:%M')}"
)
# =====================================
# PARTICIPANTES
# =====================================
if os.path.exists(ARQUIVO):
    df = pd.read_csv(ARQUIVO)
    participantes = len(df)
else:
    participantes = 0
premio = (
    participantes
    * VALOR_APOSTA
    * PERCENTUAL_PREMIO
)
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "👥 Participantes",
        participantes
    )
with col2:
    st.metric(
        "🏆 Prêmio Atual",
        f"R$ {premio:.2f}"
    )
# =====================================
# CONTAGEM REGRESSIVA
# =====================================
agora = datetime.now()
if agora < ENCERRAMENTO:
    restante = ENCERRAMENTO - agora
    dias = restante.days
    horas = restante.seconds // 3600
    minutos = (
        restante.seconds % 3600
    ) // 60
    st.info(
        f"⏰ Encerramento em "
        f"{dias}d "
        f"{horas}h "
        f"{minutos}min"
    )
else:
    st.error(
        "🚫 As apostas estão encerradas."
    )
    st.stop()
st.markdown("---")
# =====================================
# FORMULÁRIO
# =====================================
nome = st.text_input(
    "Nome"
)
col1, col2 = st.columns(2)
with col1:
    gols_a = st.number_input(
        f"Gols {TIME_A}",
        min_value=0,
        max_value=20,
        value=0
    )
with col2:
    gols_b = st.number_input(
        f"Gols {TIME_B}",
        min_value=0,
        max_value=20,
        value=0
    )
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
        st.error(
            "Informe seu nome."
        )
        st.stop()
    if os.path.exists(ARQUIVO):
        df_existente = pd.read_csv(
            ARQUIVO
        )
        nomes_existentes = (
            df_existente["Nome"]
            .astype(str)
            .str.lower()
            .str.strip()
        )
        if (
            nome.lower().strip()
            in nomes_existentes.values
        ):
            st.error(
                "Você já realizou um palpite."
            )
            st.stop()
    novo_palpite = pd.DataFrame([{
        "Nome": nome,
        "GolsA": gols_a,
        "GolsB": gols_b,
        "PrimeiroGol": primeiro_gol,
        "Minuto": minuto,
        "DataHora": datetime.now()
    }])
    if os.path.exists(ARQUIVO):
        novo_palpite.to_csv(
            ARQUIVO,
            mode="a",
            header=False,
            index=False
        )
    else:
        novo_palpite.to_csv(
            ARQUIVO,
            index=False
        )
    st.success(
        "✅ Palpite registrado com sucesso!"
    )
    st.balloons()
