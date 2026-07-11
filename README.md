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
