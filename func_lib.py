import heapq
from networkx import draw, draw_networkx_edge_labels, spring_layout, get_edge_attributes
import matplotlib.pyplot as plt
import os
import shutil

import heapq

def dijkstra_caminho(G, origem, destino):
    c = {node: float('inf') for node in G} # c[i] = infinito
    prev = {node: None for node in G} # guarda nó anterior para construir o caminho
    c[origem] = 0
    heap = [(0, origem)]

    while heap:
        current_c, u = heapq.heappop(heap)

        if u == destino:
            break

        for vizinho, attrs in G[u].items():  # attrs contém as propriedades da aresta
            weight = attrs.get('weight', 1)  # Pega o peso da aresta, com valor padrão de 1
            aux = current_c + weight
            if aux < c[vizinho]:
                c[vizinho] = aux
                prev[vizinho] = u
                heapq.heappush(heap, (aux, vizinho))

    # Reconstruir o caminho
    caminho = []
    u = destino
    while u is not None:
        caminho.append(u)
        u = prev[u]
    caminho.reverse()

    if caminho and caminho[0] == origem:
        return caminho
    else:
        return []  # Caminho não encontrado


# modificado para fazer a largura de 1 só vertice
def bfs_mod(G, m, vert, alastramento, prioridade, postos, equipes, fogo):
    # python não tem ponteiros então isso está substituindo o u ← G[w].prox e o u ← u.prox
    for u in G[vert]:
        if m[u] == "verde":
            if m[u] != "azul" and m[u] != "amarelo":
                m[u] = "vermelho"
                fogo.append(u)
                heapq.heappush(alastramento, (prioridade + 1, u))
                
    # Removendo os elementos comuns
    fogo = [x for x in fogo if m[x] not in ('amarelo', 'azul')]
    print(f"eq: {equipes} \nm: {m} \nf: {fogo}")

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
    
    fogo = []
    origem = f"V{dados['fogo']}"
    fogo.append(origem)

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

    alastramento = []
    heapq.heappush(alastramento, (0, origem))
    
    # Criar uma função para diminuir isso aqui ----------------------------------
    
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
        if origem == "vermelho" or m[vert] == "vermelho"
        else "lightblue"
        if vert in coleta_agua
        else "lightgreen"
        for vert in G.nodes()
    ]

    # Cria a imagem do passo atual
    criar_imagem(
        G, pos, cores, edge_labels, pasta_imgs, passo, origem, alastramento
    )
    
    input("Enter...")

    prioridade, atual = heapq.heappop(alastramento)
    print(m[atual])
    input("test...")
    
    while fogo:
        if m[atual] != "vermelho":
            prioridade, atual = heapq.heappop(alastramento)  # remove da heap
        
        for i, v in enumerate(equipe):
            tam = 0
            for u in list(G[atual]) + [atual]:
                if v == u:
                    continue
                caminho = dijkstra_caminho(G, v, u)
                # print(f"Menor caminho de {v} até {u}: {caminho} -> tam: {len(caminho)}")
                if len(caminho) < tam and u not in postos:
                    equipe[i] = caminho[1]
                    tam = len(caminho)
                else:
                    equipe[i] = caminho[1]
                    tam = len(caminho)
            acao = "apagando o fogo" if m[equipe[i]] == "vermelho" else "evitando que o fogo se alastrasse"
            if equipe[i] in list(G[atual]) + [atual]:
                print(f"----> A equipe - {v}, se moveu para {equipe[i]} {acao}")
                m[equipe[i]] = "amarelo"
            else:
                print(f"----> A equipe - {v}, se moveu para {equipe[i]}")
        
        bfs_mod(G, m, atual, alastramento, prioridade, postos, equipe, fogo)

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

        print(f"equipes: {equipe}")
        
        if not alastramento:
            print("O fogo foi completamente controlado.")
            break
