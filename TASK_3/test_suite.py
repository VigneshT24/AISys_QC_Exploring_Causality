import sys
import os
import numpy as np
import pandas as pd
import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'TASK_2'))

from basic_quantum_circuits import BasicQuantumCircuits as BQC
from evaluate_circuit import evaluate_circuit, show_circuit

shots_list          = [128, 512, 1024, 4096]
optimization_levels = [0, 1, 2, 3]
noise_rates         = [0.0, 0.001, 0.01, 0.05]
qubit_counts        = [2, 3, 4, 5]
depth_counts        = [1, 3, 5, 10]
grover_targets      = {2: '11', 3: '101', 4: '1001'}

def build_experiments():
    experiments = []

    # BELL
    for shots, opt, noise in itertools.product(shots_list, optimization_levels, noise_rates):
        experiments.append({
            'circuit_name':       'Bell',
            'n_qubits':           2,
            'depth':              None,
            'shots':              shots,
            'optimization_level': opt,
            'noise_rate':         noise,
            'correct_answer':     None
        })

    # GHZ
    for n, shots, opt, noise in itertools.product(qubit_counts, shots_list, optimization_levels, noise_rates):
        experiments.append({
            'circuit_name':       'GHZ',
            'n_qubits':           n,
            'depth':              None,
            'shots':              shots,
            'optimization_level': opt,
            'noise_rate':         noise,
            'correct_answer':     None
        })
    
    # GROVER
    for n, shots, opt, noise in itertools.product([2, 3, 4], shots_list, optimization_levels, noise_rates):
        experiments.append({
            'circuit_name':       'Grover',
            'n_qubits':           n,
            'depth':              None,
            'shots':              shots,
            'optimization_level': opt,
            'noise_rate':         noise,
            'correct_answer':     grover_targets[n]
        })

    # PARAMETERIZED
    for n, shots, opt, noise in itertools.product(qubit_counts, shots_list, optimization_levels, noise_rates):
        experiments.append({
            'circuit_name':       'Parameterized',
            'n_qubits':           n,
            'depth':              None,
            'shots':              shots,
            'optimization_level': opt,
            'noise_rate':         noise,
            'correct_answer':     None
        })
    
    # VARIABLE DEPTH
    for depth, shots, opt, noise in itertools.product(depth_counts, shots_list, optimization_levels, noise_rates):
        experiments.append({
            'circuit_name':       'Variable Depth',
            'n_qubits':           2,
            'depth':              depth,
            'shots':              shots,
            'optimization_level': opt,
            'noise_rate':         noise,
            'correct_answer':     None
        })

    return experiments

def run_single_experiment(config):
    circuit = BQC()

    name = config['circuit_name']

    if name == 'Bell':
        qc = circuit.bell_state_circuit()

    elif name == 'GHZ':
        qc = circuit.ghz_state_circuit(n_qubits=config['n_qubits'])
    
    elif name == 'Grover':
        qc = circuit.grover_circuit(
            n_qubits=config['n_qubits'],
            target=config['correct_answer']
        )
    
    elif name == 'Parameterized':
        angles = [('ry', np.pi / (i + 1)) for i in range(config['n_qubits'])]
        qc = circuit.parameterized_circuit(
            n_qubits=config['n_qubits'],
            axis_angles_list=angles
        )
    
    elif name == 'Variable Depth':
        qc = circuit.variable_depth_circuit(
            n_qubits=config['n_qubits'],
            depth=config['depth']
        )

    
    result = evaluate_circuit(
        circuit_name=config['circuit_name'],
        qc=qc,
        shots=config['shots'],
        optimization_level=config['optimization_level'],
        noise_rate=config['noise_rate'],
        correct_answer=config['correct_answer']
    )

    result['n_qubits_config'] = config['n_qubits']
    result['depth_config']    = config['depth']

    return result

if __name__ == "__main__":
    experiments = build_experiments()
    total = len(experiments)
    print(f"Total experiments to run {total}")

    all_results = []
    completed = 0

    with ProcessPoolExecutor(max_workers=4) as executor:

        futures = {
            executor.submit(run_single_experiment, exp): exp
            for exp in experiments
        }

        for future in as_completed(futures):
            try:
                result = future.result()
                all_results.append(result)
                completed += 1
                print(f"[{completed}/{total}] Done: {result['circuit_name']} | "
                      f"shots={result['shots']} | "
                      f"opt={result['optimization_level']} | "
                      f"noise={result['noise_rate']} | "
                      f"TVD={result['tvd']:.4f}")
                
            except Exception as e:
                failed_config = futures[future]
                print(f"FAILED: {failed_config['circuit_name']} - {e}")
    
    df = pd.DataFrame(all_results)
    df.to_csv('experiment_results.csv', index=False)

    print(f"\nFinished! {completed}/{total} experiments completed.")
    print(f"Results saved to experiment_results.csv")
    print(f"\nPreview:")
    print(df.head(10))
    print(f"\nShape: {df.shape}")