# CÓPIA GERADA por painel/publicar_painel.py do repositório fgv_dissertacao_python.
# No repositório do painel, os dados ficam ao lado do app (na dissertação, em output/arquivos/).
import os

_PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_INDICE_PROXIMIDADE = os.path.join(_PASTA, "indice_proximidade_psr_equipamentos_2024.parquet")
PASTA_PAINEL_RESULTADOS = os.path.join(_PASTA, "painel_resultados")
# Imagens servidas direto do GitHub: no Streamlit Cloud, o endereço de mídia do Streamlit (/~/+/media/...) devolvia 404 e
# os mapas não apareciam, embora os arquivos estivessem no app (2026-10-15). Localmente funcionava.
URL_IMAGENS_PAINEL = "https://raw.githubusercontent.com/jmbrasil/painel-estudos-dissertacao/main/painel_resultados"
