# Causal Graph Explanation (from "causal_graph.py")

## Causal Variables

### "shots"
- [shots -> tvd]: Increasing shots decreases TVD because more repeated measurements average out sampling noise, pulling the measured probability distribution closer to the ideal - though with diminishing returns past ~2000 shots.

### "noise_rate"
- [noise_rate -> tvd]: Increasing noise_rate increases TVD because higher noise physically perturbs qubit states during execution, pushing the measured distribution further from the ideal.
- [noise_rate -> success_probability]: Increasing noise_rate decreases success_probability because noise degrades the qubit states that Grover's amplitude amplification depends on, making it harder for the marked state to stay boosted above the noise floor.

### "optimization_level"
- [optimization_level -> depth]: Increasing optimization_level tends to decrease depth because Qiskit's transpiler spends more effort compressing and restructuring the circuit - though in this dataset, this effect was only visible for the Grover circuit.
- [optimization_level -> count_2q]: Increasing optimization_level is expected to decrease count_2q through gate cancellation/merging, but no such effect appeared in this dataset, likely because the five simple circuits tested had no redundant two-qubit gates for the transpiler to eliminate.

### "circuit_name"
- [circuit_name -> depth]: Different circuits transpile to fundamentally different depths due to their distinct gate structures - for example, Grover at ~30, Variable Depth at ~22, Parameterized at ~4.5, and Bell/GHZ at ~3.
- [circuit_name -> count_2q]: Different circuits contain different numbers of two-qubit gates by design - for example, Variable Depth at ~15.5, Grover at ~14, Parameterized/GHZ at ~2.5, and Bell at ~1.
- [circuit_name -> success_probability]: circuit_name directly determines success_probability because this metric is defined only for Grover's algorithm, where it measures whether amplitude amplification successfully identifies the marked state - a property tied to the algorithm's specific structure, not just its size.

### "num_qubits"
- [num_qubits -> depth]: Increasing num_qubits increases depth because more qubits require more gate layers to entangle and manipulate them all - for example, Grover's depth grows from ~10 at 2 qubits to ~57 at 4 qubits.
- [num_qubits -> count_2q]: Increasing num_qubits increases count_2q because more qubits means more pairs available to entangle - for example, Grover's count_2q grows from ~3 at 2 qubits to ~28 at 4 qubits.
- [num_qubits -> tvd]: Increasing num_qubits directly increases TVD beyond what depth and count_2q explain, because each additional qubit contributes its own idle and readout error regardless of circuit size - confirmed empirically by holding depth and count_2q constant and still observing TVD increase with qubit count.
- [num_qubits -> runtime]: Increasing num_qubits directly increases runtime because the simulator's state space grows exponentially with qubit count, requiring more memory and computation independent of circuit depth or gate count.

## Mediator Variables

### "depth"
- [depth -> runtime]: Increasing depth increases runtime because each additional gate layer requires more sequential computation steps for the simulator to process.
- [depth -> tvd]: Increasing depth increases TVD because each additional gate layer is another opportunity for noise to accumulate before measurement.
- [depth -> success_probability]: Increasing depth decreases success_probability because more gate layers under noise means more accumulated error by the time Grover's amplitude amplification result is measured - depth growing from 5 to 65 corresponds to success_probability dropping from ~0.9 to ~0.27.

### "count_2q"
- [count_2q -> runtime]: Increasing count_2q increases runtime because two-qubit gates are more computationally expensive for the simulator than single-qubit gates, acting on a larger joint state space.
- [count_2q -> tvd]: Increasing count_2q increases TVD because two-qubit gates are noisier and more error-prone than single-qubit gates, so more of them means more accumulated error before measurement.
- [count_2q -> success_probability]: Increasing count_2q decreases success_probability because Grover's oracle and diffusion operator rely on two-qubit entangling gates, and more error-prone gates mean more noise degrading the amplification result - count_2q growing from 2 to 28 corresponds to success_probability dropping from ~0.89 to ~0.28.

## Outcome Metrics

### "runtime"
Wall-clock simulation time, influenced directly by num_qubits (exponential state space growth) and indirectly through depth and count_2q (more layers and costlier gates). Not affected by noise_rate or shots.

### "tvd"
Total variation distance between the measured and ideal probability distributions - the primary output quality metric, applicable to all five circuits. Influenced directly by noise_rate, shots, num_qubits, depth, and count_2q, with noise_rate being the strongest cause.

### "success_probability"
Grover-specific metric measuring whether amplitude amplification successfully identifies the marked state. Influenced by noise_rate, depth, and count_2q (same accumulated-error reasoning as TVD), plus a direct effect from circuit_name since the metric only exists for Grover's algorithm.