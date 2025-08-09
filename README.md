## Greening the Digital Age: A Simulation-Driven Framework for Indoor Plant Integration and ISO-Aligned Synthetic Carbon Credit Valuation within Digital Workspaces

---

## 📄 Developer README – Dual Scenario Carbon Simulation Tool (Colab Version)

### 🧑‍💻 Author

**Muhammad Saddam Khokhar**

### 📜 Description

This Google Colab tool simulates **carbon sequestration** from indoor plants and **offset ratios** for digital device emissions using a Monte Carlo model.
It runs **two scenarios automatically**:

* **Scenario 1**: Uses parameters set by the user in the sliders.
* **Scenario 2**: Parameters are slightly randomized from Scenario 1 to simulate a different real-world configuration.

The tool:

* Generates **results tables** for each scenario
* Creates a **comparison table** (median values side-by-side)
* Saves and downloads a **research paper–style PDF** with plots and discussion
* Automatically runs in **Google Colab** with an interactive GUI

---

### 🚀 How to Run in Google Colab

1. **Open Google Colab**
   Go to [https://colab.research.google.com/](https://colab.research.google.com/)

2. **Create a New Notebook**

   * File → New Notebook
   * (Optional) Rename to `carbon_simulation.ipynb`

3. **Paste the Full Code**
   Copy the provided Python code into the first cell of the notebook.

4. **Run the First Cell**

   * The code will install dependencies (`ipywidgets`, `reportlab`, `pandas`, `matplotlib`) automatically.
   * Ignore any warnings; they won’t affect the tool.

5. **Use the GUI Sliders**
   After the code runs, you’ll see an interactive form with sliders:

   * **Trials** → Number of Monte Carlo runs (e.g., 1000)
   * **Area m²** → Workspace size
   * **Devices** → Number of digital devices in use
   * **Plants** → Number of indoor plants
   * **LAI / Light** → Leaf area index and light interception values
   * **R mean & sigma** → Photosynthetic rate parameters
   * **Seed** → Random seed for reproducibility

6. **Click “Run Tool”**

   * The tool runs **Scenario 1** and **Scenario 2**
   * Plots and summary tables are generated
   * PDF report is built

7. **Download the PDF**

   * Once ready, the `simulation_report.pdf` will auto-download
   * The PDF includes:

     * Title, author, abstract, intro, methodology
     * Scenario 1 and 2 results tables
     * Comparison table
     * Plots for both scenarios
     * Discussion & conclusion

---

### 📂 Output Files

* `simulation_report.pdf` – Full formatted research-style report
* `plot_sequestration_1.png` – Sequestration histogram for Scenario 1
* `plot_offset_1.png` – Offset ratio histogram for Scenario 1
* `plot_sequestration_2.png` – Sequestration histogram for Scenario 2
* `plot_offset_2.png` – Offset ratio histogram for Scenario 2

---

### 🛠 Notes for Developers

* If the PDF does not auto-download, you can manually run:

  ```python
  from google.colab import files
  files.download("simulation_report.pdf")
  ```
* You can modify the **random variation** in Scenario 2 by editing:

  ```python
  random.uniform(0.8, 1.2)  # 20% variation
  ```
* To change text in the PDF (abstract, intro, discussion), edit the variables:

  * `ABSTRACT`
  * `README_TEXT`
  * `METHODOLOGY_TEXT`
  * `DISCUSSION_TEXT`

---
