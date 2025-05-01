from ler_arquivo import ler_arquivo
import func_lib as func
import networkx as nx


if __name__ == "__main__":
    dados = ler_arquivo("entrada.txt")
    
    G = nx.Graph()
    func.criar_grafo(G, dados)
    func.mostrar_grafo(G, dados)


