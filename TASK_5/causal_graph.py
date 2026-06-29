import networkx as nx
import matplotlib.pyplot as plt

dg = nx.DiGraph()

# SHOTS
dg.add_edges_from([("shots", "TVD")])

# OPTIMIZATION LEVEL
dg.add_edges_from([("optimization_level", "depth")])
dg.add_edges_from([("optimization_level", "count_2q")])

# NOISE RATE
dg.add_edges_from([("noise_rate", "TVD")])
dg.add_edges_from([("noise_rate", "success_probability")])

# NUM_QUBITS
dg.add_edges_from([("num_qubits", "depth")])
dg.add_edges_from([("num_qubits", "count_2q")])
dg.add_edges_from([("num_qubits", "TVD")])
dg.add_edges_from([("num_qubits", "runtime")])

# CIRCUIT_NAME
dg.add_edges_from([("circuit_name", "depth")])
dg.add_edges_from([("circuit_name", "count_2q")])
dg.add_edges_from([("circuit_name", "success_probability")])

# MEDIATOR: DEPTH
dg.add_edges_from([("depth", "TVD")])
dg.add_edges_from([("depth", "runtime")])
dg.add_edges_from([("depth", "success_probability")])

# MEDIATOR: COUNT_2Q
dg.add_edges_from([("count_2q", "TVD")])
dg.add_edges_from([("count_2q", "runtime")])
dg.add_edges_from([("count_2q", "success_probability")])

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
    "TVD": (2, 1),
    "success_probability": (2, 0)
}

nx.draw(
    dg,
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