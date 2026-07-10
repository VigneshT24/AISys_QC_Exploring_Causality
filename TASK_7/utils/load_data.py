import pandas as pd 
import streamlit as st


@st.cache_data
def load_results(path="..\TASK_7\data\experiment_results.csv"):
    return pd.read_csv(path)