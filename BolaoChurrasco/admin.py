import streamlit as st
import pandas as pd
import os
st.write(os.listdir())
# =====================================
# CONFIGURAÇÕES
# =====================================
ARQUIVO = "palpites.csv"
VALOR_APOSTA = 80

st.set_page_config(
    page_title="Administração do Bolão",
    page_icon="🏆",
    layout="centered"
)

st.title("🏆 Administração do Bolão")

# =====================================
# RESULTADO DO JOGO
# =====================================
resultado_brasil = st.number_input(
    "Gols Brasil",
    min_value=0,
    max_value=20,
    value=0
)

resultado_marrocos = st.number_input(
    "Gols Marrocos",
    min_value=0,
    max_value=20,
    value=0
)

primeiro_gol = st.radio(
    "Primeiro gol",
    ["Brasil", "Marrocos"]
)

minuto_primeiro_gol = st.number_input(
    "Minuto do primeiro gol",
    min_value=1,
    max_value=120,
    value=1
)

# =====================================
# BOTÃO
# =====================================
if st.button("Calcular vencedor"):

    # =====================================
    # PROTEÇÃO CSV
    # =====================================
    if not os.path.exists(ARQUIVO):
        st.warning("Nenhum palpite registrado ainda.")
        st.stop()

    df = pd.read_csv(ARQUIVO)

    required_cols = ["Nome", "GolsA", "GolsB", "PrimeiroGol", "Minuto"]

    if not all(col in df.columns for col in required_cols):
        st.error("CSV inválido ou corrompido.")
        st.stop()

    # =====================================
    # FINANCEIRO
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
    # FUNÇÃO DE RANKING (HIERÁRQUICO CORRETO)
    # =====================================
    def calcular_rank(linha):

        # 1) Placar exato (CRITÉRIO MAIS IMPORTANTE)
        placar_exato = (
            linha["GolsA"] == resultado_brasil and
            linha["GolsB"] == resultado_marrocos
        )

        # 2) Resultado (vitória/empate/derrota)
        resultado_real = resultado_brasil - resultado_marrocos
        resultado_aposta = linha["GolsA"] - linha["GolsB"]

        acertou_resultado = (
            (resultado_real > 0 and resultado_aposta > 0) or
            (resultado_real < 0 and resultado_aposta < 0) or
            (resultado_real == 0 and resultado_aposta == 0)
        )

        # 3) Primeiro gol
        acertou_primeiro_gol = (
            linha["PrimeiroGol"] == primeiro_gol
        )

        # 4) Minuto (APENAS DESEMPATE FINAL)
        erro_minuto = abs(linha["Minuto"] - minuto_primeiro_gol)

        # =====================================
        # TUPLA DE RANKING (ordem importa)
        # =====================================
        return (
            int(placar_exato),          # 1º critério
            int(acertou_resultado),     # 2º critério
            int(acertou_primeiro_gol),  # 3º critério
            -erro_minuto                # 4º critério (menor vence)
        )

    # =====================================
    # RANKING
    # =====================================
    df["Rank"] = df.apply(calcular_rank, axis=1)

    ranking = df.sort_values(by="Rank", ascending=False)

    vencedor = ranking.iloc[0]

    # =====================================
    # RESULTADO
    # =====================================
    st.success(f"🏆 Vencedor: {vencedor['Nome']}")

    # Se quiser mostrar empate técnico
    melhores = ranking[ranking["Rank"] == ranking.iloc[0]["Rank"]]

    if len(melhores) > 1:
        st.warning("⚠️ Houve empate!")

    # =====================================
    # RANKING FINAL
    # =====================================
    st.subheader("📊 Ranking Final")

    st.dataframe(
        ranking[
            ["Nome", "GolsA", "GolsB", "PrimeiroGol", "Minuto"]
        ],
        use_container_width=True
    )

    # =====================================
    # RESUMO DO JOGO
    # =====================================
    st.markdown("### 📌 Resultado do Jogo")

    st.write(f"Brasil {resultado_brasil} x {resultado_marrocos} Marrocos")
    st.write(f"Primeiro gol: {primeiro_gol}")
    st.write(f"Minuto: {minuto_primeiro_gol}")
