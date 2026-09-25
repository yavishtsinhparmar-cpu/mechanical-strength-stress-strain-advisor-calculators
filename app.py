import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mechanical Metal Strength Calculator",
    page_icon="⚙️",
    layout="wide"
)

# =========================================================
# TEAM DETAILS
# CHANGE THESE DETAILS
# =========================================================

GROUP_NUMBER = "Group No. 01"

MEMBERS = [
    "Member 1 - Your Name - Enrollment No.",
    "Member 2 - Member Name - Enrollment No.",
    "Member 3 - Member Name - Enrollment No."
]

# =========================================================
# MATERIAL DATABASE
# Strength values are in MPa
# Young's modulus is in MPa
# =========================================================

materials = {
    "Mild Steel": {
        "yield": 250,
        "ultimate": 400,
        "E": 200000
    },

    "Aluminium": {
        "yield": 276,
        "ultimate": 310,
        "E": 69000
    },

    "Cast Iron": {
        "yield": 130,
        "ultimate": 200,
        "E": 100000
    },

    "Stainless Steel": {
        "yield": 215,
        "ultimate": 505,
        "E": 193000
    },

    "Copper": {
        "yield": 70,
        "ultimate": 220,
        "E": 110000
    }
}

# =========================================================
# TITLE
# =========================================================

st.title("⚙️ Mechanical Metal Strength Calculator")

st.subheader(
    "Stress • Strain • Elongation • Factor of Safety"
)

st.write(
    "An interactive mechanical engineering calculator "
    "developed using Python and Streamlit."
)

# =========================================================
# TEAM DETAILS
# =========================================================

with st.expander("👥 Team Details"):

    st.write(f"**{GROUP_NUMBER}**")

    for member in MEMBERS:
        st.write(member)

st.divider()

# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.header("🔧 Input Parameters")

# Material selection
material = st.sidebar.selectbox(
    "Select Material",
    list(materials.keys())
)

# Load type
load_type = st.sidebar.radio(
    "Load Type",
    ["Tensile", "Compressive"]
)

# Applied load
load = st.sidebar.number_input(
    "Applied Load (kN)",
    min_value=0.1,
    max_value=1000.0,
    value=10.0,
    step=1.0
)

# Cross-section selection
cross_section = st.sidebar.selectbox(
    "Cross-Section",
    ["Circular", "Rectangular"]
)

# =========================================================
# CROSS-SECTION CALCULATION
# =========================================================

if cross_section == "Circular":

    diameter = st.sidebar.number_input(
        "Diameter (mm)",
        min_value=0.1,
        max_value=1000.0,
        value=20.0,
        step=1.0
    )

    area = np.pi * diameter ** 2 / 4

    dimension_text = (
        f"Diameter = {diameter:.2f} mm"
    )

else:

    width = st.sidebar.number_input(
        "Width (mm)",
        min_value=0.1,
        max_value=1000.0,
        value=20.0,
        step=1.0
    )

    thickness = st.sidebar.number_input(
        "Thickness (mm)",
        min_value=0.1,
        max_value=1000.0,
        value=10.0,
        step=1.0
    )

    area = width * thickness

    dimension_text = (
        f"Width = {width:.2f} mm, "
        f"Thickness = {thickness:.2f} mm"
    )

# Original length
length = st.sidebar.number_input(
    "Original Length (mm)",
    min_value=0.1,
    max_value=10000.0,
    value=100.0,
    step=10.0
)

# =========================================================
# MATERIAL PROPERTIES
# =========================================================

yield_strength = materials[material]["yield"]
ultimate_strength = materials[material]["ultimate"]
young_modulus = materials[material]["E"]

# =========================================================
# ENGINEERING CALCULATIONS
# =========================================================

# Convert kN to N
load_N = load * 1000

# Stress
stress = load_N / area

# Strain
strain = stress / young_modulus

# Elongation
elongation = strain * length

# Factor of Safety
fos_yield = yield_strength / stress
fos_ultimate = ultimate_strength / stress

# =========================================================
# MAIN RESULTS
# =========================================================

st.header("📊 Calculation Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Area",
        f"{area:.2f} mm²"
    )

with col2:
    st.metric(
        "Stress",
        f"{stress:.2f} MPa"
    )

with col3:
    st.metric(
        "Strain",
        f"{strain:.6f}"
    )

with col4:
    st.metric(
        "Elongation",
        f"{elongation:.4f} mm"
    )

st.divider()

# =========================================================
# FACTOR OF SAFETY
# =========================================================

st.header("🛡️ Factor of Safety")

col5, col6 = st.columns(2)

with col5:
    st.metric(
        "FOS against Yield",
        f"{fos_yield:.2f}"
    )

with col6:
    st.metric(
        "FOS against Ultimate",
        f"{fos_ultimate:.2f}"
    )

# =========================================================
# SAFE / FAIL
# =========================================================

st.header("🚦 Safety Status")

if stress <= yield_strength:

    st.success(
        f"✅ SAFE\n\n"
        f"Applied stress = {stress:.2f} MPa\n\n"
        f"Yield strength = {yield_strength} MPa"
    )

else:

    st.error(
        f"❌ FAIL\n\n"
        f"Applied stress = {stress:.2f} MPa\n\n"
        f"Yield strength = {yield_strength} MPa"
    )

# =========================================================
# MATERIAL INFORMATION
# =========================================================

st.header("🔩 Material Properties")

info1, info2, info3 = st.columns(3)

with info1:
    st.info(
        f"Material\n\n**{material}**"
    )

with info2:
    st.info(
        f"Yield Strength\n\n**{yield_strength} MPa**"
    )

with info3:
    st.info(
        f"Young's Modulus\n\n**{young_modulus:,} MPa**"
    )

st.write(
    f"**Ultimate Strength:** "
    f"{ultimate_strength} MPa"
)

st.write(
    f"**Load Type:** {load_type}"
)

st.write(
    f"**Cross-Section:** {dimension_text}"
)

# =========================================================
# STRESS VS LOAD GRAPH
# =========================================================

st.header("📈 Stress vs Applied Load")

# Generate load values
load_range = np.linspace(
    0,
    max(load * 1.5, 1),
    100
)

# Convert kN to N
load_range_N = load_range * 1000

# Calculate stress for each load
stress_range = load_range_N / area

# Create graph
fig, ax = plt.subplots(
    figsize=(9, 5)
)

ax.plot(
    load_range,
    stress_range,
    linewidth=2,
    label="Stress"
)

# Yield strength line
ax.axhline(
    y=yield_strength,
    linestyle="--",
    linewidth=2,
    label="Yield Strength"
)

# Current operating point
ax.scatter(
    [load],
    [stress],
    s=80,
    label="Operating Point"
)

# Graph labels
ax.set_xlabel(
    "Applied Load (kN)"
)

ax.set_ylabel(
    "Stress (MPa)"
)

ax.set_title(
    "Stress vs Applied Load"
)

ax.grid(True)

ax.legend()

st.pyplot(fig)

# =========================================================
# ENGINEERING FORMULAS
# =========================================================

st.header("📐 Engineering Formulas")

st.subheader("1. Stress")

st.latex(
    r"\sigma = \frac{P}{A}"
)

st.write(
    "σ = Stress (MPa), "
    "P = Applied Load (N), "
    "A = Cross-sectional Area (mm²)"
)

st.subheader("2. Strain")

st.latex(
    r"\epsilon = \frac{\sigma}{E}"
)

st.write(
    "ε = Strain, "
    "σ = Stress (MPa), "
    "E = Young's Modulus (MPa)"
)

st.subheader("3. Elongation")

st.latex(
    r"\Delta L = \epsilon L"
)

st.write(
    "ΔL = Elongation (mm), "
    "ε = Strain, "
    "L = Original Length (mm)"
)

st.subheader("4. Factor of Safety")

st.latex(
    r"FOS = \frac{\text{Strength}}{\text{Applied Stress}}"
)

# =========================================================
# ENGINEERING CONCLUSION
# =========================================================

st.header("📝 Engineering Conclusion")

if stress <= yield_strength:

    st.write(
        f"For the selected **{material}**, the calculated "
        f"stress is **{stress:.2f} MPa**, which is below "
        f"the yield strength of **{yield_strength} MPa**."
    )

    st.write(
        "Therefore, the selected loading condition is "
        "within the yield-strength limit."
    )

else:

    st.write(
        f"For the selected **{material}**, the calculated "
        f"stress is **{stress:.2f} MPa**, which exceeds "
        f"the yield strength of **{yield_strength} MPa**."
    )

    st.write(
        "Therefore, the selected loading condition exceeds "
        "the yield-strength limit."
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Python Mini Project | Diploma in Mechanical Engineering | "
    "Semester 3 | Python + Streamlit"
)