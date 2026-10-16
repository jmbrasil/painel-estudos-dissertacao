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

from resultados_comuns import (AVISO_FORA, CORES, FORA_DA_DISSERTACAO, conferir_pasta, escolher_zona, ler, mostrar_tabela,
                               mostrar_tabela_zona, numero_br)

st.title("Decaimento por distância")
conferir_pasta()
zona = escolher_zona("zona_decaimento")

if zona is None:
    faixas = pd.concat([ler("decaimento_faixas_50m.parquet"), ler("decaimento_faixas_50m_extras.parquet")])
    # mediana da Tabela 5 (distância exata), não das faixas de 50 m
    medianas = ler("tabela_decaimento_psr_referencias_2024.parquet").set_index("Referência")["Mediana (m)"]
else:  # PSR da zona; a distância vai até o ponto mais próximo em qualquer lugar da cidade
    faixas = ler("zonas/decaimento_faixas_50m.parquet")
    faixas = faixas[faixas["zona"] == zona["zona"]]
    tabela_zona = ler("zonas/tabela_decaimento.parquet")
    tabela_zona = tabela_zona[tabela_zona["zona"] == zona["zona"]].set_index("Referência")
    medianas = tabela_zona["Mediana (m)"]
    sem_ponto = [r for r in CORES if r in tabela_zona.index and tabela_zona.loc[r, "Pontos na zona"] == 0]
    if sem_ponto:
        st.info(f"Sem ponto {zona['em']}: {', '.join(sem_ponto)}. Para essas referências, a distância vai até o "
                "ponto mais próximo fora da zona.")
referencias = [r for r in CORES if r in set(faixas["referencia"])]
na_dissertacao = [r for r in referencias if r not in FORA_DA_DISSERTACAO]

# os três controles numa linha, com menus em vez de sliders, para ocupar menos altura (pedido do usuário em 2026-10-14)
col1, col2, col3 = st.columns([4, 1.3, 1.3])
with col1:
    selecionadas = st.multiselect("Referências", referencias, default=na_dissertacao,
                                  help=AVISO_FORA)
DISTANCIAS = list(range(500, 10_001, 250))
with col2:
    distancia_max = st.selectbox("Distância máxima", DISTANCIAS, index=DISTANCIAS.index(1_500),
                                 format_func=lambda v: f"{numero_br(v, 0)} m")
with col3:
    largura = st.selectbox("Largura da faixa", [50, 100, 200, 250, 500], index=1, format_func=lambda v: f"{v} m")
# sem as opções "Eixo y" (% da PSR) e "Exibição" (sobrepostas) desde 2026-10-14, a pedido do usuário: número de PSR,
# um painel por referência, como na figura da dissertação

if not selecionadas:
    st.info("Escolha ao menos uma referência.")
    st.stop()

fig = make_subplots(rows=len(selecionadas), cols=1, shared_xaxes=True, vertical_spacing=0.06, subplot_titles=selecionadas)

acima_max = {}
y_max = 0
for i, rotulo in enumerate(selecionadas, start=1):
    t = faixas[faixas["referencia"] == rotulo]
    total = t["n_psr"].sum()
    t = t[t["inicio_m"] < distancia_max].assign(faixa=lambda d: d["inicio_m"] // largura * largura)
    contagem = t.groupby("faixa")["n_psr"].sum()
    acima_max[rotulo] = total - contagem.sum()
    y_max = max(y_max, contagem.max() if len(contagem) else 0)
    fig.add_trace(go.Bar(
        x=contagem.index + largura / 2, y=contagem, width=largura * 0.85, name=rotulo, marker_color=CORES[rotulo],
        showlegend=False,
        customdata=list(zip(contagem.index, contagem.index + largura, contagem, 100 * contagem / total)),
        hovertemplate=(f"<b>{rotulo}</b><br>%{{customdata[0]:,.0f}} a %{{customdata[1]:,.0f}} m<br>"
                       "%{customdata[2]:,.0f} PSR (%{customdata[3]:.1f}% da PSR)<extra></extra>"),
    ), row=i, col=1)

# uma linha na mediana de cada referência, como na figura da dissertação (pedido do usuário em 2026-10-12; antes, linhas
# em 500 m e 1 km). A mediana vem da Tabela 5 (distância exata), não das faixas de 50 m.
for k, rotulo in enumerate(selecionadas):
    mediana = medianas[rotulo]
    alvo = dict(row=k + 1, col=1)
    texto = f"mediana: {numero_br(mediana, 0)} m"
    if mediana < distancia_max:
        fig.add_vline(x=mediana, line=dict(color="#EF9F27", dash="dot", width=2), **alvo)
        fig.add_annotation(x=mediana, y=0.97, xref="x", yref="y domain", text=f"<b>{texto}</b>", showarrow=False,
                           xanchor="left", yanchor="top", xshift=4, font=dict(color="#b36b00"),
                           bgcolor="rgba(255,255,255,0.85)", **alvo)
    else:  # mediana além da distância máxima do gráfico: rótulo com seta na borda direita
        fig.add_annotation(x=distancia_max, y=0.97, xref="x", yref="y domain", text=f"<b>{texto} →</b>",
                           showarrow=False, xanchor="right", yanchor="top", font=dict(color="#b36b00"),
                           bgcolor="rgba(255,255,255,0.85)", **alvo)

fig.update_layout(separators=",.", plot_bgcolor="white", paper_bgcolor="white",
                  height=max(450, 230 * len(selecionadas)), margin=dict(t=60))
fig.update_xaxes(range=[0, distancia_max], tickformat=",.0f", showgrid=False)
fig.update_xaxes(title_text=f"Distância ao ponto mais próximo da referência (m), faixas de {largura} m",
                 row=len(selecionadas), col=1)
fig.update_yaxes(title_text="Número de PSR", gridcolor="#e0dfd7", rangemode="tozero")
# o mesmo eixo y em todos os painéis, até a maior barra das referências escolhidas (com a faixa e a distância máxima
# escolhidas) (pedido do usuário em 2026-10-14; antes, fixo em 4.000 PSR no município)
fig.update_yaxes(range=[0, 1.05 * y_max])
# fundo branco e texto escuro fixos, sem o tema do Streamlit: no modo escuro, o tema punha texto claro sobre o fundo
# branco do gráfico e títulos, eixos e legenda sumiam (2026-10-12)
fig.update_layout(template="plotly_white", font=dict(color="#31333F"))
st.plotly_chart(fig, width="stretch", theme=None)

st.caption(
    ("Distância em linha reta de cada PSR (8.195) ao ponto mais próximo da referência. " if zona is None else
     f"Distância em linha reta de cada PSR {zona['em']} ({numero_br(zona['n_psr'], 0)}) ao ponto mais próximo da "
     "referência, em qualquer lugar da cidade. ")
    + "A linha pontilhada marca a "
    "mediana da distância; quando ela passa da distância máxima do gráfico, aparece só o rótulo com a seta, na borda "
    "direita. Fora do gráfico (acima da distância máxima): "
    + "; ".join(f"{r}: {numero_br(acima_max[r], 0)} PSR" for r in selecionadas) + "."
    + (f" {AVISO_FORA}" if FORA_DA_DISSERTACAO & set(selecionadas) else "")
)

if zona:
    mostrar_tabela_zona("decaimento", 5, zona)
else:
    mostrar_tabela("decaimento_psr_referencias_2024", 5)
