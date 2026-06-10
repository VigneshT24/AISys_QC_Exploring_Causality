from qiskit import QuantumCircuit as QC
from qiskit.primitives import StatevectorSampler as SvS
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qc = QC(3)
qc.h(0)
qc.h(1)
qc.cx(0, 1)
qc.cx(1, 2)
qc.x(1)
qc.measure_all()

sampler = SvS()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
plot_histogram(counts)

plt.show()
