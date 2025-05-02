import networkx as nx
import matplotlib.pyplot as plt
import heapq
import os
import shutil

def criar_grafo(G, dados):

    for i in range(dados['num_vertices']):
        G.add_node(f"V{i}")

    for aresta in dados['arestas']:
        G.add_edge(f"V{aresta[0]}", f"V{aresta[2]}", weight=aresta[1])
    
    postos = []
    for i in dados['postos']:
        postos.append(f"V{i}")
        
    return postos
        
        
def mostrar_grafo(G, dados, postos):
    pasta_imgs = "imgs"
    
    # Cria a pasta se não existir, ou limpa se já existir
    if os.path.exists(pasta_imgs):
        shutil.rmtree(pasta_imgs)
    os.makedirs(pasta_imgs)

    origem = f"V{dados['fogo']}"
    visitados = set()
    
    # inicia a distancia de todos os vert como infinito
    distancias = {vert: float('inf') for vert in G.nodes()}
    distancias[origem] = 0

    fila = [(0, origem)]
    passo = 0

    # Layout e pesos das arestas
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    while fila:
        custo_atual, atual = heapq.heappop(fila) # remove da heap

        if atual in visitados: # Se já foi visitado ignora
            continue
        visitados.add(atual) # se não adiciona em visitados

        # Define cores dos nós
        cores = [
            "blue" if vert in postos else
            "red" if vert in visitados else
            "lightgreen"
            for vert in G.nodes()
        ]

        # Cria a imagem do passo atual
        plt.figure(figsize=(8, 6))
        if passo == 0:
            plt.title(f"Passo {passo}: Fogo iniciou em {atual} (custo acumulado: {custo_atual})")
        else:
            plt.title(f"Passo {passo}: Fogo chegou em {atual} (custo acumulado: {custo_atual})")
        nx.draw(G, pos, with_labels=True, node_color=cores)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        caminho_imagem = os.path.join(pasta_imgs, f"passo_{passo:03}.png")
        plt.savefig(caminho_imagem)
        plt.close()

        passo += 1

        for vizinho in G.neighbors(atual): # verifica vizinhos do meu vertice atual
            peso = G[atual][vizinho]['weight'] # w(u, i)
            nova_dist = custo_atual + peso # c(i, u) + w(u, i)
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                heapq.heappush(fila, (nova_dist, vizinho)) # atualiza heap