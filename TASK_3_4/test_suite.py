import sys
import os
import numpy as np
import pandas as pd
import itertools
from tqdm import tqdm
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
    """
    Generates a flat list of every experiment configuration to run.

    Combines all circuits with every combination of shots, optimization level,
    noise rate, qubit count, and depth using itertools.product. Each experiment
    is represented as a dictionary containing all the parameters needed to build
    and run a single circuit evaluation.

    Args:
        None

    Returns:
        'experiments': a list of dictionaries, where each dictionary represents
        one unique experiment configuration containing keys: 'circuit_name',
        'n_qubits', 'depth', 'shots', 'optimization_level', 'noise_rate',
        and 'correct_answer'

    Raises:
        None
    """
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
    """
    Builds and evaluates a single quantum circuit from a configuration dictionary.

    Designed to be called by ProcessPoolExecutor as a parallel worker. Receives
    one experiment config from build_experiments(), constructs the appropriate
    circuit using BasicQuantumCircuits, and passes it to evaluate_circuit().
    Must remain a top-level function for Python's pickle serialization to work
    correctly with multiprocessing.

    Args:
        'config': a dictionary containing one experiment's full configuration,
        as produced by build_experiments(). Expected keys are 'circuit_name',
        'n_qubits', 'depth', 'shots', 'optimization_level', 'noise_rate',
        and 'correct_answer'

    Returns:
        a dictionary of results from evaluate_circuit(), with two additional
        keys appended: 'n_qubits_config' and 'depth_config' from the original
        config for traceability in the final dataset

    Raises:
        ValueError: if 'circuit_name' in config does not match any known circuit
    """
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
    all_results = []

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_single_experiment, exp): exp
            for exp in experiments
        }

        with tqdm(total=total, desc="Running Experiments", unit="exp") as pbar:
            for future in as_completed(futures):
                try:
                    result = future.result()
                    all_results.append(result)

                    pbar.set_postfix({
                        'circuit':  result['circuit_name'],
                        'TVD':      f"{result['tvd']:.4f}",
                        'noise':    result['noise_rate']
                    })
                    pbar.update(1)
                
                except Exception as e:
                    failed = futures[future]
                    tqdm.write(f"FAILED: {failed['circuit_name']} - {type(e).__name__}: {e}")
                    import traceback
                    tqdm.write(traceback.format_exc())  # full stack trace
                    pbar.update(1)
    
    df = pd.DataFrame(all_results)
    df.to_csv('experiment_results.csv', index=False)
    print(f"\n Done! {len(all_results)}/{total} experiments completed.")