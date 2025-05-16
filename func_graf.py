import heapq


def peso_total_caminho(G, caminho):
    return sum(G[caminho[i]][caminho[i + 1]]['weight'] for i in range(len(caminho) - 1))


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
def alastrar(G, m, vert, alastramento, prioridade, postos, equipes, fogo):
    # python não tem ponteiros então isso está substituindo o u ← G[w].prox e o u ← u.prox
    for u in G.neighbors(vert):
        if m[u] == "verde":
            if m[u] != "azul" and m[u] != "amarelo":
                m[u] = "vermelho"
                fogo.append(u)
                heapq.heappush(alastramento, (prioridade + 1, u))
                
    # print(f"eq: {equipes} \nm: {m}\nal: {alastramento}")

    return m
