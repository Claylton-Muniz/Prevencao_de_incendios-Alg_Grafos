from itertools import chain
import os
import heapq
import shutil
import matplotlib.pyplot as plt

from func_graf import alastrar, dijkstra_caminho, peso_total_caminho
from networkx import draw, draw_networkx_edge_labels, spring_layout, get_edge_attributes


def criar_grafo(G, dados):
    G.add_nodes_from(f"V{i}" for i in range(dados["num_vertices"]))
    for v1, peso, v2 in dados["arestas"]:
        G.add_edge(f"V{v1}", f"V{v2}", weight=peso)


def criar_imagem(G, pos, cores, edge_labels, pasta_imgs, passo, atual, alastramento):
    plt.figure(figsize=(8, 6))

    titulo = (
        f"Passo {passo}: Fogo iniciou em {atual}"
        if passo == 0 
        else f"Passo {passo}: Fogo se alastrou por {atual}"
        + "".join(f", {v[1]}" for v in alastramento)
        if passo != -1 else "O fogo foi completamente controlado."
    )

    plt.title(titulo)

    draw(G, pos, with_labels=True, node_color=cores)
    draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    plt.savefig(os.path.join(pasta_imgs, "slide.png"))
    plt.close()


def rederinzar_imagem(
    G,
    m,
    pos,
    edge_labels,
    pasta_imgs,
    postos,
    equipe,
    coleta_agua,
    atual,
    passo,
    alastramento,
):
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
    
    print(f"Passo: {passo}")

    # Cria a imagem do passo atual
    criar_imagem(G, pos, cores, edge_labels, pasta_imgs, passo, atual, alastramento)

    input("Enter...")


def movimento_equipes(G, m, equipe, postos, fogo, capacidade_equipe, requisitos):
    for i, v in enumerate(equipe):
        menor_peso = float("inf")
        capaz = True

        vizinhos = [list(G.neighbors(vert)) + [vert] for vert in fogo]
        vizinhos = set(chain.from_iterable(vizinhos))
        vizinhos = [vert for vert in vizinhos if m[vert] != "amarelo"]

        # print(f"\nvizinhos {vizinhos}")

        for u in vizinhos:
            if v == u:
                continue

            if requisitos[u] > capacidade_equipe[i]:
                capaz = False
                continue

            capaz = True
            caminho = dijkstra_caminho(G, v, u)

            if caminho[-1] in postos:
                continue

            peso_caminho = peso_total_caminho(G, caminho)
            if peso_caminho < menor_peso and u not in postos and caminho[1] not in equipe:
                equipe[i] = caminho[1]
                menor_peso = peso_caminho

        if equipe[i] == v and capaz:
            equipe[i] = caminho[1]
        elif not capaz:
            for u in postos:
                if v == u:
                    print(f"Equipe {i} reabasteceu completamente!!")
                    capacidade_equipe[i] = 100
                    break

                caminho = dijkstra_caminho(G, v, u)
                peso_caminho = peso_total_caminho(G, caminho)
                print(caminho)
                if peso_caminho < menor_peso:
                    print(f"es: {caminho}")
                    equipe[i] = caminho[1]
                    menor_peso = peso_caminho

        # Texto bonito...
        acao = (
            "apagando o fogo"
            if m[equipe[i]] == "vermelho"
            else "evitando que o fogo se alastrasse"
        )
        if equipe[i] in vizinhos:
            print(f"----> A equipe - {i} que estava em {v}, se moveu para {equipe[i]} {acao}")
            capacidade_equipe[i] -= requisitos[equipe[i]]
            print(f"\tAgora a equipe tem {capacidade_equipe[i]} de capacidade para apagar o resto do fogo")
            requisitos[equipe[i]] = 0
            m[equipe[i]] = "amarelo"
        elif equipe[i] in postos:
            print(f"----> A equipe - {i}, se moveu para {equipe[i]} e reabateceu completamente!")
        else:
            print(f"----> A equipe - {i}, se moveu para {equipe[i]}")
    # print(f"requisitos {requisitos}\n capacidade {capacidade_equipe}")


def mostrar_grafo(G, dados, postos, coleta_agua, equipe, capacidade_equipe, requisitos):
    # Cria a pasta se não existir, ou limpa se já existir
    pasta_imgs = "imgs"
    if os.path.exists(pasta_imgs):
        shutil.rmtree(pasta_imgs)
    os.makedirs(pasta_imgs)

    # Define a origem do fogo
    origem = f"V{dados['fogo']}"
    fogo = [origem]

    # Declaração inicial das marcas na BFS.
    # Alterei para verde e vermelho para fazer sentido com o fogo
    m = {v: ("azul" if v in postos else "verde") for v in G.nodes()}
    m[origem] = "vermelho"
    """
    Foi necessário fazer ela aqui para 
    diminuir a complexidade e não perder 
    as marcas nas iterações
    """

    # Layout e pesos das arestas
    pos = spring_layout(G, seed=42)
    edge_labels = get_edge_attributes(G, "weight")

    alastramento = []
    heapq.heappush(alastramento, (0, origem))

    passo = 0
    rederinzar_imagem(
        G,
        m,
        pos,
        edge_labels,
        pasta_imgs,
        postos,
        equipe,
        coleta_agua,
        origem,
        passo,
        alastramento,
    )

    prioridade, atual = heapq.heappop(alastramento)

    while fogo:
        while prioridade == passo:    
            alastrar(G, m, atual, alastramento, prioridade, postos, equipe, fogo)
            if alastramento:
                prioridade, atual = heapq.heappop(alastramento) # remove da heap
            else:
                break
            
        # renderiza alastramento - antes do movimento para ver oq aconteceu
        # rederinzar_imagem(
        #     G,
        #     m,
        #     pos,
        #     edge_labels,
        #     pasta_imgs,
        #     postos,
        #     equipe,
        #     coleta_agua,
        #     atual,
        #     passo,
        #     alastramento,
        # )
            
        movimento_equipes(G, m, equipe, postos, fogo, capacidade_equipe, requisitos)

        # Removendo os elementos comuns
        fogo = [x for x in fogo if m[x] not in ("amarelo", "azul")]

        passo += 1
        rederinzar_imagem(
            G,
            m,
            pos,
            edge_labels,
            pasta_imgs,
            postos,
            equipe,
            coleta_agua,
            atual,
            passo,
            alastramento,
        )

        # print(f"fogo: {fogo}")

        if not fogo:
            print("O fogo foi completamente controlado.")
            rederinzar_imagem(
                G,
                m,
                pos,
                edge_labels,
                pasta_imgs,
                postos,
                equipe,
                coleta_agua,
                atual,
                -1,
                alastramento,
            )
            break

        # print(f"equipes: {equipe}")
