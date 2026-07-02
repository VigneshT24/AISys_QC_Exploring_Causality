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


# # print out the node --> causal_mechanism
for node in main_model.graph.nodes:
    print(node, "-->", main_model.causal_mechanism(node))

print("\n", "------------------", "\n")

for node in grover_model.graph.nodes:
    print(node, "-->", grover_model.causal_mechanism(node))

# fitting the data from the two different models, for analysis
gcm.fit(main_model, main_df)
gcm.fit(grover_model, grover_df)


tvd_strength = gcm.arrow_strength(main_model, target_node='tvd')

# the following is to convert np.float64() to float, and then sort it in decending order
ordered_tvd_strength = {}
for key, val in tvd_strength.items():
    ordered_tvd_strength[key] = (float(val) * 100)


ordered_tvd_strength = dict(sorted(ordered_tvd_strength.items(), key=lambda item: item[1], reverse=True))

# --------------------------------------------
#             ANSWER TO QUESTION 1
# --------------------------------------------
print()
print("----- QUESTION 1: Does increasing circuit depth cause a measurable decrease in output quality under a fixed noise model? -----")
print()
# ALL THREE OF THE FOLLOWING COMPONENTS NEEDED TO FULLY ANSWER QUESTION 1

# 1) "Variable Depth - TVD vs Circuit Depth, by Noise Level" Chart

# 2) "ordered_tvd_strength" second key and value
second_key, second_value = list(ordered_tvd_strength.items())[1]
print(second_key, " --- ", second_value)

# 3) "depth --> tvd" edge from causal_graph.py


# --------------------------------------------
#             ANSWER TO QUESTION 2
# --------------------------------------------
print()
print("----- QUESTION 2: Does Qiskit's transpilation optimization level reduce gate count or circuit depth enough to improve output quality? -----")
print()
# ALL TWO OF THE FOLLOWING COMPONENTS NEEDED TO FULLY ANSWER QUESTION 2

# 1) "depth_strength" and "count_2q_strength" to see strength of optimization_level -> depth/count_2q
depth_strength = gcm.arrow_strength(main_model, target_node='depth')
count_2q_strength = gcm.arrow_strength(main_model, target_node='count_2q')

ordered_depth_strength = {}
ordered_count_2q_strength = {}

for key, val in depth_strength.items():
    ordered_depth_strength[key] = (float(val) * 100)

for key, val in count_2q_strength.items():
    ordered_count_2q_strength[key] = (float(val) * 100)

ordered_depth_strength = dict(sorted(ordered_depth_strength.items(), key=lambda item: item[1], reverse=True))
ordered_count_2q_strength = dict(sorted(ordered_count_2q_strength.items(), key=lambda item: item[1], reverse=True))

opt_depth = next(reversed(ordered_depth_strength.items()))
opt_count_2q = next(reversed(ordered_count_2q_strength.items()))

print(opt_depth)
print(opt_count_2q)

# 2) four different charts:
    # (1) "Transpiled Depth by Optimization Level, All Circuits"
    # (2) "Two-Qubit Gate Count by Optimization Level, All Circuits"
    # (3) "TVD by Transpiled Depth, All Circuits"
    # (4) "TVD by Two-Qubit Gate Count, All Circuits"

# Basically, (1) and (2) don't show much meaningful curves due to lack of heavy complexity of the five basic quantum circuit,
# however, (3) and (4) prove that in general, by increasing the "depth" and "count_2q", the "TVD" generally gets higher. Therefore,
# for more complicated circuits, this trend will be more clear since transiplation optimization level from Qiskit is defined to try to
# combine and reduce gate count and depth (as possible) to make a circuit equivalent to another same circuit with length and complexity


# --------------------------------------------
#             ANSWER TO QUESTION 3
# --------------------------------------------
print()
print("----- QUESTION 3: How does the number of shots affect the stability of the measured output distribution? -----")
print()
# ALL THREE OF THE FOLLOWING COMPONENTS NEEDED TO FULLY ANSWER QUESTION 3

# 1) "ordered_tvd_strength" weakest strength value, which is (shots -> TVD), showing that there exists a relation between shots and TVD directly
weakest_pair = next(reversed(ordered_tvd_strength.items()))
print(weakest_pair)

# 2) "TVD Stability by Shot Count, All Circuits" chart showing initial reduction in TVD and then a diminshing returns curve, as shots gets higher

# 3) "shots --> tvd" edge from causal_graph.py

# --------------------------------------------
#             ANSWER TO QUESTION 4
# --------------------------------------------
print()
print("----- QUESTION 4: Which has a stronger effect on output quality: circuit depth, two-qubit gate count, or simulated noise rate? -----")
print()
i = 1 
for a, b in ordered_tvd_strength.items():
    print("(", a[0], " -->> ", a[1], ") : ", b)
    i+=1
    # only print out the top 3 to answer QUESTION 4
    if i == 4:
        break
print()
first_key, first_value = list(ordered_tvd_strength.items())[0]
print(f"\"{first_key[0]}\" has the STRONGEST EFFECT on output quality (TVD).")
print()

# --------------------------------------------
#             ANSWER TO QUESTION 5
# --------------------------------------------
print()
print("----- QUESTION 5: Can a simple causal graph help explain how quantum workflow configurations influence observed outcomes? -----")
print()