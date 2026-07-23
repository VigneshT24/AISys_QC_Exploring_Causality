![Python](https://img.shields.io/badge/Python-3.11-blue)
![Qiskit](https://img.shields.io/badge/Qiskit-IBM-6929C4)
![DoWhy](https://img.shields.io/badge/DoWhy-GCM-green)
![Streamlit](https://img.shields.io/badge/Streamlit-deployed-FF4B4B)
# AISys: Exploring Causality in Quantum Computing Systems

REU Project exploring how causal inference can be used to understand and explain quantum computing workflows. The project 
uses IBM Qiskit to run controlled quantum circuit experiments, collects structured execution data, builds causal graphs,
and performs causal and counterfactual analysis using DoWhy's graphical causal model (GCM) module.

## Project Structure
- `TASK_1/` - Qiskit learning notebook
- `TASK_2/` - Quantum benchmark circuit library
- `TASK_3_4/` - Experiment runner and metrics evaluation
- `TASK_5/` - Constructing Causal Models, with explanations
- `TASK_6/` - Conducting DoWhy Causal and Counterfactual Analysis
- `TASK_7/` - Streamlit Tool
- `TASK_8/` - Final Report

## Research Questions
1. Does increasing configured depth cause a measurable decrease in output quality under a fixed noise model?
2. Does Qiskit’s transpilation optimization level reduce gate count or transpiled depth enough to improve output quality?
3. How does the number of shots affect the stability of the measured output distribution?
4. Which has a stronger effect on output quality: transpiled depth, two-qubit gate count, or simulated noise rate?
5. Can a simple causal graph help explain how quantum workflow configurations influence observed outcomes?
6. What would the output quality have been if the same circuit had been run with a lower noise rate or a different optimization level?

## Key Findings
- **`noise_rate`** is the most consequential causal variable for output quality and target-state success probability, approximately 2 times stronger than transpiled depth and 5 times stronger than two-qubit gate count.
- **`optimization_level`** has a negligible direct effect on output quality (TVD) for the simple set of benchmark circuits tested (~1% change).
- **`shots`** has the weakest causal effect on output quality, with diminishing returns on TVD past ~2000 shots.
- DoWhy's **GCM** Counterfactual analysis shows that fixing the **`noise_rate`** to 0.001 (low noise) would reduce mean TVD by ~67.3% (0.10445 to 0.03412), which is a significant increase in output quality.
- Grover's **`success_probability`** improves by ~28% (0.57483 to 0.73580) under low noise conditions.

## Setup

### Requirements
- Python 3.11+

First, clone the repo and navigate into the directory:
```bash
git clone [https://github.com/VigneshT24/AISys_QC_Exploring_Causality.git](https://github.com/VigneshT24/AISys_QC_Exploring_Causality.git)
```
Then:
```
cd AISys_QC_Exploring_Causality
```

Then install all required dependencies:
```bash
pip install -r requirements.txt
```

### Reproducibility & Random Seeds
To ensure stable causal estimates and reproducible simulator results, a fixed random seed (`42`) is utilized throughout the entire pipeline. This explicit seed is passed to the Qiskit `AerSimulator` measurement executions (in `evaluate_circuit.py`) and is used for the DoWhy causal mechanism fitting and bootstrap resampling (in `TASK_6/analysis_notebook.ipynb`).

### 1. Generating the Dataset
To regenerate the `experiment_results.csv` dataset from scratch:
```bash
cd TASK_3_4
python test_suite.py
```
**Note**: This utilizes parallel processing but may still take several minutes. It generates exactly 12,672 execution rows across the 5 benchmark circuits and all configuration combinations.

### 2. Reproducing Figures & Causal Analysis
The project splits analysis into two parts: standard metrics visualization and DoWhy causal/counterfactual analysis.
*   **Visualizing Metrics:** Run `visual_view.py` to regenerate the high-quality Matplotlib/Seaborn boxplots and line charts used in the report.
*   **Causal Analysis:** Navigate to `TASK_6/` and execute the `analysis_notebook.ipynb` Jupyter Notebook. This notebook imports the NetworkX graph from `TASK_5`, builds the Invertible Structural Causal Models (GCM), calculates arrow strengths, and performs the counterfactual sampling.

### 3. Running the Streamlit Dashboard
You do not need to download the repository to explore the causal findings. You can visit the live deployed dashboard here: 
**[https://aisys-quantumcausality.streamlit.app/](https://aisys-quantumcausality.streamlit.app/)**

However, if you wish to run the dashboard locally:
```bash
cd TASK_7
streamlit run app.py
```

## Causal Graph

The causal graph connects workflow configurations (column 1) to outcome metrics (column 3) through two mediator variables (column 2):

<img width="2265" height="1731" alt="causal_graph" src="https://github.com/user-attachments/assets/e9479568-8030-459a-a1d1-b975b3158fdc" />

**Causal Variables:** ``shots``, ``noise_rate``, ``optimization_level``, ``num_qubits``, ``circuit_name`` 

**Mediators:** ``depth``, ``count_2q``  

**Outcome Metrics:** ``tvd``, ``runtime``, ``success_probability`` (Grover only)

See `TASK_5/causal_explanation.md` for full justification of every edge.

## Mentors
- Pooyan Jamshidi, University of South Carolina
- Mohammad Ali Javidian, Appalachian State University

## Read the Full Research Report
**For a comprehensive breakdown of the methodology, experiment explanations, and the final report for this project, please refer to the complete report located in the [`TASK_8/`](TASK_8/) directory.**
