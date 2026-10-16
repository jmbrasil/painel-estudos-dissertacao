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
# Largura dos mapas na tela: com width="stretch" e a página em modo largo, o mapa ocupava a janela inteira e era preciso
# rolar para ver a imagem e a legenda (pedido do usuário em 2026-10-15). O mapa fica numa coluna com esta fração da
# largura da página. Não usar width=<pixels> no st.image: no Streamlit Cloud as imagens sumiram (funcionava localmente).
FRACAO_LARGURA_MAPA = 0.6


def mostrar_mapa(arquivo):
    coluna, _ = st.columns([FRACAO_LARGURA_MAPA, 1 - FRACAO_LARGURA_MAPA])
    coluna.image(arquivo, width="stretch")


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


def escolher_e_mostrar_mapa(prefixo, rotulo, chave, extensao="jpg", zona=None):
    """Escolha da referência e mapa recortado da figura composta da dissertação (ou o mapa da zona escolhida)."""
    conferir_pasta()
    referencia = st.radio(rotulo, list(REFERENCIAS_MAPAS), horizontal=True, key=chave)
    if referencia in FORA_DA_DISSERTACAO:
        st.info(AVISO_FORA)
    if zona is None:
        mostrar_mapa(caminho(f"{prefixo}_{REFERENCIAS_MAPAS[referencia]}.{extensao}"))
    else:
        arquivo = caminho(f"zonas/{prefixo}_{zona['slug']}_{REFERENCIAS_MAPAS[referencia]}.jpg")
        if os.path.exists(arquivo):
            mostrar_mapa(arquivo)
        else:
            st.info(f"{referencia}: menos de {MIN_PONTOS_ZONA} pontos {zona['em']}; o mapa e o índice não são calculados.")
    return referencia


# ---------------------------------------------------------------- recorte por zona da cidade
# Dados de painel/gera_dados_painel_zonas.py, em painel_resultados/zonas/ (pedido do usuário em 2026-10-14).
RECORTES = ["Município", "Centro", "Zona Sul", "Zona Norte", "Zona Sudoeste", "Zona Oeste"]
MIN_PONTOS_ZONA = 5


def escolher_zona(chave):
    """Seletor do recorte no topo da aba: o município ou uma zona. A escolha passa para as outras abas.

    Devolve None para o município ou um dict com zona (código das tabelas), nome, slug e os totais da zona.
    """
    if not os.path.exists(caminho("zonas/resumo_zonas.parquet")):
        st.caption("Recorte por zona indisponível: gere com `python painel/gera_dados_painel_zonas.py`.")
        return None
    # cada aba tem o seu widget (chave própria); a escolha fica em zona_painel para valer nas outras abas
    atual = st.session_state.get("zona_painel", "Município")
    nome = st.radio("Recorte", RECORTES, index=RECORTES.index(atual), horizontal=True, key=chave,
                    help="Município: os resultados da dissertação. Zona: as mesmas análises dentro da zona, "
                         "como no apêndice de zonas da dissertação.")
    st.session_state["zona_painel"] = nome
    if nome == "Município":
        return None
    zona = ler("zonas/resumo_zonas.parquet").set_index("nome").loc[nome].to_dict()
    zona["nome"] = nome
    zona["em"] = "no Centro" if nome == "Centro" else f"na {nome}"  # "no Centro", "na Zona Sul"
    st.caption(
        f"**{nome}:** {numero_br(zona['n_psr'], 0)} PSR, {numero_br(zona['n_cenas'], 0)} cenas de uso, "
        f"{numero_br(zona['n_bairros'], 0)} bairros e {numero_br(zona['n_celulas'], 0)} células de 1 km (recortadas "
        f"pelos limites da zona). {zona['descricao']}"
        + (" Com tão poucas cenas, os resultados das cenas na zona são frágeis." if zona["n_cenas"] < 20 else "")
    )
    return zona


def mostrar_tabela_zona(nome, numero, zona):
    """Versão por zona das Tabelas 4, 5 e 6, no mesmo formato de mostrar_tabela."""
    meta = ler("zonas/tabelas_metadados.parquet").set_index("tabela").loc[nome]
    df = ler(f"zonas/tabela_{nome}.parquet")
    df = df[df["zona"] == zona["zona"]].drop(columns="zona")
    decimais = json.loads(meta["decimais"])
    st.subheader(f"Tabela {numero} por zona – {meta['titulo'].format(zona=zona['nome'])}")
    formatos = {col: (lambda v, d=d: numero_br(v, d)) for col, d in decimais.items()}
    st.dataframe(df.style.format(formatos), hide_index=True, width="stretch")
    legendas = ["Clique no nome de uma coluna para ordenar a tabela.", meta["na_dissertacao"],
                f"**Nota:** {meta['nota']}", f"**Fonte:** {meta['fonte']}"]
    st.caption("  \n".join(legendas))
