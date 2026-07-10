# AISys: Exploring Causality in Quantum Computing Systems

REU Project exploring how causal inference can be used to understand 
and explain quantum computing workflows. The project 
uses IBM Qiskit to run controlled quantum circuit experiments, collects structured 
execution data, builds causal graphs, and performs causal and counterfactual 
analysis using DoWhy's graphical causal model (GCM) module.

## Project Structure
- `TASK_1/` - Qiskit learning notebooks
- `TASK_2/` - Quantum benchmark circuit library
- `TASK_3_4/` - Experiment runner and metrics evaluation
- `TASK_5/` - Constructing Causal Models, with explanations
- `TASK_6/` - Conducting DoWhy Causal and Counterfactual Analysis
- `TASK_7/` - Streamlit Tool
- `TASK_8/` - Final Report

## Setup

### Requirements
- Python 3.12+
- Install dependencies:
pip install -r requirements.txt

### Running the Benchmark Suite
```bash
cd TASK_3_4
python test_suite.py
```
This generates `experiment_results.csv` with ~2736 experiment results.

## Mentors
- Pooyan Jamshidi, University of South Carolina
- Mohammad Ali Javidian, Appalachian State University
