# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""paginas/dissimilaridade.py — Aba do índice de dissimilaridade (D de Duncan) e da dissimilaridade local."""

import streamlit as st

from resultados_comuns import escolher_e_mostrar_mapa, mostrar_tabela

st.title("Índice de Dissimilaridade (D de Duncan) e Gráfico de Dissimilaridade Local")

mostrar_tabela("duncan_psr_referencias_2024", 6)

st.subheader("Dissimilaridade local da PSR 2024 nas células de 1 km da Grade Estatística do IBGE")
escolher_e_mostrar_mapa("dissimilaridade", "Referência do mapa", "referencia_dissimilaridade", extensao="jpg")
st.caption(
    "Dissimilaridade local: diferença, em pontos percentuais, entre a fatia da PSR e a fatia da referência em cada "
    "célula. A área do círculo é proporcional ao valor absoluto da diferença, na mesma escala em todos os mapas.  \n"
    "**Fonte:** Elaboração própria a partir do censo de PSR de 2024 (IPP), das cenas de uso registradas no censo, "
    "da Grade Estatística do Censo 2022 (IBGE), dos pontos de parada do SPPO (DATA.RIO; pontos de ônibus) e do OpenStreetMap "
    "(via NextGIS Data; trem, metrô e VLT), sobre imagem de satélite do Google "
    "em tons de cinza."
)
