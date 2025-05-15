import os
import heapq
import shutil
import matplotlib.pyplot as plt

from func_graf import bfs_mod, dijkstra_caminho
from networkx import draw, draw_networkx_edge_labels, spring_layout, get_edge_attributes


def criar_grafo(G, dados):
    G.add_nodes_from(f"V{i}" for i in range(dados["num_vertices"]))
    for v1, peso, v2 in dados["arestas"]:
        G.add_edge(f"V{v1}", f"V{v2}", weight=peso)


def criar_imagem(G, pos, cores, edge_labels, pasta_imgs, passo, atual, alastramento):
    plt.figure(figsize=(8, 6))

    titulo = (
        f"Passo {passo}: Fogo iniciou em {atual}"
        if passo == 0 else
        f"Passo {passo}: Fogo se alastrou por {atual}" +
        "".join(f", {v[1]}" for v in alastramento)
    )
    
    plt.title(titulo)

    draw(G, pos, with_labels=True, node_color=cores)
    draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    plt.savefig(os.path.join(pasta_imgs, "slide.png"))
    plt.savefig(os.path.join(pasta_imgs, "slide-{}.png".format(passo)))
    plt.close()


def rederinzar_imagem(
    G, m, pos, edge_labels, pasta_imgs, postos, equipe, coleta_agua, atual, passo, alastramento
    ):
    # Define cores dos nós
    cores = [
        "#3F48CC" if vert in postos and vert in equipe else 
        "blue" if vert in postos else 
        "orange" if vert in equipe else 
        "yellow" if vert in coleta_agua and m[vert] == "vermelho" else 
        "red" if atual == "vermelho" or m[vert] == "vermelho" else 
        "lightblue" if vert in coleta_agua else 
        "lightgreen"
        for vert in G.nodes()
    ]
    
    # Cria a imagem do passo atual
    criar_imagem(
        G, pos, cores, edge_labels, pasta_imgs, passo, atual, alastramento
    )
    
    input("Enter...")
    

def mostrar_grafo(G, dados, postos, coleta_agua, equipe):
    
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
        G, m, pos, edge_labels, pasta_imgs, postos, equipe, coleta_agua, origem, passo, alastramento
    )

    prioridade, atual = heapq.heappop(alastramento)
    
    while fogo:
        if m[atual] != "vermelho":
            prioridade, atual = heapq.heappop(alastramento)  # remove da heap
        
        for i, v in enumerate(equipe):
            tam = float("inf")
            
            # u anda nos vizinhos do fogo ou no fogo
            for u in list(G[atual]) + [atual]:
                if v == u:
                    continue
                caminho = dijkstra_caminho(G, v, u)
                print(f"{atual} - Menor caminho de {v} até {u}: {caminho} -> tam: {len(caminho)}")
                if (len(caminho) < tam and 
                    u not in postos and
                    caminho[1] not in equipe):
                    equipe[i] = caminho[1]
                    tam = len(caminho)
                
            # texto para diexar bonito, não afeta a lógica    
            acao = "apagando o fogo" if m[equipe[i]] == "vermelho" else "evitando que o fogo se alastrasse"
            if equipe[i] in list(G[atual]) + [atual]:
                print(f"----> A equipe que estava em {v}, se moveu para {equipe[i]} {acao}")
                m[equipe[i]] = "amarelo"
            else:
                print(f"----> A equipe - {v}, se moveu para {equipe[i]}")
        
        bfs_mod(G, m, atual, alastramento, prioridade, postos, equipe, fogo)
        
        # Removendo os elementos comuns
        fogo = [x for x in fogo if m[x] not in ('amarelo', 'azul')]

        passo += 1
        
        rederinzar_imagem(
            G, m, pos, edge_labels, pasta_imgs, postos, equipe, coleta_agua, atual, passo, alastramento
        )
        
        print(f"fogo: {fogo}")
        if not fogo:
            break

        print(f"equipes: {equipe}")
        
        if not alastramento:
            # Define cores dos nós
            rederinzar_imagem(
                G, m, pos, edge_labels, pasta_imgs, postos, equipe, coleta_agua, atual, passo, alastramento
            )
            
            print("O fogo foi completamente controlado.")
