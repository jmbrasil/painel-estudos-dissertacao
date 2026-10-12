# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""paginas/dados_rio.py — Aba com os dados gerais da PSR de 2024 e do município do Rio de Janeiro."""

import streamlit as st

from resultados_comuns import mostrar_tabela

st.title("Dados do Rio de Janeiro")

mostrar_tabela("psr_metodo_questionario_2024", 1)
mostrar_tabela("resumo_municipio_rio", 2)
mostrar_tabela("moran_grade_variaveis_2024", 3)
