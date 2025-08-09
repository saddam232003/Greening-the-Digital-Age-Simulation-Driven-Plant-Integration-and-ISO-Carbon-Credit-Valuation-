# FINAL Dual Scenario Simulation Tool - Research Paper Style PDF
# Author: Muhammad Saddam Khokhar

!pip install ipywidgets reportlab pandas matplotlib --quiet
from ipywidgets import interact_manual, FloatSlider, IntSlider
import random, csv, math, statistics, pandas as pd
import matplotlib.pyplot as plt
from google.colab import files
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from IPython.display import display, clear_output
import os

# Paper metadata
PAPER_TITLE = "Greening the Digital Age: Leveraging Indoor Plants and Green Architecture for Carbon Credits to Offset Computational Carbon Emissions"
AUTHOR = "Muhammad Saddam Khokhar"
ABSTRACT = """This research investigates the integration of indoor plants and green architectural elements to mitigate the carbon emissions 
produced by computational activities. Using a Monte Carlo simulation model, the study estimates carbon sequestration potential, 
synthetic carbon credit generation, and offset ratios for varying workspace and plant configurations. The results demonstrate 
that strategic indoor greenery can significantly reduce the carbon footprint of digital work environments, creating a viable 
pathway for carbon credit markets and sustainable computing practices."""
README_TEXT = """This simulation tool models carbon sequestration potential from indoor plants and green architectural setups in workspaces 
to offset emissions from digital devices. The user specifies workspace parameters, plant and device counts, and biological factors 
such as leaf area index and light interception. The tool runs a Monte Carlo simulation to estimate carbon capture, offset ratios, 
and synthetic carbon credits, outputting CSV data, PNG plots, and a formatted PDF report."""
METHODOLOGY_TEXT = """We implemented a Monte Carlo simulation with adjustable parameters for workspace size, plant density, 
device emissions, and biological performance factors. Each trial simulates daily plant CO₂ uptake based on leaf area index, 
light interception, and a lognormal photosynthetic rate. Device emissions are drawn from a Gaussian distribution. 
Offset ratios and carbon credits are computed using random performance factors and uncertainty rates."""
DISCUSSION_TEXT = """The simulation results suggest that indoor plants can contribute meaningfully to offsetting emissions from 
digital devices, especially in large workspaces with optimized plant species and layout. While the offset ratio rarely reaches 100%, 
the contribution is significant enough to justify integration into sustainable building designs. Synthetic carbon credits derived from 
verified plant-based sequestration could support green financing for digital infrastructure. Future work could incorporate species-specific 
growth curves, real-time IoT-based monitoring, and integration with blockchain carbon markets."""

# Simulation function
def run_simulation(trials, area_m2, device_mean_kg, device_std_kg,
                   device_count, plant_count, lai_min, lai_max,
                   light_min, light_max, r_mu_gm2day, r_sigma, seed):
    if seed is not None:
        random.seed(seed)
    sequestration_tonnes, offset_ratio, credit_yield = [], [], []
    for _ in range(trials):
        devs = [random.gauss(device_mean_kg, device_std_kg) for _ in range(device_count)]
        Etotal_tonnes = sum(devs) / 1000.0
        annual_tonnes_plants = 0.0
        for _p in range(plant_count):
            lai = random.uniform(lai_min, lai_max)
            light = random.uniform(light_min, light_max)
            R = random.lognormvariate(math.log(r_mu_gm2day), r_sigma)
            area_per_plant = area_m2 / plant_count
            daily_g = R * lai * light * area_per_plant
            annual_tonnes_plants += daily_g * 365.0 * 1e-6
        sequestration_tonnes.append(annual_tonnes_plants)
        Pf = random.uniform(0.75, 0.90)
        Ur = random.uniform(0.03, 0.09)
        credit_yield.append(annual_tonnes_plants * Pf * (1 - Ur))
        offset_ratio.append(annual_tonnes_plants / (Etotal_tonnes + 1e-12))
    return sequestration_tonnes, offset_ratio, credit_yield

# PDF generator with comparison
def generate_pdf(results1, results2, trials, params1, params2):
    seq1, off1, cred1 = results1
    seq2, off2, cred2 = results2
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate("simulation_report.pdf", pagesize=A4)
    elements = []

    # Title
    elements.append(Paragraph(PAPER_TITLE, styles["Title"]))
    elements.append(Paragraph(f"Author: {AUTHOR}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Abstract
    elements.append(Paragraph("Abstract", styles["Heading2"]))
    elements.append(Paragraph(ABSTRACT, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Intro
    elements.append(Paragraph("Introduction / ReadMe", styles["Heading2"]))
    elements.append(Paragraph(README_TEXT, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Methodology
    elements.append(Paragraph("Methodology", styles["Heading2"]))
    elements.append(Paragraph(METHODOLOGY_TEXT, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Scenario 1 table
    elements.append(Paragraph("Scenario 1 Results", styles["Heading2"]))
    data1 = [
        ["Metric", "Median", "Mean", "Std Dev", "Min", "Max"],
        ["Sequestration (tCO₂/yr)", f"{statistics.median(seq1):.3f}", f"{statistics.mean(seq1):.3f}", f"{statistics.pstdev(seq1):.3f}", f"{min(seq1):.3f}", f"{max(seq1):.3f}"],
        ["Offset Ratio", f"{statistics.median(off1):.3f}", f"{statistics.mean(off1):.3f}", f"{statistics.pstdev(off1):.3f}", f"{min(off1):.3f}", f"{max(off1):.3f}"],
        ["Synthetic Credit (tCO₂e)", f"{statistics.median(cred1):.3f}", f"{statistics.mean(cred1):.3f}", f"{statistics.pstdev(cred1):.3f}", f"{min(cred1):.3f}", f"{max(cred1):.3f}"]
    ]
    table1 = Table(data1, hAlign="LEFT")
    table1.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.lightgrey),("GRID", (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(table1)
    elements.append(Spacer(1, 12))

    # Scenario 2 table
    elements.append(Paragraph("Scenario 2 Results", styles["Heading2"]))
    data2 = [
        ["Metric", "Median", "Mean", "Std Dev", "Min", "Max"],
        ["Sequestration (tCO₂/yr)", f"{statistics.median(seq2):.3f}", f"{statistics.mean(seq2):.3f}", f"{statistics.pstdev(seq2):.3f}", f"{min(seq2):.3f}", f"{max(seq2):.3f}"],
        ["Offset Ratio", f"{statistics.median(off2):.3f}", f"{statistics.mean(off2):.3f}", f"{statistics.pstdev(off2):.3f}", f"{min(off2):.3f}", f"{max(off2):.3f}"],
        ["Synthetic Credit (tCO₂e)", f"{statistics.median(cred2):.3f}", f"{statistics.mean(cred2):.3f}", f"{statistics.pstdev(cred2):.3f}", f"{min(cred2):.3f}", f"{max(cred2):.3f}"]
    ]
    table2 = Table(data2, hAlign="LEFT")
    table2.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.lightgrey),("GRID", (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(table2)
    elements.append(Spacer(1, 12))

    # Comparison table
    elements.append(Paragraph("Scenario Comparison (Median Values)", styles["Heading2"]))
    comparison = [
        ["Metric", "Scenario 1", "Scenario 2"],
        ["Sequestration (tCO₂/yr)", f"{statistics.median(seq1):.3f}", f"{statistics.median(seq2):.3f}"],
        ["Offset Ratio", f"{statistics.median(off1):.3f}", f"{statistics.median(off2):.3f}"],
        ["Sequestration (tCO\u2082/yr)", f"{statistics.median(cred1):.3f}", f"{statistics.median(cred2):.3f}"]
    ]
    table_cmp = Table(comparison, hAlign="LEFT")
    table_cmp.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.lightgrey),("GRID", (0,0), (-1,-1), 0.5, colors.grey)]))
    elements.append(table_cmp)
    elements.append(Spacer(1, 12))

    # Plots
    elements.append(Paragraph("Scenario 1 Plots", styles["Heading3"]))
    elements.append(RLImage("plot_sequestration_1.png", width=400, height=250))
    elements.append(RLImage("plot_offset_1.png", width=400, height=250))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Scenario 2 Plots", styles["Heading3"]))
    elements.append(RLImage("plot_sequestration_2.png", width=400, height=250))
    elements.append(RLImage("plot_offset_2.png", width=400, height=250))
    elements.append(Spacer(1, 12))

    # Discussion
    elements.append(Paragraph("Discussion & Conclusion", styles["Heading2"]))
    elements.append(Paragraph(DISCUSSION_TEXT, styles["Normal"]))

    doc.build(elements)

# Main tool
def run_tool(trials, area_m2, device_mean_kg, device_std_kg, device_count,
             plant_count, lai_min, lai_max, light_min, light_max, r_mu_gm2day, r_sigma, seed):

    clear_output(wait=True)
    print(f"📄 {PAPER_TITLE}\n👤 Author: {AUTHOR}\n\n📜 Abstract:\n{ABSTRACT}\n")

    # Scenario 1
    results1 = run_simulation(trials, area_m2, device_mean_kg, device_std_kg,
                              device_count, plant_count, lai_min, lai_max,
                              light_min, light_max, r_mu_gm2day, r_sigma, seed)

    # Scenario 2 random variation
    params2 = {
        "area_m2": max(5, area_m2 * random.uniform(0.8, 1.2)),
        "device_count": max(1, int(device_count * random.uniform(0.7, 1.3))),
        "plant_count": max(1, int(plant_count * random.uniform(0.7, 1.3))),
        "lai_min": lai_min * random.uniform(0.9, 1.1),
        "lai_max": lai_max * random.uniform(0.9, 1.1),
        "light_min": light_min * random.uniform(0.9, 1.1),
        "light_max": light_max * random.uniform(0.9, 1.1),
        "r_mu_gm2day": r_mu_gm2day * random.uniform(0.9, 1.1),
        "r_sigma": r_sigma * random.uniform(0.9, 1.1)
    }

    results2 = run_simulation(trials, params2["area_m2"], device_mean_kg, device_std_kg,
                              params2["device_count"], params2["plant_count"], params2["lai_min"], params2["lai_max"],
                              params2["light_min"], params2["light_max"], params2["r_mu_gm2day"], params2["r_sigma"], seed+1)

    # Plots for both scenarios
    plt.figure(figsize=(7,4))
    plt.hist(results1[0], bins=20, color="green", alpha=0.7)
    plt.title("Scenario 1 - Annual CO₂ Sequestration")
    plt.savefig("plot_sequestration_1.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7,4))
    plt.hist(results1[1], bins=20, color="blue", alpha=0.7)
    plt.title("Scenario 1 - Offset Ratio")
    plt.savefig("plot_offset_1.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7,4))
    plt.hist(results2[0], bins=20, color="green", alpha=0.7)
    plt.title("Scenario 2 - Annual CO₂ Sequestration")
    plt.savefig("plot_sequestration_2.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7,4))
    plt.hist(results2[1], bins=20, color="blue", alpha=0.7)
    plt.title("Scenario 2 - Offset Ratio")
    plt.savefig("plot_offset_2.png", dpi=150)
    plt.close()

    # PDF
    generate_pdf(results1, results2, trials, None, None)

    # Ensure download
    if os.path.exists("simulation_report.pdf"):
        files.download("simulation_report.pdf")
    else:
        print("❌ PDF generation failed.")

# GUI
interact_manual(
    run_tool,
    trials=IntSlider(value=1000, min=100, max=5000, step=100, description="Trials"),
    area_m2=FloatSlider(value=100.0, min=10, max=500, step=10, description="Area m²"),
    device_mean_kg=FloatSlider(value=2.0, min=0.5, max=5.0, step=0.1, description="Dev mean kg"),
    device_std_kg=FloatSlider(value=0.2, min=0.05, max=1.0, step=0.05, description="Dev std kg"),
    device_count=IntSlider(value=10, min=1, max=50, step=1, description="Devices"),
    plant_count=IntSlider(value=12, min=1, max=100, step=1, description="Plants"),
    lai_min=FloatSlider(value=3.5, min=1.0, max=6.0, step=0.1, description="LAI min"),
    lai_max=FloatSlider(value=4.5, min=1.0, max=6.0, step=0.1, description="LAI max"),
    light_min=FloatSlider(value=0.6, min=0.1, max=1.0, step=0.05, description="Light min"),
    light_max=FloatSlider(value=0.8, min=0.1, max=1.0, step=0.05, description="Light max"),
    r_mu_gm2day=FloatSlider(value=2.0, min=0.5, max=5.0, step=0.1, description="R mean"),
    r_sigma=FloatSlider(value=0.4, min=0.1, max=1.0, step=0.05, description="R sigma"),
    seed=IntSlider(value=42, min=0, max=9999, step=1, description="Seed")
)
