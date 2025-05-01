import networkx as nx
import matplotlib.pyplot as plt

def criar_grafo(G, dados):

    for i in range(dados['num_vertices']):
        G.add_node(f"Area{i}")

    for aresta in dados['arestas']:
        G.add_edge(f"Area{aresta[0]}", f"Area{aresta[2]}", weight=aresta[1])
        
def mostrar_grafo(G, dados):
    
    vizinho = []
    vizinhosLista = []
    visitados = []
    vert = f"Area{dados['fogo']}"
    
    iterator = 0
    
    while True:
    
        for viz in nx.bfs_edges(G, vert):
            
            cores = []
            
            if viz[0] == vert and iterator != 0:
                vizinhosLista.append(viz[1])
                visitados.append(viz[1])
                
            else:

                for node in G.nodes():
                    if node == f"Area{dados['fogo']}" or node in visitados:
                        cores.append("red")
                    else:
                        cores.append("lightgreen")
                        
                # Layout
                pos = nx.spring_layout(G)

                # Extrair pesos
                edge_labels = nx.get_edge_attributes(G, 'weight')

                # Mostrar pesos das arestas
                nx.draw(G, pos, with_labels=True, node_color=cores)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
                
                plt.show()
                input("Pressione Enter para continuar...")
                
                if iterator == 1: vert = viz[0]
                iterator = 1
                break
            