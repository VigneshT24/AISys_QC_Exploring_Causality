# Causal Explanation

## Causal Variables

### "shots"

- [shots -> TVD]: This edge establishes a causal relationship between "shots" and "TVD," where "shots" is a variable that affects the outcome metric "TVD." This direct edge exists because "shots" is defined as the number of times you run a quantum circuit with the same configuration. Since quantum circuits are probabilistic, as you increase the number of "shots", the total variation distance (or "TVD") becomes lower (which means an improvement in output quality), since "TVD" measures the absolute value distance between an ideal probability and the measured probability, and increasing the number of shots means the measured probability gets closer to the ideal probability. However, there is a diminishing returns curve, because, based on the "TVD Stability by Shot Count" graph, past ~2000 shots, increasing shots doesn't decrease the TVD as much. The direction only points from "shots" to "TVD," and not the other way, because "shots" is a configuration value chosen before the circuit is even run, while "TVD" is only computed afterward, from the measurement results. Since "TVD" doesn't exist yet at the moment "shots" is set, it cannot be the one influencing "shots."

### "noise_rate"

- [noise_rate -> TVD]: This edge establishes a causal relationship between "noise_rate" and "TVD," where "noise_rate" is a variable that affects the outcome metric "TVD." This direct edge exists because "noise_rate" is defined as the frequency at which quantum gates and qubits lose their information due to environmental interference or hardware flaws. Since quantum circuits and qubits are sensitive and prone to disruptions, based on the "TVD by Noise Rate" graph, as you increase the "noise_rate", the total variation distance (or "TVD") becomes higher (which means a worsening output quality), since "TVD" measures the absolute value distance between an ideal probability and the measured probability, and increasing the "noise_rate" means the measured probability gets farther away from the ideal probability. The direction only points from "noise_rate" to "TVD," and not the other way, because "noise_rate" is a configuration value chosen before the circuit is even run, while "TVD" is only computed afterward, from the measurement results. Since "TVD" doesn't exist yet at the moment "noise_rate" is set, it cannot be the one influencing "noise_rate."

- [noise_rate -> success_probability]: This edge establishes a causal relationship between "noise_rate" and "success_probability," where "noise_rate" is a variable that affects the outcome metric "success_probability." This direct edge exists because "noise_rate" is defined as the frequency at which quantum gates and qubits lose their information due to environmental interference or hardware flaws. Since quantum circuits and qubits are sensitive and prone to disruptions, based on the "Grover: Success Probability by Noise Rate" graph, as you increase the "noise_rate", "success_probability" (which measures the probability that a circuit will output an expected output, and is only applicable to the Grover circuit) lowers, since the noise impacts the performance and the reliability of the qubits in the circuit. The direction only points from "noise_rate" to "success_probability," and not the other way, because "noise_rate" is a configuration value chosen before the circuit is even run, while "success_probability" is only computed afterward, from the measurement results. Since "success_probability" doesn't exist yet at the moment "noise_rate" is set, it cannot be the one influencing "noise_rate."

### "optimization_level"

- [optimization_level -> depth]: This edge establishes a causal relationship between "optimization_level" and "depth," where "optimization_level" is a variable that affects the mediator metric "depth." This direct edge exists because "optimization_level" is a parameter (from 0 to 3) controlling how much computational effort the transpiler spends compressing and restructuring a quantum circuit to minimize gate count and circuit depth before running it on a quantum device. Based on the "Transpiled Depth by Optimization Level" graph, as you increase the "optimization_level," the "transpiled_depth" (which is the resulting horizontal length of the quantum circuit) lowers noticeably for the Grover circuit, while staying essentially flat for the other four circuit types, meaning the strength of this effect depends heavily on which circuit is being run. This makes sense, since increasing "optimization_level" only helps when there is actually room for the transpiler to compress the circuit further; some circuits may already be at or near their minimal depth. The direction only points from "optimization_level" to "depth," and not the other way, because "optimization_level" is a configuration value preemptively chosen before the circuit is even run, while "depth" is only known afterward, once the transpiler has processed the circuit. Since the final "depth" doesn't exist yet at the moment "optimization_level" is set, it cannot be the one influencing "optimization_level."

- [optimization_level -> count_2q]: This edge establishes a causal relationship between "optimization_level" and "count_2q," where "optimization_level" is a variable that affects the mediator metric "count_2q." This direct edge exists because, by definition, "optimization_level" is a parameter (from 0 to 3) controlling how much computational effort the transpiler spends compressing and restructuring a quantum circuit to minimize gate count and circuit depth, including the count of two-qubit gates, before running it on a quantum device. However, based on the "Two-Qubit Gate Count by Optimization Level" graph, this effect did not appear in this dataset, every circuit type shows a perfectly flat "count_2q" across all optimization levels, including Grover, which did show a depth reduction in the earlier graph. This is likely because the five circuits tested (2-5 qubits, relatively simple structures) did not contain redundant or cancellable two-qubit gates for the transpiler to act on; the mechanism for this edge is real in principle, since Qiskit's transpiler is documented to perform two-qubit gate cancellation/merging at higher optimization levels, but it may only activate for larger or more complex circuits than the ones tested here. The direction only points from "optimization_level" to "count_2q," and not the other way, because "optimization_level" is a configuration value preemptively chosen before the circuit is even run, while "count_2q" is only known afterward, once the transpiler has processed the circuit.

### "circuit_name"

- [circuit_name -> depth]: This edge establishes a causal relationship between "circuit_name" and "depth," where "circuit_name" is a variable that affects the mediator metric "depth." This direct edge exists because "circuit_name" is an indicator of which one of the five basic quantum circuits is being tested. Based on the "Transpiled Depth by Optimization Level, All Circuits" graph, all five circuit types sit at clearly different, largely flat depth levels regardless of optimization_level. For example, Grover transpiles to a depth around 30, Variable Depth around 22, Parameterized around 4.5, and Bell/GHZ around 3, indicating that the choice of circuit itself, independent of any other configuration, determines a large part of the resulting depth. The direction only points from "circuit_name" to "depth," and not the other way, because "circuit_name" identifies which circuit was selected to run, decided before execution, while "depth" is only known afterward, once the transpiler has processed that specific circuit. Since the final "depth" doesn't exist yet at the moment "circuit_name" is set, it cannot be the one influencing "circuit_name."

- [circuit_name -> count_2q]: This edge establishes a causal relationship between "circuit_name" and "count_2q," where "circuit_name" is a variable that affects the mediator metric "count_2q." This direct edge exists because "circuit_name" is an indicator of which one of the five basic quantum circuits is being tested. Based on the "Two-Qubit Gate Count by Optimization Level, All Circuits" graph, most of the five circuit types sit at different, largely flat "count_2q" levels regardless of optimization_level. For example, Grover's count_2q is around 14, Variable count_2q around 15.5, Parameterized/GHZ count_2q around 2.5, and Bell count_2q around 1, indicating that the choice of circuit itself, independent of any other configuration, determines a large part of the resulting "count_2q". The direction only points from "circuit_name" to "count_2q," and not the other way, because "circuit_name" identifies which circuit was selected to run, decided before execution, while "count_2q" is only calculated afterward, once that specific circuit is processed. Since the final "count_2q" doesn't exist yet at the moment "circuit_name" is set, it cannot be the one influencing "circuit_name."

- [circuit_name -> success_probability]: This edge establishes a causal relationship between "circuit_name" and "success_probability," where "circuit_name" is a variable that affects the outcome metric "success_probability" directly, not only through the mediators "depth" and "count_2q." This direct edge exists because "success_probability" is defined specifically for the Grover circuit as the probability that the algorithm's amplitude amplification process successfully boosts the marked state's probability above the noise floor, rather than a generic measure of output quality like "TVD." This is tied to the specific algorithmic structure of Grover's search (its oracle design and number of amplification iterations), not just to how large or gate-heavy the resulting circuit is. Even if two different circuits happened to transpile to the same "depth" and "count_2q," they would not necessarily have the same "success_probability," since that metric depends on whether the specific algorithm being run is one that is even trying to amplify a marked state at all. This is also why "success_probability" is undefined for the other four circuit types (Bell, GHZ, Parameterized, Variable Depth); they are not search algorithms with a "correct answer" to amplify toward, so the metric does not apply to them regardless of their depth or gate count. The direction only points from "circuit_name" to "success_probability," and not the other way, because "circuit_name" identifies which circuit was selected to run, decided before execution, while "success_probability" is only computed afterward, from the measurement results.

### "num_qubits"

- [num_qubits -> depth]:

- [num_qubits -> count_2q]:

- [num_qubits -> TVD]:

- [num_qubits -> runtime]: 

## Mediator Variables

### "depth"

- [depth -> runtime]:

- [depth -> TVD]:

- [depth -> success_probability]:

### "count_2q"

- [count_2q -> runtime]:

- [count_2q -> TVD]:

- [count_2q -> success_probability]:

## Outcome Metrics

### "runtime"

### "TVD"

### "success_probability"