import func_lib as func
import networkx as nx

def gerar_relatorio(dados):
    postos = [f"V{i}" for i in dados['postos']]
    coleta_agua = [f"V{i}" for i in dados['agua']]
    requisitos = {f"V{k}": v["agua"] for k, v in dados["requisitos"].items()}
    capacidade = dados["capacidade"]

    equipes = postos.copy()
    caminhos_equipes = {e: [e] for e in equipes}
    agua_usada = 0
    vertices_salvos = set()
    tempo_passos = 0

    G = nx.Graph()
    func.criar_grafo(G, dados)

    for passo, estado in enumerate(func.simular_fogo(G, dados, postos, coleta_agua, equipes)):
        tempo_passos = passo
        agua_usada += estado["agua_usada"]
        vertices_salvos.update(estado["vertices_salvos"])
        for equipe, pos in estado["caminhos"].items():
            caminhos_equipes[equipe].append(pos)

    with open("relatorio.txt", "w") as f:
        f.write("Relatório da Simulação\n")
        f.write("=======================\n")
        f.write(f"Vértices salvos: {len(vertices_salvos)}\n")
        f.write(f"Tempo para conter o fogo: {tempo_passos} passos\n")
        f.write(f"Água total utilizada: {agua_usada} unidades\n\n")
        f.write("Caminhos percorridos pelas equipes:\n")
        for equipe, caminho in caminhos_equipes.items():
            f.write(f" - {equipe}: {' -> '.join(caminho)}\n")

    print("Relatório gerado em relatorio.txt.")

