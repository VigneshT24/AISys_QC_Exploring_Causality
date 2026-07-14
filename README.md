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
1. Does increasing circuit depth cause a measurable decrease in output quality under a fixed noise model?
2. Does Qiskit’s transpilation optimization level reduce gate count or circuit depth enough to improve output quality?
3. How does the number of shots affect the stability of the measured output distribution?
4. Which has a stronger effect on output quality: circuit depth, two-qubit gate count, or simulated noise rate?
5. Can a simple causal graph help explain how quantum workflow configurations influence observed outcomes?
6. What would the output quality have been if the same circuit had been run with a lower noise rate or a different optimization level?

## Key Findings
- **``noise_rate``** is the most consequential causal variable for output quality and algorithmic correctness (success probability), approximately 2 times stronger than circuit depth and 5 times stronger than two-qubit gate count.
- **``optimization_level``** has a negligible direct effect on output quality (TVD) for the simple set of benchmark circuits tested (~1% change).
- **``shots``** has the weakest causal effect on output quality, with diminishing returns on TVD past ~2000 shots.
- DoWhy's **GCM** Counterfactual analysis shows that fixing the **``noise_rate``** to 0.001 (low noise) would reduce mean TVD by ~67.3% (0.10445 to 0.03412), which is a significant increase in output quality.
- Grover's **``success_probability``** improves by ~28% (0.57483 to 0.73580) under low noise conditions.

## Setup

### Requirements
- Python 3.11+

First, clone the repo to VS Code:
```bash
git clone https://github.com/VigneshT24/AISys_QC_Exploring_Causality.git
```

Then install the dependencies:
```bash
pip install -r requirements.txt
```

### Running the Experiment Pipeline
To regenerate ``experiment_results.csv`` from scratch:

First, navigate to the root repo, then:
```bash
cd Task_3_4
```
Then:
```bash
python test_suite.py
```

**Note**: This may take several minutes. Generates ~12,672 rows across 5 circuits 
and all configuration combinations.

## Causal Graph

The causal graph connects workflow configurations (column 1) to outcome metrics (column 3) through two mediator variables (column 2):

<img width="2265" height="1731" alt="causal_graph" src="https://github.com/user-attachments/assets/e9479568-8030-459a-a1d1-b975b3158fdc" />

**Causal Variables:** ``shots``, ``noise_rate``, ``optimization_level``, ``num_qubits``, ``circuit_name`` 

**Mediators:** ``depth``, ``count_2q``  

**Outcome Metrics:** ``tvd``, ``runtime``, ``success_probability`` (Grover only)

See `TASK_5/causal_explanation.md` for full justification of every edge.

## Streamlit Dashboard to Explore Causality

Screenshots of Dashboard:

<figure>
  <img width="1887" height="917" alt="Circuit Diagram tab showing a rendered quantum circuit for the selected configuration" src="https://github.com/user-attachments/assets/d13a042c-c089-4c78-af11-b1d4c267c00d" />
  <figcaption>Figure 1: Circuit Diagram tab, rendering a live-built circuit based on the selected benchmark circuit and configuration.</figcaption>
</figure>
<br><br><br><br>
<figure>
  <img width="1887" height="917" alt="Data Explorer tab showing the various metrics after selecting a configuration" src="https://github.com/user-attachments/assets/1dd04ad2-4ee8-4b2d-8620-cedf1e2bbca4" />
  <figcaption>Figure 2: Data Explorer tab, showing data after selecting a certain configuration.</figcaption>
</figure>
<br><br><br><br>
<figure>
  <img width="1887" height="917" alt="Counterfactual Analysis tab showing counterfactual result" src="https://github.com/user-attachments/assets/81ee3a7b-2956-4d51-aebe-d38951aa098d" />
  <figcaption>Figure 3: Counterfactual Analysis tab showing counterfactual result after selecting a certain configuration.</figcaption>
</figure>
<br><br><br><br>

Check out the dashboard:
https://aisys-quantumcausality.streamlit.app/

## Mentors
- Pooyan Jamshidi, University of South Carolina
- Mohammad Ali Javidian, Appalachian State University
