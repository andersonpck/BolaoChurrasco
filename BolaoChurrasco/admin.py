import streamlit as st
import pandas as pd
import os

# =====================================
# CONFIGURAÇÃO
# =====================================
st.set_page_config(
    page_title="Administração",
    page_icon="🏆",
    layout="centered"
)

st.title("🏆 Administração do Bolão")

TIME_A = "Brasil"
TIME_B = "Marrocos"

VALOR_APOSTA = 80

# =====================================
# CAMINHO DO CSV (MESMO DO APP)
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE_DIR, "palpites.csv")

# =====================================
# INPUT DO RESULTADO OFICIAL
# =====================================
resultado_a = st.number_input(
    f"Gols {TIME_A}",
    min_value=0,
    max_value=20,
    value=0
)

resultado_b = st.number_input(
    f"Gols {TIME_B}",
    min_value=0,
    max_value=20,
    value=0
)

primeiro_gol = st.radio(
    "Primeiro gol",
    [TIME_A, TIME_B]
)

minuto_primeiro_gol = st.number_input(
    "Minuto do primeiro gol",
    min_value=1,
    max_value=120,
    value=1
)

# =====================================
# BOTÃO CALCULAR
# =====================================
if st.button("Calcular vencedor"):

    if not os.path.exists(ARQUIVO):
        st.error("Nenhum palpite registrado ainda.")
        st.stop()

    df = pd.read_csv(ARQUIVO)

    # =====================================
    # PRÊMIO
    # =====================================
    total = len(df) * VALOR_APOSTA
    premio = total * 0.4
    churrasco = total * 0.6

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Arrecadado", f"R$ {total:.2f}")

    with col2:
        st.metric("Prêmio", f"R$ {premio:.2f}")

    with col3:
        st.metric("Churrasco", f"R$ {churrasco:.2f}")

    # =====================================
    # FUNÇÃO DE PONTUAÇÃO
    # =====================================
    def calcular_pontos(linha):

        # prioridade máxima: placar
        erro_placar = (
            abs(linha["GolsA"] - resultado_a)
            + abs(linha["GolsB"] - resultado_b)
        )

        # segundo critério: primeiro gol (forte penalidade)
        erro_time = 0
        if linha["PrimeiroGol"] != primeiro_gol:
            erro_time = 100

        # desempate: minuto
        erro_minuto = abs(linha["Minuto"] - minuto_primeiro_gol)

        return erro_placar * 1000 + erro_time + erro_minuto

    # =====================================
    # RANKING
    # =====================================
    df["Pontuacao"] = df.apply(calcular_pontos, axis=1)

    ranking = df.sort_values("Pontuacao")

    vencedor = ranking.iloc[0]

    st.success(f"🏆 Vencedor: {vencedor['Nome']}")

    st.subheader("📊 Ranking Final")

    st.dataframe(
        ranking[
            ["Nome", "GolsA", "GolsB", "PrimeiroGol", "Minuto", "Pontuacao"]
        ],
        use_container_width=True
    )
