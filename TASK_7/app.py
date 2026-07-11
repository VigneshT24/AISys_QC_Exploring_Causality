import streamlit as st
import pandas as pd
import os
import sys
import numpy as np
import altair as alt
from dowhy import gcm

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
task2_dir = os.path.join(parent_dir, "TASK_2")
task5_dir = os.path.join(parent_dir, "TASK_5")

sys.path.append(task2_dir)
sys.path.append(task5_dir)

from basic_quantum_circuits import BasicQuantumCircuits
from utils.load_data import load_results
from utils.counterfactual import build_and_fit_models
from causal_graph import get_nx

@st.cache_resource
def get_fitted_models():
    graph_main = get_nx(only_sp=False)
    graph_grover = get_nx(only_sp=True)
    df = load_results()
    return build_and_fit_models(df, graph_main, graph_grover)

main_model, grover_model, main_df, grover_df = get_fitted_models()

st.set_page_config(page_title="QC Causal Explorer", layout="wide")
st.title("Exploring Causality in Quantum Computing Systems")
st.sidebar.header("Filters")


st.sidebar.header("Causal Variables")
circuit = st.sidebar.selectbox(
    "Circuit",
    ["Bell", "GHZ", "Grover", "Parameterized", "Variable Depth"]
)

num_qubits = st.sidebar.select_slider(
    "Number of Qubits",
    options=[2, 3, 4, 5]
)

shots = st.sidebar.select_slider(
    "Shots",
    options=[128, 256, 512, 1024, 2048, 4096]
)

noise_rate = st.sidebar.select_slider(
    "Noise Rate",
    options=[0.0, 0.001, 0.005, 0.01, 0.03, 0.05]
)

optimization_level = st.sidebar.select_slider(
    "Optimization level", 
    [0, 1, 2, 3]
)

if circuit == "Grover":
    st.sidebar.markdown("---")
    st.sidebar.header("Other Configurable Parameters")
    st.sidebar.caption("These affect the circuit structure but are not modeled as independent causal variables.")

    default_targets = {2: '11', 3: '101', 4: '1001', 5: '10101'}
    target = st.sidebar.text_input(
        f"Target state ({num_qubits} bits)",
        value=default_targets.get(num_qubits, '1' * num_qubits),
        max_chars=num_qubits,
        key="grover_target"
    )

    if len(target) != num_qubits or not all(bit in '01' for bit in target):
        st.sidebar.error(f"Target must be exactly {num_qubits} bits, using only 0s and 1s.")
        target = default_targets.get(num_qubits, '1' * num_qubits)

if circuit == "Parameterized":
    st.sidebar.markdown("---")
    st.sidebar.header("Other Configurable Parameters")
    st.sidebar.caption("These affect the circuit structure but are not modeled as independent causal variables.")
    axis_options = ['rx', 'ry', 'rz']
    angle_options_deg = [0, 30, 45, 60, 90, 120, 135, 180, 270, 360]
    angles = []

    for i in range(num_qubits):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            axis = st.selectbox(f"Qubit {i} axis", axis_options, key=f"axis_{i}")
        with col2:
            angle_deg = st.number_input(f"Qubit {i} angle (°)", min_value=0, max_value=360, value=45, step=15, key=f"angle_{i}")
        angles.append((axis, np.radians(angle_deg)))

if circuit == "Variable Depth":
    st.sidebar.markdown("---")
    st.sidebar.header("Other Configurable Parameters")
    st.sidebar.caption("These affect the circuit structure but are not modeled as independent causal variables.")
    depth = st.sidebar.select_slider(
        "Circuit Depth",
        options=[1, 2, 3, 5, 7, 10, 15]
    )

tab1, tab2, tab3, tab4 = st.tabs(["Data Explorer", "Causal Graph", "Counterfactuals", "Circuit Diagram"])

with tab1:
    df = load_results()

    # sidebar filters
    filtered_df = df[
        (df['circuit_name'] == circuit) &
        (df['num_qubits'] == num_qubits) &
        (df['shots'] == shots) &
        (df['noise_rate'] == noise_rate) &
        (df['optimization_level'] == optimization_level)
    ]

    st.subheader(f"Filtered results ({len(filtered_df)} runs)")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("Metric Summary")
    metric_cols = ['tvd', 'runtime', 'depth', 'count_2q']
    if circuit == "Grover":
        metric_cols.append('success_probability')

    summary = filtered_df[metric_cols].agg(['mean', 'std', 'min', 'max']).T
    st.dataframe(summary, use_container_width=True)

    st.subheader("TVD Distribution")

    if not filtered_df.empty:
        tvd_counts = filtered_df['tvd'].value_counts(bins=20).sort_index().reset_index()
        tvd_counts.columns = ['tvd_bin', 'count']
        tvd_counts['tvd_bin'] = tvd_counts['tvd_bin'].apply(lambda interval: interval.left)

        chart = alt.Chart(tvd_counts).mark_bar().encode(
            x=alt.X('tvd_bin:Q', title='TVD value'),
            y=alt.Y('count:Q', title='Number of runs')
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No runs match the configuration that you chose. Try adjusting the filteres.")

with tab2:
    st.subheader("Causal Graph")
    st.caption("Nodes represent workflow configurations, mediators, and outcomes. " \
                "Edges represent modeled causal relationships.")
    st.image("..\CAUSAL_GRAPH\Causal_Graph.png")

with tab3:
    st.subheader("Counterfactual Analysis")
    st.caption("Ask: what would the outcome have been if a variable has a different value?")

    intervention_var = st.selectbox("Variable to intervene on", ["noise_rate", "optimization_level"])

    if intervention_var == "noise_rate":
        new_value = st.select_slider("New noise_rate value", options=[0.0, 0.001, 0.005, 0.01, 0.03, 0.05])
    else:
        new_value = st.select_slider("New optimization_level value", options=[0, 1, 2, 3])

    if st.button("Run counterfactual query"):
        cf_samples = gcm.counterfactual_samples(main_model, {intervention_var: lambda x: new_value}, main_df)

        observed_tvd = main_df['tvd'].mean()
        counterfactual_tvd = cf_samples['tvd'].mean()

        result_df = pd.DataFrame({
            'condition': ['Observed', f'Counterfactual ({intervention_var} = {new_value})'],
            'tvd': [observed_tvd, counterfactual_tvd]
        })

        chart = alt.Chart(result_df).mark_bar().encode(
            x=alt.X('condition:N', title='', sort=None,
                    axis=alt.Axis(labelAngle=0, labelLimit=300)),
            y=alt.Y('tvd:Q', title='Mean TVD'),
            color=alt.Color('condition:N',
                            scale=alt.Scale(domain=result_df['condition'].tolist(),
                                            range=['#8c1f1f', '#1f4e8c']),
                            legend=None)
        ).properties(height=350)

        text = chart.mark_text(align='center', baseline='bottom', dy=-8, fontSize=13, fontWeight='bold').encode(
            text=alt.Text('tvd:Q', format='.4f'),
            color=alt.value('white')
        )

        st.altair_chart(chart + text, use_container_width=True)

        pct_change = (counterfactual_tvd - observed_tvd) / observed_tvd * 100
        direction = "reduction" if pct_change < 0 else "increase"
        st.markdown(
            f"<p style='text-align: center; font-weight: bold;'>{abs(pct_change):.1f}% {direction} in mean TVD</p>",
            unsafe_allow_html=True
        )

with tab4:
    st.subheader(f"{circuit} circuit ({num_qubits} qubits)")

    if not filtered_df.empty:
        circuit_builder = BasicQuantumCircuits()
        if circuit == "Bell":
            qc = circuit_builder.bell_state_circuit()
        elif circuit == "GHZ":
            qc = circuit_builder.ghz_state_circuit(n_qubits=num_qubits)
        elif circuit == "Grover":
            target = {2: '11', 3: '101', 4: '1001', 5: '10101'}.get(num_qubits, '1' * num_qubits)
            qc = circuit_builder.grover_circuit(n_qubits=num_qubits, target=target)
        elif circuit == "Parameterized":
            qc = circuit_builder.parameterized_circuit(n_qubits= num_qubits, axis_angles_list=angles)
        elif circuit == "Variable Depth":
            qc = circuit_builder.variable_depth_circuit(n_qubits=num_qubits, depth=depth)
        else:
            qc = None
            st.info(f"{circuit} circuit is not one of the 5 benchmark circuit you can test.")

        if qc is not None:
            fig = qc.draw(output='mpl', style={'dpi': 1200})
            st.pyplot(fig)
    else:
        st.info("No matching configuration to build a circuit diagram for.")