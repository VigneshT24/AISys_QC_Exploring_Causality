import pandas as pd 
import streamlit as st
import os

@st.cache_data
def load_results():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "data", "experiment_results.csv")
    return pd.read_csv(csv_path)