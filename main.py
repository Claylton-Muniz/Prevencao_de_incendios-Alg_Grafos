from ler_arquivo import ler_arquivo
import func_lib as func
import networkx as nx


if __name__ == "__main__":
    dados = ler_arquivo("entrada.txt")
    postos = [f"V{i}" for i in dados['postos']]
    coleta_agua = [f"V{i}" for i in dados['agua']]
    
    equipes = postos.copy()
    
    G = nx.Graph()
    
    func.criar_grafo(G, dados)
    func.mostrar_grafo(G, dados, postos, coleta_agua, equipes)
