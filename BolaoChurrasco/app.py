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
ARQUIVO = "palpites.csv"

ENCERRAMENTO = datetime(2026, 6, 13, 19, 0)

ADMIN_PASSWORD = "1234"

# =====================================
# MENU
# =====================================
modo = st.sidebar.selectbox("Modo", ["Apostar", "Admin"])

st.title("⚽ Bolão do Churrasco")

# =====================================
# CRIA CSV SE NÃO EXISTIR
# =====================================
if not os.path.exists(ARQUIVO):
    df_init = pd.DataFrame(columns=[
        "Nome", "GolsA", "GolsB", "PrimeiroGol", "Minuto", "DataHora"
    ])
    df_init.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

# =====================================
# MODO APOSTA
# =====================================
if modo == "Apostar":

    st.subheader(f"{TIME_A} x {TIME_B}")

    agora = datetime.now()

    if agora > ENCERRAMENTO:
        st.error("⛔ Apostas encerradas.")
        st.stop()

    nome = st.text_input("Nome")

    col1, col2 = st.columns(2)

    with col1:
        gols_a = st.number_input(f"Gols {TIME_A}", 0, 20, 0)

    with col2:
        gols_b = st.number_input(f"Gols {TIME_B}", 0, 20, 0)

    primeiro_gol = st.radio("Primeiro gol", [TIME_A, TIME_B])

    minuto = st.number_input("Minuto do primeiro gol", 1, 120, 1)

    if st.button("Enviar palpite"):

        if nome.strip() == "":
            st.error("Digite seu nome.")
            st.stop()

        if nome.lower() in df["Nome"].astype(str).str.lower().values:
            st.error("Você já fez seu palpite.")
            st.stop()

        novo = pd.DataFrame([{
            "Nome": nome,
            "GolsA": gols_a,
            "GolsB": gols_b,
            "PrimeiroGol": primeiro_gol,
            "Minuto": minuto,
            "DataHora": datetime.now()
        }])

        novo.to_csv(ARQUIVO, mode="a", header=False, index=False)

        st.success("✅ Palpite registrado!")
        st.balloons()

    st.markdown("---")
    st.subheader("📊 Palpites registrados")

    st.dataframe(df)

# =====================================
# MODO ADMIN (PROTEGIDO)
# =====================================
elif modo == "Admin":

    senha = st.text_input("Senha do admin", type="password")

    if senha != ADMIN_PASSWORD:
        st.warning("🔒 Acesso restrito.")
        st.stop()

    st.subheader("🏆 Administração do Bolão")

    if df.empty:
        st.warning("Nenhum palpite registrado ainda.")
        st.stop()

    resultado_a = st.number_input(f"Gols {TIME_A}", 0, 20, 0)
    resultado_b = st.number_input(f"Gols {TIME_B}", 0, 20, 0)

    primeiro_gol_oficial = st.radio("Primeiro gol oficial", [TIME_A, TIME_B])

    minuto_oficial = st.number_input("Minuto do primeiro gol", 1, 120, 1)

    if st.button("Calcular vencedor"):

        def calcular_pontos(linha):

            erro_placar = (
                abs(linha["GolsA"] - resultado_a) +
                abs(linha["GolsB"] - resultado_b)
            )

            erro_time = 0
            if linha["PrimeiroGol"] != primeiro_gol_oficial:
                erro_time = 100

            erro_minuto = abs(linha["Minuto"] - minuto_oficial)

            return erro_placar * 1000 + erro_time + erro_minuto

        df["Pontuacao"] = df.apply(calcular_pontos, axis=1)

        ranking = df.sort_values("Pontuacao")

        vencedor = ranking.iloc[0]

        st.success(f"🏆 Vencedor: {vencedor['Nome']}")

        st.subheader("📊 Ranking Final")

        st.dataframe(
            ranking[
                ["Nome", "GolsA", "GolsB", "PrimeiroGol", "Minuto", "Pontuacao"]
            ]
        )
