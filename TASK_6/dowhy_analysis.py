import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'TASK_5'))

from dowhy import gcm
import pandas as pd
from causal_graph import get_nx

graph_1 = get_nx(only_sp=False) # all edges without success_probability
graph_2 = get_nx(only_sp=True) # all edges with only success_probability

# initialize two different models for avoiding NaN error
main_model = gcm.StructuralCausalModel(graph_1)
grover_model = gcm.StructuralCausalModel(graph_2)

# load general data_file
data_file = pd.read_csv('C:/Users/vigne/Qiskit/AISys_QC_Exploring_Casualty/TASK_3_4/experiment_results.csv')

# then initialize two seperate files for the two different models initialized earlier
grover_df = data_file[data_file['circuit_name'] == 'Grover'][list(graph_2.nodes)]
main_df = data_file[list(graph_1.nodes)]

# assign each of the model to causal mechanisms
gcm.auto.assign_causal_mechanisms(main_model, main_df)
gcm.auto.assign_causal_mechanisms(grover_model, grover_df)


# print out the node --> causal_mechanism
for node in main_model.graph.nodes:
    print(node, "-->", main_model.causal_mechanism(node))

print("\n", "------------------", "\n")

for node in grover_model.graph.nodes:
    print(node, "-->", grover_model.causal_mechanism(node))

# fitting the data from the two different models
gcm.fit(main_model, main_df)
gcm.fit(grover_model, grover_df)