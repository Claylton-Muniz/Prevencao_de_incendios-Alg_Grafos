# Sistema de Combate a Incêndios Florestais

## Este repositório contém um projeto prático criado para resolver o problema proposto na disciplina de Algoritmos em Grafos, ministrada pelo professor Dr. Carlos Vinicius G. C. Lima da Universidade Federal do Cariri (UFCA)

O projeto foi desenvolvido usando exclusivamente a linguagem de programação Python e duas de suas bibliotecas: matplotlib (Para a visualização do grafo) e a networkx (que auxilia a matplotlib).
A descrição detalhada do problema proposto está disponível no arquivo descriçãoProblema.pdf
Descrição resumida do problema:
-Criar um grafo, com diversos vértices e arestas que simulam áreas florestais;
-Distribuir postos de brigadistas;
-Distribuir pontos de coleta de água;
-Simular a propagação do fogo;
-Simular a movimentação das brigadas;
-Simular o combate ao incêndio em cada vértice em chama;
-Detalhar cada ação no gravo a cada instante de tempo simulado;
-Especificar o resultado Final do cenário simulado;

Descrição resumida da implementação:
-A distribuição dos postos, pontos de coleta e início do incêndio são lidas de um arquivo.txt base;
-A distribuição é simulada por meio da implementação de um grafo conexo e não direcionado;
-A propagação do fogo e o movimento dos brigadistas e simulado a cada instante de tempo;
-Os vértices em chamas e a quantidade de água de cada brigada é mostrada no console junto com as demais informações a cada instante;
-A simulação é finalizada quando não há mais nenhum vértice em chamas;
