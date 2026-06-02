import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =====================================
# CONFIGURAÇÃO
# =====================================
st.set_page_config(
    page_title="Bolão do Churrasco",
    page_icon="⚽",
    layout="centered"
)

TIME_A = "Brasil"
TIME_B = "Marrocos"

VALOR_APOSTA = 80
PERCENTUAL_PREMIO = 0.50

ARQUIVO = "palpites.csv"

ENCERRAMENTO = datetime(2026, 6, 13, 19, 0)

ADMIN_PASSWORD = "1234"

# =====================================
# MENU
# =====================================
modo = st.sidebar.selectbox(
    "Modo",
    ["Apostar", "Admin"]
)

# =====================================
# CRIA CSV
# =====================================
if not os.path.exists(ARQUIVO):
    pd.DataFrame(columns=[
        "Nome",
        "GolsA",
        "GolsB",
        "PrimeiroGol",
        "Minuto",
        "DataHora"
    ]).to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

# =====================================
# CABEÇALHO
# =====================================
st.title("⚽ Bolão do Churrasco")

# =====================================
# MODO APOSTAR
# =====================================
if modo == "Apostar":

    total_participantes = len(df)

    premio = (
        total_participantes
        * VALOR_APOSTA
        * PERCENTUAL_PREMIO
    )

    st.subheader(f"{TIME_A} x {TIME_B}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "👥 Participantes",
            total_participantes
        )

    with col2:
        st.metric(
            "🏆 Prêmio Atual",
            f"R$ {premio:,.2f}"
        )

    # =====================================
    # REGRAS
    # =====================================
    st.markdown("### 📜 Regras do Bolão")

    st.info(
        f"""
• Cada palpite custa **R$ {VALOR_APOSTA}**

• **50%** do valor arrecadado vai para o vencedor

• **50%** do valor arrecadado ajuda a pagar o churrasco

• Cada participante leva sua própria bebida

• Critério de desempate:
    1. Placar mais próximo
    2. Time que faz o primeiro gol
    3. Minuto do primeiro gol

• Apenas 1 vencedor por jogo
"""
    )

    # =====================================
    # CONTAGEM REGRESSIVA
    # =====================================
    agora = datetime.now()

    if agora < ENCERRAMENTO:

        restante = ENCERRAMENTO - agora

        dias = restante.days
        horas = restante.seconds // 3600
        minutos = (restante.seconds % 3600) // 60

        st.info(
            f"⏰ Encerramento em "
            f"{dias}d "
            f"{horas}h "
            f"{minutos}min"
        )

    else:
        st.error("⛔ Apostas encerradas.")
        st.stop()

    st.markdown("---")

    # =====================================
    # FORMULÁRIO
    # =====================================
    nome = st.text_input("Nome")

    col1, col2 = st.columns(2)

    with col1:
        gols_a = st.number_input(
            f"Gols {TIME_A}",
            0,
            20,
            0
        )

    with col2:
        gols_b = st.number_input(
            f"Gols {TIME_B}",
            0,
            20,
            0
        )

    primeiro_gol = st.radio(
        "Quem fará o primeiro gol?",
        [TIME_A, TIME_B]
    )

    minuto = st.number_input(
        "Minuto do primeiro gol",
        1,
        120,
        1
    )

    if st.button("Enviar palpite"):

        if nome.strip() == "":
            st.error("Digite seu nome.")
            st.stop()

        nomes_existentes = (
            df["Nome"]
            .astype(str)
            .str.lower()
            .tolist()
        )

        if nome.lower() in nomes_existentes:
            st.error(
                "Você já registrou um palpite."
            )
            st.stop()

        novo = pd.DataFrame([{
            "Nome": nome,
            "GolsA": gols_a,
            "GolsB": gols_b,
            "PrimeiroGol": primeiro_gol,
            "Minuto": minuto,
            "DataHora": datetime.now()
        }])

        novo.to_csv(
            ARQUIVO,
            mode="a",
            header=False,
            index=False
        )

        st.success(
            "✅ Palpite registrado!"
        )

        st.balloons()

# =====================================
# ADMIN
# =====================================
else:

    senha = st.text_input(
        "Senha do admin",
        type="password"
    )

    if senha != ADMIN_PASSWORD:
        st.warning("🔒 Acesso restrito.")
        st.stop()

    st.subheader(
        "🏆 Administração do Bolão"
    )

    total_participantes = len(df)

    premio = (
        total_participantes
        * VALOR_APOSTA
        * PERCENTUAL_PREMIO
    )

    st.metric(
        "Prêmio Atual",
        f"R$ {premio:,.2f}"
    )

    st.metric(
        "Participantes",
        total_participantes
    )

    st.markdown("---")

    if st.button(
        "🧨 Zerar bolão (apagar todos os palpites)"
    ):

        pd.DataFrame(columns=[
            "Nome",
            "GolsA",
            "GolsB",
            "PrimeiroGol",
            "Minuto",
            "DataHora"
        ]).to_csv(
            ARQUIVO,
            index=False
        )

        st.success(
            "🔥 Todos os palpites foram apagados."
        )

        st.stop()

    if df.empty:
        st.warning(
            "Nenhum palpite registrado."
        )
        st.stop()

    resultado_a = st.number_input(
        f"Gols {TIME_A}",
        0,
        20,
        0
    )

    resultado_b = st.number_input(
        f"Gols {TIME_B}",
        0,
        20,
        0
    )

    primeiro_gol_oficial = st.radio(
        "Primeiro gol oficial",
        [TIME_A, TIME_B]
    )

    minuto_oficial = st.number_input(
        "Minuto oficial do primeiro gol",
        1,
        120,
        1
    )

    if st.button("Calcular vencedor"):

        def calcular_pontos(linha):

            erro_placar = (
                abs(
                    linha["GolsA"] - resultado_a
                )
                +
                abs(
                    linha["GolsB"] - resultado_b
                )
            )

            erro_time = 0

            if (
                linha["PrimeiroGol"]
                != primeiro_gol_oficial
            ):
                erro_time = 100

            erro_minuto = abs(
                linha["Minuto"]
                - minuto_oficial
            )

            return (
                erro_placar * 1000
                + erro_time
                + erro_minuto
            )

        df["Pontuacao"] = df.apply(
            calcular_pontos,
            axis=1
        )

        ranking = df.sort_values(
            "Pontuacao"
        )

        vencedor = ranking.iloc[0]

        st.success(
            f"🏆 Vencedor: {vencedor['Nome']}"
        )

        st.success(
            f"💰 Prêmio: R$ {premio:,.2f}"
        )

        st.subheader(
            "📊 Ranking Final"
        )

        st.dataframe(
            ranking[
                [
                    "Nome",
                    "GolsA",
                    "GolsB",
                    "PrimeiroGol",
                    "Minuto",
                    "Pontuacao"
                ]
            ],
            use_container_width=True
        )
