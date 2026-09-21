import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="LH2 Turnaround Simulation", layout="wide")

st.title("✈️ Stochastic LH2 Aircraft Turnaround & Infrastructure Simulation")
st.write("Discrete-Event & Monte Carlo Model for LH2 Cryogenic Refueling Bottlenecks")

st.sidebar.header("Simulation Parameters")
num_runs = st.sidebar.slider("Monte Carlo Runs", 10, 500, 100)
mass_flow_rate = st.sidebar.slider("Mass Flow Rate (kg/s)", 0.5, 2.0, 1.0)
dispenser_capacity = st.sidebar.selectbox("Dispenser Capacity (N)", [1, 2])

if st.button("Run Simulation"):
    # Stochastic Simulation Logic
    np.random.seed(42)
    
    # Base turnaround times with stochastic noise
    boarding_time = np.random.triangular(20, 30, 45, num_runs)
    refueling_base = (3000 / (mass_flow_rate * 60)) / dispenser_capacity
    pressure_fluctuation = np.random.uniform(0.9, 1.1, num_runs)
    
    refueling_time = refueling_base * pressure_fluctuation
    bog_loss = np.random.exponential(scale=1.5, size=num_runs)
    
    total_turnaround = boarding_time + refueling_time + (bog_loss * 0.2)
    
    mean_tat = np.mean(total_turnaround)
    
    st.success(f"Simulation Complete! Mean Turnaround Time (TAT): **{mean_tat:.2f} minutes**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Turnaround Time Distribution")
        fig, ax = plt.subplots()
        ax.hist(total_turnaround, bins=15, color='skyblue', edgecolor='black')
        ax.set_xlabel("Turnaround Time (min)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
        
    with col2:
        st.subheader("Summary Metrics")
        df_res = pd.DataFrame({
            "Metric": ["Mean TAT (min)", "Min TAT (min)", "Max TAT (min)", "Avg BOG Loss (kg)"],
            "Value": [f"{mean_tat:.2f}", f"{np.min(total_turnaround):.2f}", f"{np.max(total_turnaround):.2f}", f"{np.mean(bog_loss):.2f}"]
        })
        st.table(df_res)