def ler_arquivo(arquivo):
    # Cria uma lista chamada linhas, contendo apenas as linhas não vazias e sem #
    with open(arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.startswith('#')]

    idx = 0  # rastreia linha atual
    num_vertices = int(linhas[idx])
    idx += 1

    num_arestas = int(linhas[idx])
    idx += 1

    # Lê as arestas
    arestas = []
    for _ in range(num_arestas):
        u, custo, v = map(int, linhas[idx].split())
        arestas.append((u, custo, v))
        idx += 1

    # Postos de brigadistas
    postos = list(map(int, linhas[idx].split()[1:]))  # Remove "Postos:"
    idx += 1

    # Pontos de coleta de água
    agua = list(map(int, linhas[idx].split()[1:]))  # Remove "Agua:"
    idx += 1

    # Capacidade de água dos caminhões
    capacidade = int(linhas[idx].split()[1])  # Remove "Capacidade:"
    idx += 1

    # Requisitos por vértice
    requisitos = {}
    idx += 1  # Pula a linha "Requisitos:"
    for _ in range(num_vertices):
        v_id, agua_necessaria = map(int, linhas[idx].split())
        requisitos[f'V{v_id}'] = agua_necessaria
        idx += 1

    # Ponto inicial do incêndio
    fogo = int(linhas[idx].split()[1])  # Remove "Fogo:"

    # Retorna um dicionário com todas as informações
    return {
        'num_vertices': num_vertices,
        'num_arestas': num_arestas,
        'arestas': arestas,
        'postos': postos,
        'agua': agua,
        'capacidade': capacidade,
        'requisitos': requisitos,
        'fogo': fogo
    }
