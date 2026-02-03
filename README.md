# Sprint4: Vehicle Data Dashboard

This project provides an exploratory data analysis and interactive dashboard for the US vehicles advertisement dataset (`vehicles_us.csv`).

The Jupyter notebook in `notebooks/EDA.ipynb` performs initial exploration and visualizations using Pandas and Plotly Express.  
The Streamlit application in `app.py` provides an interactive dashboard with four main sections to explore the vehicle dataset: Data viewer, Vehicle types by manufacturer, Histogram of `condition` vs `model_year`, and Compare price distribution between manufacturers.  
  
## App Features
- **Section 1 — Data viewer**
  - Checkbox: _Include manufacturers with less than 1000 ads_ (default **checked**)
  - Displays a table of the filtered dataset
- **Section 2 — Vehicle types by manufacturer**
  - Stacked bar chart showing counts of vehicle `type` for each `manufacturer`
- **Section 3 — Histogram of `condition` vs `model_year`**
  - Histogram of `model_year` colored by `condition`
- **Section 4 — Compare price distribution between manufacturers**
  - Selectboxes: _Select manufacturer 1_ and _Select manufacturer 2_ (defaults: **chevrolet**, **bmw**)
  - Checkbox: _Normalize histogram_ (default **checked**)
  - Overlayed histogram of `price` distributions with optional normalization to percent

- **Section 5 — Interactive scatterplot**
  - Interactive scatter plot to explore relationships between numeric variables.
  - Controls within an expandable "Scatterplot settings" panel:
    - Axis selectors for X and Y from numeric columns (`price`, `odometer`, `model_year`, `cylinders`, `days_listed`), preventing same-axis selection.
    - Color grouping by categorical columns (`condition`, `type`, `fuel`, `transmission`, `paint_color`, `is_4wd`, `manufacturer`).
    - Slider to limit "Max points to plot" for performance, with downsampling if needed.
    - Checkbox to "Clip outliers" (1st–99th percentile).
    - Checkboxes for log scaling on X and Y axes (applied only if all values are positive).
    - Checkbox to show a regression line, computed with SciPy, with slope, intercept, R-value, R-squared, and p-value displayed.
  - The plot supports rich Plotly interactions: hover tooltips, zoom, pan, box select, and lasso select.

## Setup and Installation

1. Ensure you have Python 3.8+ installed.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```
3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

5. Open your browser and navigate to the address shown in the terminal (e.g., `http://localhost:8501`).

## Project Structure

- `vehicles_us.csv`: Original dataset of US vehicle advertisements.  
- `notebooks/EDA.ipynb`: Exploratory Data Analysis notebook using Plotly Express.  
- `app.py`: Streamlit application code.  
- `requirements.txt`: Project dependencies with minimum version specifications to support a range of Python environments.  
- `.streamlit/config.toml`: Streamlit configuration for deployment (headless mode, port settings).  

Repo Url: github.com/aurascoper/Sprint4.git

Render Url: https://sprint4-s6ej.onrender.com/
