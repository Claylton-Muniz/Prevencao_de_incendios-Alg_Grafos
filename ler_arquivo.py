def ler_arquivo(arquivo):
    # Cria uma lista chamada linhas, contendo apenas as linhas não vazias e sem #
    with open(arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip() and not linha.startswith('#')]

    idx = 0 # rastreia linha atual
    num_vertices = list(map(int, linhas[idx].split()))[0]
    idx += 1 # atualiza linha

