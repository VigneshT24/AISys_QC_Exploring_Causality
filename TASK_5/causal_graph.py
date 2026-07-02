import networkx as nx
import matplotlib.pyplot as plt


def get_nx(only_sp=False):
    """Generate the causal graph using NetworkX, to be fed into DoWhy for Analysis"""
    dg = nx.DiGraph()

    ## W/O SUCCESS_PROBABILITY ##
    if not only_sp:
        # SHOTS
        dg.add_edges_from([("shots", "tvd")])

        # OPTIMIZATION LEVEL
        dg.add_edges_from([("optimization_level", "depth")])
        dg.add_edges_from([("optimization_level", "count_2q")])

        # NOISE RATE
        dg.add_edges_from([("noise_rate", "tvd")])

        # NUM_QUBITS
        dg.add_edges_from([("num_qubits", "depth")])
        dg.add_edges_from([("num_qubits", "count_2q")])
        dg.add_edges_from([("num_qubits", "tvd")])
        dg.add_edges_from([("num_qubits", "runtime")])

        # CIRCUIT_NAME
        dg.add_edges_from([("circuit_name", "depth")])
        dg.add_edges_from([("circuit_name", "count_2q")])

        # MEDIATOR: DEPTH
        dg.add_edges_from([("depth", "tvd")])
        dg.add_edges_from([("depth", "runtime")])

        # MEDIATOR: COUNT_2Q
        dg.add_edges_from([("count_2q", "tvd")])
        dg.add_edges_from([("count_2q", "runtime")])

    ## W/ SUCCESS_PROBABILITY ONLY ##
    else:
        dg.add_edges_from([("noise_rate", "success_probability")])
        
        # REMOVED THIS EDGE, SINCE CIRCUIT_NAME WILL ALWAYS BE "grover" IN THIS CASE
        # dg.add_edges_from([("circuit_name", "success_probability")])


        dg.add_edges_from([("depth", "success_probability")])
        dg.add_edges_from([("count_2q", "success_probability")])

    return dg

def draw_nx(only_sp=False):
    graph = get_nx(only_sp=only_sp)
    
    if not only_sp:
        pos = {
            "shots": (0, 4),
            "num_qubits": (0, 3),
            "optimization_level": (0, 2),
            "noise_rate": (0, 1),
            "circuit_name": (0, 0),
            "depth": (1, 1),
            "count_2q": (1, 0),
            "runtime": (2, 2),
            "tvd": (2, 1),
            "success_probability": (2, 0)
        }
    else:
        pos = {
            "noise_rate": (0, 2),
            "depth": (0, 1),
            "count_2q": (0, 0),
            "success_probability": (1, 1)
        }
    
    plt.figure(figsize=(10, 5))
    nx.draw(graph, pos=pos, with_labels=True, node_color="red",
            node_size=2000, font_size=10, font_weight="bold",
            arrowsize=20, edge_color="blue")
    plt.margins(x=0.2, y=0.1)
    plt.show()


if __name__ == "__main__":

    # generate two different graphs, one with and the other without success_probability
    graph_1 = get_nx(only_sp=False)
    graph_2 = get_nx(only_sp=True)

    plt.figure(figsize=(10, 5))

    pos = {
        # causal variables
        "shots": (0, 4),
        "num_qubits": (0, 3),
        "optimization_level": (0, 2),
        "noise_rate": (0, 1),
        "circuit_name": (0, 0),

        # mediators
        "depth": (1, 1),
        "count_2q": (1, 0),

        # output metrics
        "runtime": (2, 2),
        "tvd": (2, 1),
        "success_probability": (2, 0)
    }

    nx.draw(
        graph_1,
        pos=pos,
        with_labels=True,
        node_color="red",
        node_size=2000,
        font_size=10,
        font_weight="bold",
        arrowsize=20,
        edge_color="blue"
    )

    nx.draw(
        graph_2,
        pos=pos,
        with_labels=True,
        node_color="red",
        node_size=2000,
        font_size=10,
        font_weight="bold",
        arrowsize=20,
        edge_color="blue"
    )

    plt.show()