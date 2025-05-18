# Sistema de Combate a Incêndios Florestais

## Este repositório contém um projeto prático criado para resolver o problema proposto na disciplina de Algoritmos em Grafos, ministrada pelo professor Dr. Carlos Vinicius G. C. Lima da Universidade Federal do Cariri (UFCA)

O projeto foi desenvolvido usando exclusivamente a linguagem de programação Python e duas de suas bibliotecas: matplotlib (Para a visualização do grafo) e a networkx (que auxilia a matplotlib).
A descrição detalhada do problema proposto está disponível no arquivo descriçãoProblema.pdf<br>
Descrição resumida do problema: <br>
-Criar um grafo, com diversos vértices e arestas que simulam áreas florestais;<br>
-Distribuir postos de brigadistas;<br>
-Distribuir pontos de coleta de água;<br>
-Simular a propagação do fogo;<br>
-Simular a movimentação das brigadas;<br>
-Simular o combate ao incêndio em cada vértice em chama;<br>
-Detalhar cada ação no gravo a cada instante de tempo simulado;<br>
-Especificar o resultado Final do cenário simulado;<br>


Descrição resumida da implementação:<br>
-A distribuição dos postos, pontos de coleta e início do incêndio são lidas de um arquivo.txt base;<br>
-A distribuição é simulada por meio da implementação de um grafo conexo e não direcionado;<br>
-A propagação do fogo e o movimento dos brigadistas e simulado a cada instante de tempo;<br>
-Os vértices em chamas e a quantidade de água de cada brigada é mostrada no console junto com as demais informações a cada instante;<br>
-A simulação é finalizada quando não há mais nenhum vértice em chamas;<br>
