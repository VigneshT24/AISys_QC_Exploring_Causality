import pandas as pd
import numpy as np
from dowhy import gcm
from dowhy.gcm.ml.regression import SklearnRegressionModel
from sklearn.ensemble import HistGradientBoostingRegressor


def build_and_fit_models(data_file, graph_main, graph_grover):
    """Rebuilds and fits the two different models, similar to what was done in Task 6.
       
       "main_model" is the model that doesn't contain the success probability metric
       "grover_model" is the model that only contains success probability metric
    """
    np.random.seed(42)

    # creating an invertible SCM to perform counterfactual analysis
    main_model = gcm.InvertibleStructuralCausalModel(graph_main)
    grover_model = gcm.InvertibleStructuralCausalModel(graph_grover)

    grover_df = data_file[data_file['circuit_name'] == 'Grover'][list(graph_grover.nodes)]
    main_df = data_file[list(graph_main.nodes)]

    for root in ['shots', 'noise_rate', 'optimization_level', 'num_qubits', 'circuit_name']:
        main_model.set_causal_mechanism(root, gcm.EmpiricalDistribution())
    for non_root in ['tvd', 'depth', 'count_2q', 'runtime']:
        main_model.set_causal_mechanism(non_root, gcm.AdditiveNoiseModel(SklearnRegressionModel(HistGradientBoostingRegressor())))

    for root in ['noise_rate', 'depth', 'count_2q']:
        grover_model.set_causal_mechanism(root, gcm.EmpiricalDistribution())
    grover_model.set_causal_mechanism('success_probability', gcm.AdditiveNoiseModel(SklearnRegressionModel(HistGradientBoostingRegressor())))

    # fitting the data to be analyzed
    gcm.fit(main_model, main_df)
    gcm.fit(grover_model, grover_df)

    # returning the models and the data file
    return main_model, grover_model, main_df, grover_df