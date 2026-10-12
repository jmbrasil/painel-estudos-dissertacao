# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""paginas/quadrats.py — Aba da análise por quadrats (células de 1 km da Grade Estatística do IBGE)."""

import streamlit as st

from resultados_comuns import escolher_e_mostrar_mapa, mostrar_tabela

st.title("Quadrats")

mostrar_tabela("quadrats_psr_referencias_2024", 4)

st.subheader("Células de 1 km por presença de PSR e da referência, 2024")
escolher_e_mostrar_mapa("quadrats", "Referência do mapa", "referencia_quadrats")
st.caption(
    "Células sem PSR e sem a referência ficam em branco. População residente: células com ao menos um morador. "
    "Para não revelar a localização exata das cenas, o mapa mostra apenas as células.  \n"
    "**Fonte:** Elaboração própria a partir do censo de PSR de 2024 (IPP), das cenas de uso registradas no censo, "
    "da Grade Estatística do Censo 2022 (IBGE), do OpenStreetMap (via NextGIS Data) e da camada Limite de Bairros (DATA.RIO)."
)
