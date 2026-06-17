from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit_aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt
import time
# CREATE A TEST SUITE FOR EACH OF THESE TO TEST THEM IN ORDER TO FINISH TASK 2

def evaluate_circuit(circuit_name, qc, shots, optimization_level, noise_rate, correct_answer=None):
    print(f"------Evalutating {circuit_name}------")
    
    # calculate the ideal probabilities
    ideal_probs = Statevector(qc).probabilities_dict()

    # add measurement so the simulator can actually run
    qc.measure_all()

    simulator = AerSimulator()
    
    # adding noise model for noise detection
    noise_model = None
    if noise_rate > 0.0:
        noise_model = NoiseModel()
        error_1q = depolarizing_error(noise_rate, 1)
        error_2q = depolarizing_error(noise_rate * 2, 2)
        noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'rx', 'ry', 'rz'])
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cz'])

    # transpile circuit for the simulator 
    transpiled_qc = transpile(qc, simulator, optimization_level=optimization_level)

    # extract static metrics
    depth = transpiled_qc.depth()
    num_qubits = transpiled_qc.num_qubits
    num_parameters = transpiled_qc.num_parameters

    # sort the gate counts into 1-qubit or 2-qubit groups
    ops = transpiled_qc.count_ops()
    count_1q = 0
    count_2q = 0

    two_qubit_gates = ['cx', 'cz', 'cp', 'swap']
    for gate_name, count in ops.items():
        if gate_name in two_qubit_gates:
            count_2q += count
        elif gate_name not in ['measure', 'barrier']:
            count_1q += count

    # the stopwatch for runtime
    start_time = time.time()
    job_result = simulator.run(transpiled_qc, shots=shots, noise_model=noise_model).result()
    end_time = time.time()

    runtime = end_time - start_time

    # get raw counts and convert them to measured probabilities
    counts = job_result.get_counts()
    measured_probs = {}

    for state, count in counts.items():
        measured_probs[state] = count / shots

    # calculate Total Variation Distance (TVD)
    all_states = set(ideal_probs.keys()).union(set(measured_probs.keys()))
    tvd = 0.0

    for state in all_states:
        ideal_val = ideal_probs.get(state, 0.0)
        measured_val = measured_probs.get(state, 0.0)
        tvd += abs(ideal_val - measured_val)

    tvd = 0.5 * tvd

    # calculating success probability
    success_prob = None
    if correct_answer is not None:
        success_prob = measured_probs.get(correct_answer, 0.0)

    # print the report
    print("\n\n------ EXPERIMENT CONFIGURATION ------")
    print(f"Circuit:            {circuit_name}")
    print(f"Shots:              {shots}")
    print(f"Optimization Level: {optimization_level}")
    print(f"Noise Rate:         {noise_rate} ({'none' if noise_rate == 0.0 else 'low' if noise_rate <= 0.001 else 'medium' if noise_rate <= 0.01 else 'high'})")

    print("\n------ STRUCTURAL METRICS ------")
    print(f"Qubits:             {num_qubits}")
    print(f"Parameters:         {num_parameters}")
    print(f"Circuit Depth:      {depth}")
    print(f"1-Qubit Gates:      {count_1q}")
    print(f"2-Qubit Gates:      {count_2q}")

    print("\n------ PERFORMANCE METRICS ------")
    print(f"Runtime:            {runtime:.4f} seconds")

    print("\n------ QUALITY METRICS ------")
    print(f"TVD from Ideal:     {tvd:.4f} (0.0 is perfect)")

    top_state = max(measured_probs, key=measured_probs.get)
    print(f"Top State:          |{top_state}> with {measured_probs[top_state]*100:.1f}% probability")

    if success_prob is not None:
        print(f"Success Probability: {success_prob * 100:.1f}%")
    else:
        print("Success Probability: Not Applicable")
    
    print("\n")

    return {
        'circuit_name':         circuit_name,
        'shots':                shots,
        'optimization_level':   optimization_level,
        'noise_rate':           noise_rate,
        'num_qubits':           num_qubits,
        'depth':                depth,
        'count_1q':             count_1q,
        'count_2q':             count_2q,
        'runtime':              runtime,
        'tvd':                  tvd,
        'top_state':            top_state,
        'success_probability':  success_prob,
    }

def show_circuit(qc):
    print("Circuit Image:")
    qc.draw('mpl')
    plt.show()