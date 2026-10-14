# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""
paginas/decaimento.py — Aba do decaimento por distância: histograma da distância de cada PSR de 2024 ao ponto
mais próximo de cada referência, com escolha das referências, da faixa e da distância máxima.

Lê as contagens em faixas de 50 m (decaimento_faixas_50m.parquet e, para as referências que não estão na dissertação,
decaimento_faixas_50m_extras.parquet) e as junta nas faixas escolhidas.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from resultados_comuns import AVISO_FORA, CORES, FORA_DA_DISSERTACAO, conferir_pasta, ler, mostrar_tabela, numero_br

st.title("Decaimento por distância")
conferir_pasta()

faixas = pd.concat([ler("decaimento_faixas_50m.parquet"), ler("decaimento_faixas_50m_extras.parquet")])
referencias = [r for r in CORES if r in set(faixas["referencia"])]
na_dissertacao = [r for r in referencias if r not in FORA_DA_DISSERTACAO]

col1, col2 = st.columns([3, 2])
with col1:
    selecionadas = st.multiselect("Referências", referencias, default=na_dissertacao,
                                  help=AVISO_FORA)
    distancia_max = st.slider("Distância máxima no gráfico (m)", min_value=500, max_value=10_000, value=1_500, step=250)
with col2:
    largura = st.select_slider("Largura da faixa (m)", options=[50, 100, 200, 250, 500], value=100)
    eixo_pct = st.radio("Eixo y", ["Número de PSR", "% da PSR"], horizontal=True) == "% da PSR"
    separado = st.radio("Exibição", ["Um painel por referência", "Sobrepostas"], horizontal=True) == "Um painel por referência"

if not selecionadas:
    st.info("Escolha ao menos uma referência.")
    st.stop()

if separado:
    fig = make_subplots(rows=len(selecionadas), cols=1, shared_xaxes=True, vertical_spacing=0.06,
                        subplot_titles=selecionadas)
else:
    fig = go.Figure()

acima_max = {}
for i, rotulo in enumerate(selecionadas, start=1):
    t = faixas[faixas["referencia"] == rotulo]
    total = t["n_psr"].sum()
    t = t[t["inicio_m"] < distancia_max].assign(faixa=lambda d: d["inicio_m"] // largura * largura)
    contagem = t.groupby("faixa")["n_psr"].sum()
    acima_max[rotulo] = total - contagem.sum()
    y = 100 * contagem / total if eixo_pct else contagem
    barra = go.Bar(
        x=contagem.index + largura / 2, y=y, width=largura * 0.85, name=rotulo, marker_color=CORES[rotulo],
        opacity=1 if separado else 0.55, showlegend=not separado,
        customdata=list(zip(contagem.index, contagem.index + largura, contagem, 100 * contagem / total)),
        hovertemplate=(f"<b>{rotulo}</b><br>%{{customdata[0]:,.0f}} a %{{customdata[1]:,.0f}} m<br>"
                       "%{customdata[2]:,.0f} PSR (%{customdata[3]:.1f}% da PSR)<extra></extra>"),
    )
    if separado:
        fig.add_trace(barra, row=i, col=1)
    else:
        fig.add_trace(barra)

# uma linha na mediana de cada referência, como na figura da dissertação (pedido do usuário em 2026-10-12; antes, linhas
# em 500 m e 1 km). A mediana vem da Tabela 5 (distância exata), não das faixas de 50 m.
medianas = ler("tabela_decaimento_psr_referencias_2024.parquet").set_index("Referência")["Mediana (m)"]
for k, rotulo in enumerate(selecionadas):
    mediana = medianas[rotulo]
    cor = "#EF9F27" if separado else CORES[rotulo]
    alvo = dict(row=k + 1, col=1) if separado else {}
    y_rotulo = 0.97 if separado else 0.97 - 0.07 * k  # sobrepostas: um rótulo embaixo do outro
    texto = f"mediana{'' if separado else ' (' + rotulo + ')'}: {numero_br(mediana, 0)} m"
    if mediana < distancia_max:
        fig.add_vline(x=mediana, line=dict(color=cor, dash="dot", width=2), **alvo)
        fig.add_annotation(x=mediana, y=y_rotulo, xref="x", yref="y domain", text=f"<b>{texto}</b>", showarrow=False,
                           xanchor="left", yanchor="top", xshift=4, font=dict(color="#b36b00" if separado else cor),
                           bgcolor="rgba(255,255,255,0.85)", **alvo)
    else:  # mediana além da distância máxima do gráfico: rótulo com seta na borda direita
        fig.add_annotation(x=distancia_max, y=y_rotulo, xref="x", yref="y domain", text=f"<b>{texto} →</b>",
                           showarrow=False, xanchor="right", yanchor="top", font=dict(color="#b36b00" if separado else cor),
                           bgcolor="rgba(255,255,255,0.85)", **alvo)

titulo_y = "% da PSR" if eixo_pct else "Número de PSR"
fig.update_layout(
    barmode="overlay", separators=",.", plot_bgcolor="white", paper_bgcolor="white",
    height=max(450, 230 * len(selecionadas)) if separado else 560,
    legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
    margin=dict(t=60 if separado else 30),
)
fig.update_xaxes(range=[0, distancia_max], tickformat=",.0f", showgrid=False)
fig.update_xaxes(title_text=f"Distância ao ponto mais próximo da referência (m), faixas de {largura} m",
                 row=len(selecionadas) if separado else None, col=1 if separado else None)
fig.update_yaxes(title_text=titulo_y, gridcolor="#e0dfd7", rangemode="tozero")
if not eixo_pct:  # teste (2026-10-14): eixo y fixo em 4.000 PSR em todos os painéis
    fig.update_yaxes(range=[0, 4000])
# fundo branco e texto escuro fixos, sem o tema do Streamlit: no modo escuro, o tema punha texto claro sobre o fundo
# branco do gráfico e títulos, eixos e legenda sumiam (2026-10-12)
fig.update_layout(template="plotly_white", font=dict(color="#31333F"))
st.plotly_chart(fig, width="stretch", theme=None)

st.caption(
    "Distância em linha reta de cada PSR (8.195) ao ponto mais próximo da referência. A linha pontilhada marca a "
    "mediana da distância; quando ela passa da distância máxima do gráfico, aparece só o rótulo com a seta, na borda "
    "direita. Fora do gráfico (acima da distância máxima): "
    + "; ".join(f"{r}: {numero_br(acima_max[r], 0)} PSR" for r in selecionadas) + "."
    + (f" {AVISO_FORA}" if FORA_DA_DISSERTACAO & set(selecionadas) else "")
)

mostrar_tabela("decaimento_psr_referencias_2024", 5)
