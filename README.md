# Painel — índice de proximidade da PSR 2024

Painel interativo do índice de proximidade da população em situação de rua (PSR) de 2024 a cenas
abertas de uso de drogas e a equipamentos urbanos, no município do Rio de Janeiro. Parte da
dissertação de mestrado de João Marcelo Guimarães Brasil (FGV EBAPE).

    índice(r) = PSR observada no raio / PSR esperada no raio sob aleatoriedade na área habitável

O app lê `indice_proximidade_psr_equipamentos_2024.parquet`, com valores agregados por referência e raio (26 raios, de 100 m a 8 km).

Para rodar localmente:

    pip install -r requirements.txt
    streamlit run app_indice_proximidade.py

Os arquivos deste repositório são cópias geradas a partir do repositório da dissertação.
