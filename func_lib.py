import heapq
from networkx import draw, draw_networkx_edge_labels, spring_layout, get_edge_attributes
import matplotlib.pyplot as plt
import os
import shutil

import heapq

def dijkstra_path(G, source, target):
    dist = {node: float('inf') for node in G}
    prev = {node: None for node in G}
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        if u == target:
            break

        for neighbor, attrs in G[u].items():  # attrs contém as propriedades da aresta
            weight = attrs.get('weight', 1)  # Pega o peso da aresta, com valor padrão de 1
            alt = current_dist + weight
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u
                heapq.heappush(heap, (alt, neighbor))

    # Reconstruir o caminho
    path = []
    u = target
    while u is not None:
        path.append(u)
        u = prev[u]
    path.reverse()

    if path and path[0] == source:
        return path
    else:
        return []  # Caminho não encontrado


# modificado para fazer a largura de 1 só vertice
def bfs_mod(G, m, vert, alastramento, prioridade, postos, equipes):
    # python não tem ponteiros então isso está substituindo o u ← G[w].prox e o u ← u.prox
    for u in G[vert]:
        if m[u] == "verde":
            m[u] = "azul"  # É um posto
            if u not in postos + equipes:
                m[u] = "vermelho"
                heapq.heappush(alastramento, (prioridade + 1, u))

    return m


def criar_grafo(G, dados):
    for i in range(dados["num_vertices"]):
        G.add_node(f"V{i}")

    for aresta in dados["arestas"]:
        G.add_edge(f"V{aresta[0]}", f"V{aresta[2]}", weight=aresta[1])


def criar_imagem(G, pos, cores, edge_labels, pasta_imgs, passo, atual, alastramento):
    plt.figure(figsize=(8, 6))

    if passo == 0:
        plt.title(f"Passo {passo}: Fogo iniciou em {atual}")
    else:
        plt.title(
            f"Passo {passo}: Fogo se alastrou por {atual}"
            + "".join(f", {v[1]}" for v in alastramento)
        )

    draw(G, pos, with_labels=True, node_color=cores)
    draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    caminho_imagem = os.path.join(pasta_imgs, "slide.png")

    plt.savefig(caminho_imagem)
    plt.close()


def mostrar_grafo(G, dados, postos, coleta_agua, equipe):
    pasta_imgs = "imgs"

    # Cria a pasta se não existir, ou limpa se já existir
    if os.path.exists(pasta_imgs):
        shutil.rmtree(pasta_imgs)
    os.makedirs(pasta_imgs)

    origem = f"V{dados['fogo']}"

    # Layout e pesos das arestas
    pos = spring_layout(G, seed=42)
    edge_labels = get_edge_attributes(G, "weight")

    # Declaração inicial das marcas na BFS.
    # Alterei para verde e vermelho para fazer sentido com o fogo
    m = {v: ("azul" if v in postos else "verde") for v in G.nodes()}
    m[origem] = "vermelho"
    """
    Foi necessário fazer ela aqui para 
    diminuir a complexidade e não perder 
    as marcas nas iterações
    """

    passo = 0
    test_imp = -1

    alastramento = []
    heapq.heappush(alastramento, (0, origem))

    while alastramento:
        prioridade, atual = heapq.heappop(alastramento)  # remove da heap

        if test_imp != prioridade:
            # Define cores dos nós
            cores = [
                "#3F48CC"
                if vert in postos and vert in equipe
                else "blue"
                if vert in postos
                else "orange"
                if vert in equipe
                else "yellow"
                if vert in coleta_agua and m[vert] == "vermelho"
                else "red"
                if atual == "vermelho" or m[vert] == "vermelho"
                else "lightblue"
                if vert in coleta_agua
                else "lightgreen"
                for vert in G.nodes()
            ]

            # Cria a imagem do passo atual
            criar_imagem(
                G, pos, cores, edge_labels, pasta_imgs, passo, atual, alastramento
            )

            passo += 1
            input("Enter...")
            print(atual, alastramento)

            test_imp = prioridade

        for i, v in enumerate(equipe):
            tam = 0
            for u in list(G[atual]) + [atual]:
                if v == u:
                    continue
                path = dijkstra_path(G, v, u)
                # print(f"Menor caminho de {v} até {u}: {path} -> tam: {len(path)}")
                if len(path) < tam and u not in postos:
                    equipe[i] = path[1]
                    tam = len(path)
                else:
                    equipe[i] = path[1]
                    tam = len(path)
            acao = "apagando o fogo" if m[equipe[i]] == "vermelho" else "evitando que o fogo se alastrasse"
            if equipe[i] in list(G[atual]) + [atual]:
                print(f"----> A equipe - {v}, se moveu para {equipe[i]} {acao}")
                m[equipe[i]] = "amarelo"
            else:
                print(f"----> A equipe - {v}, se moveu para {equipe[i]}")

        print(f"equipes: {equipe}")

        bfs_mod(G, m, atual, alastramento, prioridade, postos, equipe)
