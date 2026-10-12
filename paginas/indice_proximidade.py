# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""
paginas/indice_proximidade.py — Aba do painel com o índice de proximidade da PSR 2024 a cenas de
uso e equipamentos urbanos (aberta pelo app_indice_proximidade.py, que monta a navegação).

    índice(r) = PSR observada no raio / PSR esperada no raio sob aleatoriedade na área habitável

Mesma figura de analises/analise_indice_de_comparacao_de_correlacao.ipynb, com escolha das
referências e da faixa de raio. Não calcula nada: lê o parquet gerado no pipeline por
pipeline_limpeza/gera_indice_proximidade_equipamentos.py (26 raios, de 100 m a 8 km).

Rodar com no terminal do conda (a partir da raiz do repo):
    streamlit run painel/app_indice_proximidade.py
"""

import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config_painel import ARQUIVO_INDICE_PROXIMIDADE

# Mesmas cores e ordem da figura do notebook
CORES = {"Pontos de ônibus": "#185FA5", "Escolas": "#2A9D8F", "Delegacias e batalhões": "#A32D2D",
         "Estações de trem": "#6A4C93", "Estações de metrô": "#E76F51", "Paradas do VLT": "#F4A261",
         "Unidades de saúde": "#B5838D", "Cenas de uso": "#555555"}
TICKS_Y = [0.5, 1, 2, 5, 10, 20, 50]
RAIO_MAX_M = 8_000


def metros(valor):
    return f"{valor:,}".replace(",", ".")

st.title("Índice de proximidade Observada sobre Esperada")
st.caption(
    "Índice = PSR observada no raio ÷ PSR esperada no raio sob aleatoriedade. "
    "PSR esperada = PSR total × (área habitável no raio ÷ área habitável do município). "
    "\"No raio\" = dentro da união dos círculos de raio r em volta de todos os pontos do tipo. "
    "1 = o que o acaso daria; acima de 1 = mais PSR do que o acaso daria."
)


@st.cache_data
def carregar_indice(caminho: str, modificado_em: float) -> pd.DataFrame:  # modificado_em invalida o cache quando o parquet muda
    return pd.read_parquet(caminho)


if not os.path.exists(ARQUIVO_INDICE_PROXIMIDADE):
    st.error(
        "Parquet do índice não encontrado. Gere com "
        "`python pipeline_limpeza/gera_indice_proximidade_equipamentos.py` (ou `python run_all.py`)."
    )
    st.stop()

indice = carregar_indice(ARQUIVO_INDICE_PROXIMIDADE, os.path.getmtime(ARQUIVO_INDICE_PROXIMIDADE))
referencias = [r for r in CORES if r in set(indice["referencia"])]

with st.sidebar:
    st.header("Filtros")
    selecionadas = st.multiselect("Referências", options=referencias, default=referencias)
    raio_min, raio_max = st.slider("Raio inicial e final (m)", min_value=0, max_value=RAIO_MAX_M,
                                   value=(0, RAIO_MAX_M), step=50)
    escala_log = st.checkbox("Eixo y em escala logarítmica", value=True)
    st.caption(
        "Raios calculados: de 100 em 100 m até 1 km, de 250 em 250 m até 2 km e de 500 em 500 m até 8 km. "
        "A figura mostra os raios que caem dentro da faixa escolhida."
    )

dados = indice[indice["referencia"].isin(selecionadas) & indice["raio_m"].between(raio_min, raio_max)]
if not selecionadas:
    st.info("Escolha ao menos uma referência na barra lateral.")
    st.stop()
if dados.empty:
    st.warning(f"Nenhum raio calculado entre {metros(raio_min)} e {metros(raio_max)} m. Amplie a faixa.")
    st.stop()

fig = go.Figure()
for rotulo in selecionadas:
    t = dados[dados["referencia"] == rotulo].sort_values("raio_m")
    fig.add_trace(go.Scatter(
        x=t["raio_m"], y=t["indice"], name=rotulo, mode="lines+markers",
        line=dict(color=CORES[rotulo], width=2.5, dash="dash" if rotulo == "Cenas de uso" else "solid"),
        marker=dict(size=6),
        customdata=t[["psr_observada", "psr_esperada", "pct_psr", "pct_area_habitavel", "n_pontos"]].to_numpy(),
        hovertemplate=(
            f"<b>{rotulo}</b><br>raio: %{{x:,.0f}} m<br>índice: %{{y:.2f}}<br>"
            "PSR observada: %{customdata[0]:,.0f} (%{customdata[2]:.1f}% da PSR)<br>"
            "PSR esperada: %{customdata[1]:,.0f}<br>"
            "área habitável no raio: %{customdata[3]:.1f}%<br>"
            "pontos do tipo: %{customdata[4]:,.0f}<extra></extra>"
        ),
    ))
fig.add_hline(y=1, line=dict(color="gray", width=1, dash="dot"))

eixo_y = dict(title="PSR observada no raio ÷ PSR esperada no raio", gridcolor="#e0dfd7", zeroline=False)
if escala_log:
    ticks = [v for v in TICKS_Y if dados["indice"].min() * 0.8 <= v <= dados["indice"].max() * 1.5]
    eixo_y.update(type="log", tickvals=ticks, ticktext=[f"{v:g}".replace(".", ",") for v in ticks])
fig.update_layout(
    title=f"Índice: observada ÷ esperada sob aleatoriedade (1 = o acaso), raio de {metros(raio_min)} a {metros(raio_max)} m",
    xaxis=dict(title="Raio r (m)", range=[raio_min - 0.02 * (raio_max - raio_min), raio_max * 1.01],
               tickformat=",.0f", showgrid=False),
    yaxis=eixo_y,
    separators=",.",  # decimal com vírgula, milhar com ponto
    plot_bgcolor="white", paper_bgcolor="white", height=620,
    legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
    hovermode="closest",
)
# fundo branco e texto escuro fixos, sem o tema do Streamlit: no modo escuro, o tema punha texto claro sobre o fundo
# branco do gráfico e títulos, eixos e legenda sumiam (2026-10-12)
fig.update_layout(template="plotly_white", font=dict(color="#31333F"))
st.plotly_chart(fig, width="stretch", theme=None)

st.subheader("Valores do índice na faixa escolhida")
tabela = (dados.pivot(index="referencia", columns="raio_m", values="indice")
          .reindex([r for r in selecionadas])
          .rename(columns=lambda r: f"{metros(r)} m")
          .round(2))
tabela.index.name = "referência"
st.dataframe(tabela, width="stretch")

with st.expander("Dados completos da faixa escolhida (PSR observada, área, PSR esperada, índice)"):
    st.dataframe(dados.reset_index(drop=True), width="stretch", hide_index=True)
