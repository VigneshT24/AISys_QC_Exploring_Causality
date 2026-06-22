import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from basic_quantum_circuits import BasicQuantumCircuits
import numpy as np

def show_circuit(circuit_name, qc):
    print(f"{circuit_name}: ")
    qc.draw('mpl')
    plt.show()

circuit = BasicQuantumCircuits()

show_circuit("Bell State Circuit", circuit.bell_state_circuit())
show_circuit("GHZ State Circuit", circuit.ghz_state_circuit(4))
show_circuit("Grover Circuit", circuit.grover_circuit(2, '11'))
show_circuit("Parameterized Circuit", circuit.parameterized_circuit(1, [('rx', np.pi/2)]))
show_circuit("Variable Depth Circuit", circuit.variable_depth_circuit(3, 4))