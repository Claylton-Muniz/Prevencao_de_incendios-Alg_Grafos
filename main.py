from ler_arquivo import ler_arquivo
import func_lib as func
from networkx import Graph


if __name__ == "__main__":
    dados = ler_arquivo("entrada.txt")
    postos = [f"V{i}" for i in dados['postos']]
    coleta_agua = [f"V{i}" for i in dados['agua']]
    capacidade = dados['capacidade']
    
    equipes = postos.copy()
    capacidade_equipe = [capacidade for i in equipes]
    requisitos = dados['requisitos']
    
    G = Graph()
    
    func.criar_grafo(G, dados)
    func.mostrar_grafo(G, dados, postos, coleta_agua, equipes, capacidade_equipe, requisitos)
