# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""
app_indice_proximidade.py — Ponto de entrada do painel de estudos da dissertação (PSR 2024 no Rio de Janeiro).

Monta a navegação por abas no topo da página; cada aba é um script em paginas/. O nome do arquivo ficou o do
primeiro painel (só o índice de proximidade) porque é o arquivo principal configurado no Streamlit Community
Cloud (https://github.com/jmbrasil/painel-estudos-dissertacao); trocar o nome exigiria recriar o app lá.

Dados das abas:
  - Índice de proximidade: parquet do pipeline (pipeline_limpeza/gera_indice_proximidade_equipamentos.py);
  - demais abas: output/arquivos/painel_resultados/, gerado por painel/gera_dados_painel_resultados.py
    a partir das tabelas e figuras da dissertação.

Rodar no terminal do conda (a partir da raiz do repo):
    streamlit run painel/app_indice_proximidade.py
"""

import importlib
import sys

import streamlit as st

# O Streamlit Community Cloud roda de novo este arquivo e as abas a cada push, mas mantém na memória os módulos já
# importados: depois de uma mudança em resultados_comuns.py, as abas novas chamavam a versão antiga das funções
# (TypeError em 2026-10-12). Recarregar os módulos do painel a cada execução evita isso; config_painel antes, porque
# resultados_comuns importa dele.
for _modulo in ("config_painel", "resultados_comuns"):
    if _modulo in sys.modules:
        importlib.reload(sys.modules[_modulo])

st.set_page_config(page_title="PSR no Rio de Janeiro — estudos da dissertação", layout="wide")

paginas = [
    st.Page("paginas/dados_rio.py", title="Dados do Rio de Janeiro", default=True),
    st.Page("paginas/quadrats.py", title="Quadrats"),
    st.Page("paginas/decaimento.py", title="Decaimento por distância"),
    # aba oculta em 2026-10-13 (pedido do usuário); a página continua em paginas/indice_proximidade.py
    # st.Page("paginas/indice_proximidade.py", title="Índice de proximidade Observada sobre Esperada"),
    st.Page("paginas/dissimilaridade.py", title="Dissimilaridade (D de Duncan)"),
    st.Page("paginas/agenda_futura.py", title="Agenda futura"),
]
st.navigation(paginas, position="top").run()
