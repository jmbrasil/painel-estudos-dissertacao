# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""paginas/dissimilaridade.py — Aba do índice de dissimilaridade (D de Duncan) e da dissimilaridade local."""

import streamlit as st

from resultados_comuns import escolher_e_mostrar_mapa, escolher_zona, mostrar_tabela, mostrar_tabela_zona

st.title("Índice de Dissimilaridade (D de Duncan) e Gráfico de Dissimilaridade Local")
zona = escolher_zona("zona_dissimilaridade")

st.subheader("Dissimilaridade local da PSR 2024 nas células de 1 km da Grade Estatística do IBGE"
             + (f", {zona['nome']}" if zona else ""))
escolher_e_mostrar_mapa("dissimilaridade", "Referência do mapa", "referencia_dissimilaridade", extensao="jpg", zona=zona)
st.caption(
    "Dissimilaridade local: diferença, em pontos percentuais, entre a fatia da PSR e a fatia da referência em cada "
    + ("célula. A área do círculo é proporcional ao valor absoluto da diferença, na mesma escala em todos os mapas.  \n"
       if zona is None else
       "pedaço de célula recortado pela zona, com as fatias sobre os totais da zona. A área do círculo é proporcional ao "
       "valor absoluto da diferença, na mesma escala em todos os mapas por zona e na figura do apêndice de zonas da "
       "dissertação (diferente da escala dos mapas do município).  \n")
    +
    "**Fonte:** Elaboração própria a partir do censo de PSR de 2024 (IPP), das cenas de uso registradas no censo, "
    "da Grade Estatística do Censo 2022 (IBGE), dos pontos de parada do SPPO (DATA.RIO; pontos de ônibus) e do OpenStreetMap "
    "(via NextGIS Data; trem, metrô e VLT), sobre imagem de satélite do Google "
    "em tons de cinza."
)

if zona:
    mostrar_tabela_zona("duncan", 6, zona)
else:
    mostrar_tabela("duncan_psr_referencias_2024", 6)
