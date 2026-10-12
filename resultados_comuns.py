# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""
resultados_comuns.py — Funções das abas de resultados do painel: ler as tabelas e imagens preparadas por
painel/gera_dados_painel_resultados.py e mostrá-las no formato da dissertação.
"""

import json
import os

import pandas as pd
import streamlit as st

from config_painel import PASTA_PAINEL_RESULTADOS

# referências das figuras compostas de quadrats e de dissimilaridade, na ordem da dissertação
REFERENCIAS_MAPAS = {"Cenas de uso": "cenas_de_uso", "População residente": "populacao_residente",
                     "Pontos de ônibus": "pontos_de_onibus", "Estações de trem": "estacoes_de_trem",
                     "Estações de metrô": "estacoes_de_metro", "Paradas do VLT": "paradas_do_vlt",
                     "Escolas": "escolas", "Unidades de saúde": "unidades_de_saude",
                     "Delegacias e batalhões": "delegacias_e_batalhoes"}
# calculadas só para o painel, com o mesmo método (pipeline_limpeza/gera_analises_referencias_extras_2024.py)
FORA_DA_DISSERTACAO = {"Escolas", "Unidades de saúde", "Delegacias e batalhões"}
AVISO_FORA = ("Escolas, unidades de saúde e delegacias e batalhões não estão na dissertação: foram calculadas só "
              "para este painel, com o mesmo método das outras referências.")

# mesmas cores do índice de proximidade
CORES = {"Pontos de ônibus": "#185FA5", "Estações de trem": "#6A4C93", "Estações de metrô": "#E76F51",
         "Paradas do VLT": "#F4A261", "Cenas de uso": "#555555", "Escolas": "#2A9D8F", "Unidades de saúde": "#B5838D",
         "Delegacias e batalhões": "#A32D2D"}


def caminho(arquivo):
    return os.path.join(PASTA_PAINEL_RESULTADOS, arquivo)


def conferir_pasta():
    if not os.path.exists(caminho("tabelas_metadados.parquet")):
        st.error("Dados das abas de resultados não encontrados. Gere com `python painel/gera_dados_painel_resultados.py`.")
        st.stop()


@st.cache_data
def ler_parquet(arquivo, modificado_em):  # modificado_em invalida o cache quando o arquivo muda
    return pd.read_parquet(caminho(arquivo))


def ler(arquivo):
    return ler_parquet(arquivo, os.path.getmtime(caminho(arquivo)))


def numero_br(valor, decimais):
    if pd.isna(valor):
        return "—"
    return f"{valor:,.{decimais}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def mostrar_tabela(nome, numero):
    """Tabela da dissertação com título, nota e fonte; números no formato brasileiro e ordenáveis pelo cabeçalho."""
    conferir_pasta()
    meta = ler("tabelas_metadados.parquet").set_index("tabela").loc[nome]
    df = ler(f"tabela_{nome}.parquet")
    decimais = json.loads(meta["decimais"])
    st.subheader(f"Tabela {numero} – {meta['titulo']}")
    formatos = {col: (lambda v, d=d: numero_br(v, d)) for col, d in decimais.items()}
    st.dataframe(df.style.format(formatos), hide_index=True, width="stretch")
    legendas = ["Clique no nome de uma coluna para ordenar a tabela."]
    if "Na dissertação" in df.columns:
        legendas.append(f"Linhas com “Não” em “Na dissertação”: {AVISO_FORA[0].lower()}{AVISO_FORA[1:]}")
    if meta["nota"]:
        legendas.append(f"**Nota:** {meta['nota']}")
    if meta["fonte"]:
        legendas.append(f"**Fonte:** {meta['fonte']}")
    st.caption("  \n".join(legendas))


def escolher_e_mostrar_mapa(prefixo, rotulo, chave):
    """Escolha da referência e mapa recortado da figura composta da dissertação."""
    conferir_pasta()
    referencia = st.radio(rotulo, list(REFERENCIAS_MAPAS), horizontal=True, key=chave)
    if referencia in FORA_DA_DISSERTACAO:
        st.info(AVISO_FORA)
    st.image(caminho(f"{prefixo}_{REFERENCIAS_MAPAS[referencia]}.png"), width="stretch")
    return referencia
