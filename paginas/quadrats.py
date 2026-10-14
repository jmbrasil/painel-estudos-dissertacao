# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""paginas/quadrats.py — Aba da análise por quadrats (células de 1 km da Grade Estatística do IBGE)."""

import streamlit as st

from resultados_comuns import escolher_e_mostrar_mapa, escolher_zona, mostrar_tabela, mostrar_tabela_zona

st.title("Quadrats")
zona = escolher_zona("zona_quadrats")

st.subheader("Células de 1 km por presença de PSR e da referência, 2024" + (f", {zona['nome']}" if zona else ""))
escolher_e_mostrar_mapa("quadrats", "Referência do mapa", "referencia_quadrats", zona=zona)
st.caption(
    "Células sem PSR e sem a referência ficam sem cor (só o fundo de satélite). População residente: células com ao menos um morador. "
    "Para não revelar a localização exata das cenas, o mapa mostra apenas as células.  \n"
    "**Fonte:** Elaboração própria a partir do censo de PSR de 2024 (IPP), das cenas de uso registradas no censo, "
    "da Grade Estatística do Censo 2022 (IBGE), dos pontos de parada do SPPO (DATA.RIO; pontos de ônibus), do OpenStreetMap "
    "(via NextGIS Data; trem, metrô e VLT) e da camada Limite de Bairros (DATA.RIO), "
    "sobre imagem de satélite do Google em tons de cinza."
)

if zona:
    mostrar_tabela_zona("quadrats", 4, zona)
else:
    mostrar_tabela("quadrats_psr_referencias_2024", 4)
