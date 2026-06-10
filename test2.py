from qiskit import QuantumCircuit as QC
from qiskit.circuit import QuantumRegister as QR
from qiskit.circuit import ClassicalRegister as CR
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendSamplerV2
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import math

q = QR(2)
circ = QC(q)

circ.h(q[0])
circ.cx(q[0], q[1])

print(circ)

circ.measure_all()

print(circ)

def bell(a, b, circ):
    circ.h(a)
    circ.cx(a, b)
    return circ

def bell_inverse(a, b, circ):
    circ.cx(a, b)
    circ.h(a)
    return circ

def tele():
    q = QR(3)
    b = CR(3)
    circ = QC(q, b)
    circ = bell(q[1], q[2], circ)
    circ.h(q[0])
    circ = bell_inverse(q[0], q[1], circ)
    circ.measure(q[0], b[0])
    circ.measure(q[1], b[1])

    with circ.if_test ((b[1], 1)):
        circ.x(q[2])
    if circ.if_test ((b[0], 1)):
        circ.z(q[2])
    
    circ.measure(q[2], b[2])
    return circ


circ1 = tele()

print(circ1)


# aer = AerSimulator()
# sampler = BackendSamplerV2(backend=aer)

# result = sampler.run([circ], shots=1024).result()

# counts = result[0].data.meas.get_counts()

# plot_histogram(counts)

# plt.show()