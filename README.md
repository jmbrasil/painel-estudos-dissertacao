# Painel — estudos da dissertação sobre a PSR no Rio de Janeiro (2024)

Painel interativo com resultados da dissertação de mestrado de João Marcelo Guimarães Brasil (FGV EBAPE)
sobre a população em situação de rua (PSR) no município do Rio de Janeiro, em abas:

- Dados do Rio de Janeiro: PSR por método de coleta, resumo do município e I de Moran;
- Quadrats: PSR nas células de 1 km da Grade Estatística do IBGE com e sem cada referência;
- Decaimento por distância: histograma da distância da PSR à referência mais próxima;
- Índice de proximidade Observada sobre Esperada: PSR observada no raio / PSR esperada sob aleatoriedade
  na área habitável (26 raios, de 100 m a 8 km);
- Dissimilaridade (D de Duncan) e dissimilaridade local;
- Agenda futura: cenas de uso por zona e sobre o mapa de grupos armados.

Os dados são agregados (tabelas, contagens por faixa de distância e imagens dos mapas); as cenas de uso
aparecem só em células ou com posição deslocada.

Para rodar localmente:

    pip install -r requirements.txt
    streamlit run app_indice_proximidade.py

Os arquivos deste repositório são cópias geradas a partir do repositório da dissertação.
