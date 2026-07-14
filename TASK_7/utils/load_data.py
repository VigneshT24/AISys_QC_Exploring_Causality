import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_results():
    """Loading the data from the csv file in data (no live simulation)"""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # TASK_7/utils
    task7_dir = os.path.dirname(current_dir)                   # TASK_7
    csv_path = os.path.join(task7_dir, "data", "experiment_results.csv")
    return pd.read_csv(csv_path)