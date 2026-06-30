from qiskit import transpile
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit_aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt
import time

def evaluate_circuit(circuit_name, qc, shots, optimization_level, noise_rate, correct_answer=None, seed=42) -> dict:
    """
    Takes a circuit and evaluates it based on runtime, TVD, and Noise Rate, in addition to other metrics

    Args:
        'circuit_name': name of the circuit that will be evaluated
        'qc': the quantum circuit that will be evaluated
        'shots': the number of shots to evaluate the quantum circuit (128, 512, 1024, 4096)
        'optimization_level': the level of optimization (0-3) to apply to the quantum circuit
        'noise_rate': the level of noise (0-1) to apply to the quantum circuit
        'correct_answer': only applicable if the quantum circuit needs to return a specific answer
    
    Returns:
        'output_metrics': a dictionary full of all the output metrics of the quantum circuit evaluation
    
    Raises:
        ValueError: if any of the entered parameter is not valid
    """

    # parameter validity check
    if not isinstance(circuit_name, str) or circuit_name.strip() == '':
        raise ValueError(f"The value entered for 'circuit_name' parameter must be a string and not be empty. Got '{circuit_name}.'")
    if not isinstance(qc, QuantumCircuit):
        raise ValueError("The value entered for 'qc' parameter must be a Qiskit QuantumCircuit instance.")
    if not isinstance(shots, int) or shots < 1:
        raise ValueError(f"The value entered for 'shots' parameter must be a POSITIVE INTEGER. Got '{shots}")
    if not isinstance(noise_rate, (int, float)):
        raise ValueError(f"The value entered for 'noise_rate' parameter must be a number. Got '{noise_rate}'")
    if noise_rate < 0.0:
        raise ValueError(f"The value entered for 'noise_rate' parameter cannot be negative. Got '{noise_rate}'")
    if noise_rate > 1.0:
        raise ValueError(f"The value entered for 'noise_rate' parameter cannot exceed 1.0. Got '{noise_rate}'")
    if not isinstance(optimization_level, int):
        raise ValueError(f"The value entered for 'optimization_level' parameter must be an INTEGER. Got '{optimization_level}'")
    if optimization_level not in [0, 1, 2, 3]:
        raise ValueError(f"The value entered for 'optimization_level' parameter must be 0, 1, 2, or 3. Got '{optimization_level}'")
    if correct_answer is not None:
        if not isinstance(correct_answer, str):
            raise ValueError(f"The value entered for 'correct_answer' parameter must be a string of 0s and 1s. Got '{correct_answer}'")
        if not all(bit in '01' for bit in correct_answer):
            raise ValueError(f"The value entered for 'correct_answer' parameter must only contain '0' and '1'. Got '{correct_answer}'")
        if len(correct_answer) != qc.num_qubits:
            raise ValueError(f"The value entered for 'correct_answer' parameter length ({len(correct_answer)}) must match "
                             f"the circuit qubit count ({qc.num_qubits})")
    
    # calculate the ideal probabilities
    ideal_probs = Statevector(qc).probabilities_dict()

    # add measurement so the simulator can actually run
    qc.measure_all()

    # use AerSimulator
    simulator = AerSimulator()
    
    # adding noise model for noise detection
    noise_model = None
    if noise_rate > 0.0:
        noise_model = NoiseModel()
        error_1q = depolarizing_error(noise_rate, 1)
        error_2q = depolarizing_error(noise_rate * 2, 2)
        noise_model.add_all_qubit_quantum_error(error_1q, ['u'])
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    # transpile circuit for the simulator
    # convert all gates to either be 'u' or 'cx' for simplicity (one-qubit vs two-qubit gate)
    transpiled_qc = transpile(qc, simulator, optimization_level=optimization_level, basis_gates=['cx', 'u'])

    # extract static metrics
    depth = transpiled_qc.depth()
    num_qubits = transpiled_qc.num_qubits

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
    job_result = simulator.run(transpiled_qc, shots=shots, noise_model=noise_model, seed_simulator=seed).result()
    end_time = time.time()

    # calculating runtime
    runtime = end_time - start_time

    # get raw counts and convert them to measured probabilities
    counts = job_result.get_counts()
    measured_probs = {}

    for state, count in counts.items():
        measured_probs[state] = count / shots

    # calculate Total Variation Distance (TVD)
    all_states = set(ideal_probs.keys()).union(set(measured_probs.keys()))
    tvd = 0.0

    # calculate TVD
    for state in all_states:
        ideal_val = ideal_probs.get(state, 0.0)
        measured_val = measured_probs.get(state, 0.0)
        tvd += abs(ideal_val - measured_val)

    tvd = 0.5 * tvd

    top_state = max(measured_probs, key=measured_probs.get) if measured_probs else None

    # calculating success probability
    success_prob = None
    if correct_answer is not None:
        success_prob = measured_probs.get(correct_answer, 0.0)

    # make a returnable dictionary
    output_metrics = {
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
        'top_state':            str(top_state) if top_state is not None else None,
        'success_probability':  success_prob,
    }

    return output_metrics