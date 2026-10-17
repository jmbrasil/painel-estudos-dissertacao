# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# Não edite aqui: edite o arquivo de mesmo nome em painel/ lá e publique de novo.
"""paginas/dissimilaridade.py — Aba do índice de dissimilaridade (D de Duncan) e da dissimilaridade local."""

import streamlit as st

from resultados_comuns import (escolher_referencia, escolher_zona, mostrar_mapa_referencia, mostrar_tabela,
                               mostrar_tabela_zona)

# sem st.title: o título da aba ocupava muito espaço acima do mapa (pedido do usuário em 2026-10-17); pelo mesmo motivo,
# menos espaço no topo da página e o título do mapa em texto normal (o mapa já traz o próprio título)
st.markdown("<style>.block-container {padding-top: 2.5rem;}</style>", unsafe_allow_html=True)

# Seletores à direita do mapa, para rolar menos (pedido do usuário em 2026-10-17). A coluna da direita é preenchida
# antes, porque o título e o mapa dependem das escolhas.
coluna_mapa, coluna_seletores = st.columns([0.68, 0.32], gap="large")
with coluna_seletores:
    zona = escolher_zona("zona_dissimilaridade", texto_pequeno=True)
    # Seletor do que o mapa mostra (pedido do usuário em 2026-10-16): as bolhas da dissimilaridade local por célula ou os
    # próprios pontos de PSR e da referência (mapas de painel/gera_dados_painel_zonas.py, função mapas_pontos)
    MODOS = {"Dissimilaridade local (círculos por célula)": "dissimilaridade", "Pontos de PSR e da referência": "pontos"}
    modo = MODOS[st.radio("Mostrar no mapa", list(MODOS), key="modo_mapa_dissimilaridade")]
    referencia = escolher_referencia("Referência do mapa", "referencia_dissimilaridade")
with coluna_mapa:
    st.markdown("**" + ("Dissimilaridade local da PSR 2024 nas células de 1 km da Grade Estatística do IBGE"
                        if modo == "dissimilaridade" else "PSR 2024 e pontos da referência")
                + (f", {zona['nome']}" if zona else "") + "**")
    # altura do mapa limitada a 1/1,25 da largura da coluna (1/1,5 até 2026-10-17; o usuário achou pequeno num MacBook
    # Air): o mapa do município ocupa a coluna inteira; o do Centro, mais alto que largo, fica mais estreito
    mostrar_mapa_referencia(modo, referencia, extensao="jpg", zona=zona, largura_por_altura=1.25)
FONTE_MAPAS = (
    "**Fonte:** Elaboração própria a partir do censo de PSR de 2024 (IPP), das cenas de uso registradas no censo, "
    "da Grade Estatística do Censo 2022 (IBGE), dos pontos de parada do SPPO (DATA.RIO; pontos de ônibus) e do OpenStreetMap "
    "(via NextGIS Data; trem, metrô e VLT), sobre imagem de satélite do Google em tons de cinza."
)
if modo == "pontos":
    st.caption(
        "Pontos vermelhos: PSR na coordenada registrada no censo; pessoas na mesma coordenada formam um único ponto, maior "
        "quanto mais pessoas (até 40). Pontos azuis: a referência na posição real. Cenas de uso (bolas brancas com contorno "
        "preto): posição deslocada ao acaso (jitter de 100 a 1.000 m), para não revelar onde estão; por isso o número de "
        "cenas no mapa de uma zona pode diferir do usado nos testes, que usam a posição real. População residente: as "
        "células coloridas pela população. Linhas tracejadas: células de 1 km da Grade Estatística do IBGE.  \n"
        + FONTE_MAPAS
    )
else:
    st.caption(
        "Dissimilaridade local: diferença, em pontos percentuais, entre a fatia da PSR e a fatia da referência em cada "
        + ("célula. A área do círculo é proporcional ao valor absoluto da diferença, na mesma escala em todos os mapas.  \n"
           if zona is None else
           "pedaço de célula recortado pela zona, com as fatias sobre os totais da zona. A área do círculo é proporcional ao "
           "valor absoluto da diferença, na mesma escala em todos os mapas por zona e na figura do apêndice de zonas da "
           "dissertação (diferente da escala dos mapas do município).  \n")
        + FONTE_MAPAS
    )

if zona:
    mostrar_tabela_zona("duncan", 6, zona)
else:
    mostrar_tabela("duncan_psr_referencias_2024", 6)
