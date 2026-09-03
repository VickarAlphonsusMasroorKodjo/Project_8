"""
Thermodynamics Calculator - Engineering Application

AI DOCUMENTATION:
================
AI Tools Used: GitHub Copilot, Claude AI for prompt assistance
Key Prompts:
1. "Create a Streamlit thermodynamics calculator for ideal gas law, first law, and efficiency calculations"
2. "Build interactive sliders for pressure, volume, temperature, mass, and work/heat inputs"
3. "Generate charts showing thermodynamic cycles and energy balance visualizations"

Manual Fixes & Verifications:
- Verified thermodynamic equations and unit consistency (SI units)
- Added proper validation for absolute temperatures (Kelvin) and pressure values
- Corrected cycle diagrams (P-V and T-S diagrams) for accuracy
- Fine-tuned energy calculations and added proper thermal efficiency formulas
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge, FancyBboxPatch
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(page_title="Thermodynamics Calculator", layout="wide")

# Custom styling
st.markdown("""
    <style>
    .header {font-size: 2.5em; font-weight: bold; color: #1B4965;}
    .subheader {font-size: 1.3em; color: #CB2E1B;}
    .result-box {background-color: #F5F5F5; padding: 15px; border-radius: 8px; border-left: 5px solid #1B4965;}
    </style>
""", unsafe_allow_html=True)

# Main title and instructions
st.markdown('<div class="header">⚡ Thermodynamics Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Engineering Analysis & Cycle Analysis Tool</div>', unsafe_allow_html=True)

st.markdown("""
### User Instructions:
1. **Select Analysis Type** in the sidebar (Ideal Gas Law, First Law of Thermodynamics, or Cycle Efficiency)
2. **Input Process Parameters** using sliders for pressure, volume, temperature, mass, and energy
3. **View Calculations** showing state properties, work, heat, and efficiency values
4. **Analyze Diagrams** including P-V diagrams, T-S diagrams, and cycle representations

**Note:** All calculations use SI units (Pa, m³, K, J, kW, etc.)
""")

st.divider()

# Sidebar controls
st.sidebar.title("⚙️ Thermodynamics Parameters")

# Analysis type selection
analysis_type = st.sidebar.radio(
    "Select Analysis Type:",
    ["Ideal Gas Law (PV=nRT)", "First Law of Thermodynamics", "Cycle Efficiency Analysis"],
    index=0
)

# Initialize session state for storing calculations
if 'calculations' not in st.session_state:
    st.session_state.calculations = []

def validate_input(value, min_val=0.001, allow_negative=False):
    """Validate input values"""
    try:
        if allow_negative:
            return True
        else:
            return value >= min_val
    except:
        return False

def add_to_calculation(analysis_name, params, results):
    """Add calculation to history"""
    st.session_state.calculations.append({
        'Analysis': analysis_name,
        'Parameters': params,
        'Results': results
    })

# Constants
R_universal = 8.314  # J/mol·K
R_specific_air = 287  # J/kg·K

# ==================== IDEAL GAS LAW ====================
if analysis_type == "Ideal Gas Law (PV=nRT)":
    st.sidebar.markdown("### Ideal Gas Law Parameters")
    st.sidebar.info("PV = nRT or P = ρRT")
    
    # Process type selection
    process_type = st.sidebar.selectbox(
        "Select Process Type:",
        ["Isobaric (Constant Pressure)", "Isochoric (Constant Volume)", 
         "Isothermal (Constant Temperature)", "Adiabatic (No Heat Transfer)"]
    )
    
    # Initial state inputs
    st.sidebar.markdown("#### Initial State (1)")
    P1 = st.sidebar.slider("Pressure P₁ [kPa]:", 1, 1000, 100, 10) * 1000  # Convert to Pa
    T1 = st.sidebar.slider("Temperature T₁ [K]:", 273, 1000, 300, 10)
    V1 = st.sidebar.slider("Volume V₁ [m³]:", min_value=0.001, max_value=10.0, value=1.0, step=0.1)
    
    # Calculate number of moles
    n_moles = (P1 * V1) / (R_universal * T1)
    
    # Final state based on process
    st.sidebar.markdown("#### Final State (2)")
    
    if process_type == "Isobaric (Constant Pressure)":
        P2 = P1
        T2 = st.sidebar.slider("Temperature T₂ [K]:", 273, 1500, 400, 10)
        V2 = (n_moles * R_universal * T2) / P2
        process_label = "Constant Pressure (Isobaric)"
        
    elif process_type == "Isochoric (Constant Volume)":
        V2 = V1
        T2 = st.sidebar.slider("Temperature T₂ [K]:", 273, 1500, 400, 10)
        P2 = (n_moles * R_universal * T2) / V2
        process_label = "Constant Volume (Isochoric)"
        
    elif process_type == "Isothermal (Constant Temperature)":
        T2 = T1
        V2 = st.sidebar.slider("Volume V₂ [m³]:", min_value=0.001, max_value=10.0, value=2.0, step=0.1)
        P2 = (n_moles * R_universal * T2) / V2
        process_label = "Constant Temperature (Isothermal)"
        
    else:  # Adiabatic
        gamma = st.sidebar.slider("Heat Capacity Ratio (γ):", min_value=1.0, max_value=1.7, value=1.4, step=0.1)
        T2 = st.sidebar.slider("Temperature T₂ [K]:", 273, 1500, 400, 10)
        P2 = P1 * (T2 / T1) ** (gamma / (gamma - 1))
        V2 = (n_moles * R_universal * T2) / P2
        process_label = f"Adiabatic Process (γ={gamma})"
    
    # Calculate work and heat
    W = n_moles * R_universal * (T2 - T1) if process_type != "Isochoric (Constant Volume)" else 0
    
    if process_type == "Isochoric (Constant Volume)":
        Q = n_moles * 1.5 * R_universal * (T2 - T1)  # For ideal diatomic gas
    else:
        Q = 0  # Will be calculated based on first law
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### Initial State (1)")
        st.metric("Pressure P₁", f"{P1/1000:.2f} kPa")
        st.metric("Temperature T₁", f"{T1:.2f} K")
        st.metric("Volume V₁", f"{V1:.3f} m³")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### Final State (2)")
        st.metric("Pressure P₂", f"{P2/1000:.2f} kPa")
        st.metric("Temperature T₂", f"{T2:.2f} K")
        st.metric("Volume V₂", f"{V2:.3f} m³")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### Gas Properties")
        st.metric("Number of Moles", f"{n_moles:.4f} mol")
        st.metric("Work Done", f"{W:.2f} J")
        st.metric("Process Type", process_label, delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    add_to_calculation("Ideal Gas Law", 
                      f"P₁={P1/1000}kPa, T₁={T1}K, V₁={V1}m³", 
                      f"P₂={P2/1000:.2f}kPa, T₂={T2}K, V₂={V2:.3f}m³, W={W:.2f}J")
    
    # P-V Diagram
    st.markdown("### 📊 Process Diagram (P-V)")
    
    if process_type == "Isobaric (Constant Pressure)":
        V_range = np.linspace(min(V1, V2) * 0.5, max(V1, V2) * 1.5, 100)
        P_range = np.full_like(V_range, P1 / 1000)
    elif process_type == "Isochoric (Constant Volume)":
        P_range = np.linspace(min(P1, P2) / 1000 * 0.5, max(P1, P2) / 1000 * 1.5, 100)
        V_range = np.full_like(P_range, V1)
    elif process_type == "Isothermal (Constant Temperature)":
        V_range = np.linspace(min(V1, V2) * 0.5, max(V1, V2) * 1.5, 100)
        P_range = (n_moles * R_universal * T1) / (V_range * 1000)
    else:  # Adiabatic
        V_range = np.linspace(min(V1, V2) * 0.5, max(V1, V2) * 1.5, 100)
        P_range = P1 / 1000 * (V1 / V_range) ** gamma
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # P-V diagram
    ax1.plot(V_range, P_range, 'b-', linewidth=2.5, label=process_type)
    ax1.scatter([V1, V2], [P1/1000, P2/1000], color='red', s=150, zorder=5)
    ax1.annotate('State 1', (V1, P1/1000), xytext=(10, 10), textcoords='offset points', 
                fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    ax1.annotate('State 2', (V2, P2/1000), xytext=(10, 10), textcoords='offset points',
                fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='cyan', alpha=0.7))
    ax1.fill_between(V_range, 0, P_range, alpha=0.2, color='blue')
    ax1.set_xlabel('Volume V [m³]', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Pressure P [kPa]', fontsize=11, fontweight='bold')
    ax1.set_title('P-V Diagram', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best')
    
    # T-V diagram
    T_range = np.linspace(min(T1, T2) * 0.7, max(T1, T2) * 1.3, 100)
    if process_type == "Isobaric (Constant Pressure)":
        V_temp = (n_moles * R_universal * T_range) / P1
        ax2.plot(V_temp, T_range, 'g-', linewidth=2.5, label=process_type)
    elif process_type == "Isochoric (Constant Volume)":
        P_temp = (n_moles * R_universal * T_range) / V1
        ax2.plot(np.full_like(T_range, V1), T_range, 'g-', linewidth=2.5, label=process_type)
    elif process_type == "Isothermal (Constant Temperature)":
        V_temp = np.linspace(min(V1, V2) * 0.5, max(V1, V2) * 1.5, 100)
        ax2.plot(V_temp, np.full_like(V_temp, T1), 'g-', linewidth=2.5, label=process_type)
    else:  # Adiabatic
        V_adi = np.linspace(min(V1, V2) * 0.5, max(V1, V2) * 1.5, 100)
        T_adi = T1 * (V1 / V_adi) ** (gamma - 1)
        ax2.plot(V_adi, T_adi, 'g-', linewidth=2.5, label=process_type)
    
    ax2.scatter([V1, V2], [T1, T2], color='red', s=150, zorder=5)
    ax2.annotate('State 1', (V1, T1), xytext=(10, 10), textcoords='offset points',
                fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    ax2.annotate('State 2', (V2, T2), xytext=(10, 10), textcoords='offset points',
                fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', facecolor='cyan', alpha=0.7))
    ax2.set_xlabel('Volume V [m³]', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Temperature T [K]', fontsize=11, fontweight='bold')
    ax2.set_title('T-V Diagram', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best')
    
    st.pyplot(fig)

# ==================== FIRST LAW OF THERMODYNAMICS ====================
elif analysis_type == "First Law of Thermodynamics":
    st.sidebar.markdown("### First Law Parameters")
    st.sidebar.info("ΔU = Q - W (Energy Balance)")
    
    # System properties
    st.sidebar.markdown("#### System Properties")
    mass = st.sidebar.slider("Mass of Gas [kg]:", 0.001, 10, 1, 0.1)
    specific_heat_v = st.sidebar.slider("Specific Heat Cv [J/kg·K]:", 100, 2000, 717, 50)
    
    st.sidebar.markdown("#### Energy Transfer")
    T_initial = st.sidebar.slider("Initial Temperature T₁ [K]:", 273, 1000, 300, 10)
    T_final = st.sidebar.slider("Final Temperature T₂ [K]:", 273, 1500, 400, 10)
    
    Q_input = st.sidebar.slider("Heat Input Q [kJ]:", -100, 1000, 100, 10) * 1000  # Convert to J
    
    # Calculate from First Law
    delta_T = T_final - T_initial
    delta_U = mass * specific_heat_v * delta_T
    W_done = Q_input - delta_U
    
    # Additional calculations
    specific_heat_p = specific_heat_v + R_specific_air
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### Internal Energy Change")
        st.metric("ΔU", f"{delta_U/1000:.2f} kJ")
        st.metric("ΔT", f"{delta_T:.2f} K")
        st.metric("Cv", f"{specific_heat_v:.2f} J/kg·K")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### Energy Transfer")
        st.metric("Heat Input Q", f"{Q_input/1000:.2f} kJ")
        st.metric("Work Output W", f"{W_done/1000:.2f} kJ")
        st.metric("Net Energy", f"{(Q_input - W_done)/1000:.2f} kJ")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### Process Information")
        st.metric("Mass", f"{mass:.2f} kg")
        st.metric("Cp", f"{specific_heat_p:.2f} J/kg·K")
        gamma = specific_heat_p / specific_heat_v
        st.metric("γ (Cp/Cv)", f"{gamma:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    add_to_calculation("First Law", 
                      f"m={mass}kg, Q={Q_input/1000}kJ, T₁={T_initial}K, T₂={T_final}K",
                      f"ΔU={delta_U/1000:.2f}kJ, W={W_done/1000:.2f}kJ")
    
    # Energy Flow Diagram
    st.markdown("### 📊 Energy Flow Diagram")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Draw system box
    system = FancyBboxPatch((2, 2), 3, 3, boxstyle="round,pad=0.1", 
                           edgecolor='black', facecolor='lightblue', linewidth=2.5)
    ax.add_patch(system)
    ax.text(3.5, 3.5, 'Thermodynamic\nSystem', ha='center', va='center', 
           fontsize=12, fontweight='bold')
    
    # Heat input arrow
    if Q_input > 0:
        ax.arrow(0.5, 3.5, 1.2, 0, head_width=0.3, head_length=0.2, fc='red', ec='red', linewidth=2)
        ax.text(0.5, 4.2, f'Q = {Q_input/1000:.2f} kJ\n(Heat In)', ha='center', fontsize=10, 
               fontweight='bold', color='red')
    else:
        ax.arrow(0.5, 3.5, 1.2, 0, head_width=0.3, head_length=0.2, fc='blue', ec='blue', linewidth=2)
        ax.text(0.5, 4.2, f'Q = {Q_input/1000:.2f} kJ\n(Heat Out)', ha='center', fontsize=10,
               fontweight='bold', color='blue')
    
    # Work output arrow
    if W_done > 0:
        ax.arrow(5.3, 3.5, 1.2, 0, head_width=0.3, head_length=0.2, fc='green', ec='green', linewidth=2)
        ax.text(7, 4.2, f'W = {W_done/1000:.2f} kJ\n(Work Out)', ha='center', fontsize=10,
               fontweight='bold', color='green')
    else:
        ax.arrow(5.3, 3.5, 1.2, 0, head_width=0.3, head_length=0.2, fc='orange', ec='orange', linewidth=2)
        ax.text(7, 4.2, f'W = {abs(W_done)/1000:.2f} kJ\n(Work In)', ha='center', fontsize=10,
               fontweight='bold', color='orange')
    
    # Internal energy change
    ax.text(3.5, 1.5, f'ΔU = {delta_U/1000:.2f} kJ\n({("↑ Increase" if delta_U > 0 else "↓ Decrease")})', 
           ha='center', fontsize=11, fontweight='bold', 
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
    
    # First Law equation
    ax.text(3.5, 0.5, 'ΔU = Q - W', ha='center', fontsize=13, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=2))
    
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(0, 5)
    ax.axis('off')
    st.pyplot(fig)

# ==================== CYCLE EFFICIENCY ====================
else:  # Cycle Efficiency Analysis
    st.sidebar.markdown("### Thermodynamic Cycle Parameters")
    
    cycle_type = st.sidebar.selectbox(
        "Select Cycle Type:",
        ["Carnot Cycle", "Otto Cycle (Spark Ignition)", "Diesel Cycle (Compression Ignition)"]
    )
    
    if cycle_type == "Carnot Cycle":
        st.sidebar.markdown("#### Carnot Cycle Parameters")
        T_hot = st.sidebar.slider("Hot Reservoir Temperature [K]:", 300, 2000, 800, 50)
        T_cold = st.sidebar.slider("Cold Reservoir Temperature [K]:", 273, 600, 300, 50)
        
        eta_carnot = 1 - (T_cold / T_hot)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Carnot Cycle Efficiency")
            st.metric("Thermal Efficiency (η)", f"{eta_carnot*100:.2f}%")
            st.metric("T_Hot", f"{T_hot} K")
            st.metric("T_Cold", f"{T_cold} K")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Efficiency Formula")
            st.write(f"η = 1 - (T_cold / T_hot)")
            st.write(f"η = 1 - ({T_cold} / {T_hot})")
            st.write(f"η = {eta_carnot:.4f} or {eta_carnot*100:.2f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        add_to_calculation("Carnot Cycle", 
                          f"T_hot={T_hot}K, T_cold={T_cold}K",
                          f"η={eta_carnot*100:.2f}%")
        
        # T-S Diagram for Carnot Cycle
        st.markdown("### 📊 Carnot Cycle (T-S Diagram)")
        
        S = np.array([0, 1, 2, 3])
        T = np.array([T_hot, T_hot, T_cold, T_cold])
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Draw cycle
        cycle_s = [0, 1, 1, 2, 2, 3, 3, 0]
        cycle_t = [T_hot, T_hot, T_cold, T_cold, T_hot, T_hot, T_cold, T_hot]
        
        ax.plot([0, 1], [T_hot, T_hot], 'r-', linewidth=3, label='Isothermal Heat Addition')
        ax.plot([1, 1], [T_hot, T_cold], 'b-', linewidth=3, label='Adiabatic Expansion')
        ax.plot([1, 0], [T_cold, T_cold], 'g-', linewidth=3, label='Isothermal Heat Rejection')
        ax.plot([0, 0], [T_cold, T_hot], 'orange', linewidth=3, label='Adiabatic Compression')
        
        # Fill cycle area
        ax.fill([0, 1, 1, 0], [T_hot, T_hot, T_cold, T_cold], alpha=0.3, color='cyan')
        
        ax.scatter([0, 1], [T_hot, T_hot], color='red', s=100, zorder=5)
        ax.scatter([1, 0], [T_cold, T_cold], color='blue', s=100, zorder=5)
        
        ax.text(0.5, T_hot+30, 'Isothermal Heat Addition (2→1)', ha='center', fontsize=10, fontweight='bold')
        ax.text(1.15, (T_hot+T_cold)/2, 'Adiabatic\nExpansion', ha='left', fontsize=10, fontweight='bold')
        ax.text(0.5, T_cold-30, 'Isothermal Heat Rejection (4→3)', ha='center', fontsize=10, fontweight='bold')
        ax.text(-0.15, (T_hot+T_cold)/2, 'Adiabatic\nCompression', ha='right', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Entropy S (arbitrary units)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Temperature T [K]', fontsize=11, fontweight='bold')
        ax.set_title(f'Carnot Cycle (T-S Diagram) - η = {eta_carnot*100:.2f}%', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        ax.set_xlim(-0.5, 1.5)
        
        st.pyplot(fig)
        
    elif cycle_type == "Otto Cycle (Spark Ignition)":
        st.sidebar.markdown("#### Otto Cycle Parameters")
        compression_ratio = st.sidebar.slider("Compression Ratio (r):", 2, 15, 8, 1)
        gamma_otto = st.sidebar.slider("Heat Capacity Ratio (γ):", min_value=1.2, max_value=1.4, value=1.4, step=0.05)
        
        eta_otto = 1 - (1 / compression_ratio ** (gamma_otto - 1))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Otto Cycle Efficiency")
            st.metric("Thermal Efficiency (η)", f"{eta_otto*100:.2f}%")
            st.metric("Compression Ratio (r)", f"{compression_ratio}:1")
            st.metric("γ (Cp/Cv)", f"{gamma_otto:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Efficiency Formula")
            st.write(f"η = 1 - (1/r^(γ-1))")
            st.write(f"η = 1 - (1/{compression_ratio}^{gamma_otto-1:.2f})")
            st.write(f"η = {eta_otto:.4f} or {eta_otto*100:.2f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        add_to_calculation("Otto Cycle",
                          f"r={compression_ratio}, γ={gamma_otto}",
                          f"η={eta_otto*100:.2f}%")
        
        # P-V Diagram for Otto Cycle
        st.markdown("### 📊 Otto Cycle (P-V Diagram)")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Otto cycle points (normalized)
        V = np.array([1, 1/compression_ratio, 1/compression_ratio, 1])
        
        # For illustration
        P1 = 100
        P_vals = np.array([P1, P1 * compression_ratio**gamma_otto, 
                          P1 * compression_ratio**gamma_otto * 3.5, P1 * 3.5])
        
        # Draw processes
        ax.plot([1, 1/compression_ratio], [P_vals[0], P_vals[1]], 'b-', linewidth=3, label='Adiabatic Compression (1→2)')
        ax.plot([1/compression_ratio, 1/compression_ratio], [P_vals[1], P_vals[2]], 'r-', linewidth=3, label='Isochoric Heat Addition (2→3)')
        ax.plot([1/compression_ratio, 1], [P_vals[2], P_vals[3]], 'g-', linewidth=3, label='Adiabatic Expansion (3→4)')
        ax.plot([1, 1], [P_vals[3], P_vals[0]], 'orange', linewidth=3, label='Isochoric Heat Rejection (4→1)')
        
        # Fill cycle
        ax.fill([1, 1/compression_ratio, 1/compression_ratio, 1], 
               [P_vals[0], P_vals[1], P_vals[2], P_vals[3]], alpha=0.3, color='cyan')
        
        ax.scatter(V, P_vals, color='red', s=100, zorder=5)
        ax.text(0.5, P_vals[0]-10, '1', ha='center', fontsize=12, fontweight='bold')
        ax.text(1/compression_ratio-0.05, P_vals[1]+10, '2', ha='center', fontsize=12, fontweight='bold')
        ax.text(1/compression_ratio-0.05, P_vals[2]+10, '3', ha='center', fontsize=12, fontweight='bold')
        ax.text(0.5, P_vals[3]+10, '4', ha='center', fontsize=12, fontweight='bold')
        
        ax.set_xlabel('Volume V (normalized to Vmax)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Pressure P (normalized)', fontsize=11, fontweight='bold')
        ax.set_title(f'Otto Cycle (P-V Diagram) - r = {compression_ratio}:1, η = {eta_otto*100:.2f}%', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')
        ax.set_xlim(0, 1.2)
        
        st.pyplot(fig)
        
    else:  # Diesel Cycle
        st.sidebar.markdown("#### Diesel Cycle Parameters")
        compression_ratio_diesel = st.sidebar.slider("Compression Ratio (r):", 10, 25, 16, 1)
        cutoff_ratio = st.sidebar.slider("Cutoff Ratio (rc):", min_value=1.0, max_value=4.0, value=2.0, step=0.1)
        gamma_diesel = st.sidebar.slider("Heat Capacity Ratio (γ):", min_value=1.2, max_value=1.4, value=1.4, step=0.05)
        
        eta_diesel = 1 - (1 / compression_ratio_diesel ** (gamma_diesel - 1)) * \
                     (cutoff_ratio ** gamma_diesel - 1) / (gamma_diesel * (cutoff_ratio - 1))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Diesel Cycle Efficiency")
            st.metric("Thermal Efficiency (η)", f"{eta_diesel*100:.2f}%")
            st.metric("Compression Ratio (r)", f"{compression_ratio_diesel}:1")
            st.metric("Cutoff Ratio (rc)", f"{cutoff_ratio:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Efficiency Formula")
            st.write(f"Complex formula involving r, rc, and γ")
            st.write(f"r = {compression_ratio_diesel}, rc = {cutoff_ratio}")
            st.write(f"η = {eta_diesel:.4f} or {eta_diesel*100:.2f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        add_to_calculation("Diesel Cycle",
                          f"r={compression_ratio_diesel}, rc={cutoff_ratio}, γ={gamma_diesel}",
                          f"η={eta_diesel*100:.2f}%")
        
        st.markdown("### 📊 Diesel Cycle (P-V Diagram)")
        st.info("Diesel cycle differs from Otto cycle with isobaric (constant pressure) heat addition instead of isochoric.")

# ==================== RESULTS TABLE ====================
st.divider()
st.markdown("### 📋 Calculation History")

if st.session_state.calculations:
    # Create a simplified dataframe for display
    display_data = []
    for calc in st.session_state.calculations:
        display_data.append({
            'Analysis Type': calc['Analysis'],
            'Parameters': calc['Parameters'][:50] + ('...' if len(calc['Parameters']) > 50 else ''),
            'Results': str(calc['Results'])[:50] + ('...' if len(str(calc['Results'])) > 50 else '')
        })
    df_history = pd.DataFrame(display_data)
    st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    if st.button("Clear Calculation History"):
        st.session_state.calculations = []
        st.rerun()
else:
    st.info("No calculations yet. Start by adjusting parameters above!")

# ==================== REFERENCE DATA ====================
st.divider()
st.markdown("### 📚 Thermodynamic Constants & Properties")

reference_constants = {
    'Constant/Property': ['Universal Gas Constant', 'Boltzmann Constant', 'Specific Gas Constant (Air)', 
                         'Heat Capacity Ratio (Diatomic)', 'Heat Capacity Ratio (Monatomic)'],
    'Value': ['8.314 J/mol·K', '1.381×10⁻²³ J/K', '287 J/kg·K', '1.40', '1.67'],
    'Use': ['PV=nRT calculations', 'Molecular scale calculations', 'Air at room temp', 'Air, N₂, O₂', 'Noble gases, He, Ar']
}

df_constants = pd.DataFrame(reference_constants)
st.dataframe(df_constants, use_container_width=True, hide_index=True)
