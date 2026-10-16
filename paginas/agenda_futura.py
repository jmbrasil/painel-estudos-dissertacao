# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""paginas/agenda_futura.py — Aba com a agenda futura: cenas de uso por zona e sobre o mapa de grupos armados."""

import streamlit as st

from resultados_comuns import LARGURA_MAPA_PX, caminho, conferir_pasta, mostrar_tabela

st.title("Agenda futura")

conferir_pasta()
st.subheader("Cenas abertas de uso de drogas em 2024 sobre mapa de grupos armados")
st.image(caminho("cenas_sobre_mapa_fogo_cruzado.jpg"), width=LARGURA_MAPA_PX)
st.caption(
    "Mapa de áreas sob controle de grupos armados de 2024 "
    "([Instituto Fogo Cruzado, 2026](https://fogocruzado.org.br/mapadosgruposarmados/)). "
    "Tons fortes: controle territorial armado; tons claros: influência territorial armada. "
    "Laranja: ADA; vermelho: CV; azul: milícia; verde: TCP. Círculos brancos: cenas de uso, com a posição "
    "deslocada aleatoriamente (de 102 a 998 m) para não revelar a localização exata."
)

mostrar_tabela("cenas_por_zona_2024", 7)
