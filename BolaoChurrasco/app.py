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

ENCERRAMENTO = datetime(
    2026,
    6,
    13,
    19,
    0
)

ADMIN_PASSWORD = "1234"

# =====================================
# MENU
# =====================================

modo = st.sidebar.selectbox(
    "Modo",
    ["Apostar", "Admin"]
)

st.title("⚽ Bolão do Churrasco")

# =====================================
# CRIA CSV SE NÃO EXISTIR
# =====================================

if not os.path.exists(ARQUIVO):

    df_init = pd.DataFrame(columns=[
        "Nome",
        "GolsA",
        "GolsB",
        "PrimeiroGol",
        "Minuto",
        "DataHora"
    ])

    df_init.to_csv(
        ARQUIVO,
        index=False
    )

df = pd.read_csv(ARQUIVO)

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

    st.subheader(
        f"{TIME_A} x {TIME_B}"
    )

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
• Cada palpite custa R$ {VALOR_APOSTA}

• 50% do valor arrecadado será pago ao vencedor.

• 50% do valor arrecadado ajudará a custear o churrasco.

• Cada participante leva sua própria bebida.

• Apenas um vencedor por partida.

• Após o encerramento não serão aceitos novos palpites.
"""
    )

    # =====================================
    # FÓRMULA
    # =====================================

    st.markdown("### 🧮 Como o vencedor é calculado?")

    st.write(
        "Vence quem tiver o menor erro total."
    )

    st.latex(
        r"""
        E =
        1000\left(
        |P_A-R_A|
        +
        |P_B-R_B|
        \right)
        +
        100I
        +
        |M_P-M_R|
        """
    )

    st.markdown("""
**Onde:**

- **E** = Erro Total
- **P_A** = gols previstos para o Time A
- **R_A** = gols reais do Time A
- **P_B** = gols previstos para o Time B
- **R_B** = gols reais do Time B
- **M_P** = minuto previsto do primeiro gol
- **M_R** = minuto real do primeiro gol
- **I = 0** se acertar quem fez o primeiro gol
- **I = 1** se errar quem fez o primeiro gol

🏆 Ganha quem tiver o menor valor de E.
""")

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

        st.warning(
            f"⏳ Encerramento em "
            f"{dias}d "
            f"{horas}h "
            f"{minutos}min"
        )

    else:

        st.error(
            "⛔ Apostas encerradas."
        )

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
            st.error(
                "Digite seu nome."
            )
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
        "💰 Aposta registrada com sucesso! 🍖"
        )

        st.markdown(
        """
        <div style="
        text-align:center;
        font-size:50px;
        line-height:2;
        margin-top:20px;
        ">
        💸 💸 💸 💸 💸 💸 💸 💸<br>
        🍖 🍺 🍖 🍺 🍖 🍺 🍖 🍺<br>
        💸 💸 💸 💸 💸 💸 💸 💸
        </div>
        """,
        unsafe_allow_html=True
    )

st.snow()

# =====================================
# ADMIN
# =====================================

else:

    senha = st.text_input(
        "Senha do admin",
        type="password"
    )

    if senha != ADMIN_PASSWORD:

        st.warning(
            "🔒 Acesso restrito."
        )

        st.stop()

    st.subheader(
        "🏆 Administração do Bolão"
    )

    total_participantes = len(df)

    arrecadado = (
        total_participantes
        * VALOR_APOSTA
    )

    premio = (
        arrecadado * 0.50
    )

    churrasco = (
        arrecadado * 0.50
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Participantes",
            total_participantes
        )

    with col2:
        st.metric(
            "Prêmio",
            f"R$ {premio:,.2f}"
        )

    with col3:
        st.metric(
            "Churrasco",
            f"R$ {churrasco:,.2f}"
        )

    st.markdown("---")

    if st.button(
        "🧨 Zerar bolão"
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

    if st.button(
        "Calcular vencedor"
    ):

        def calcular_erro(linha):

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

        df["Erro Total"] = df.apply(
            calcular_erro,
            axis=1
        )

        ranking = df.sort_values(
            "Erro Total"
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
                    "Erro Total"
                ]
            ],
            use_container_width=True
        )
