# Sprint4: Vehicle Data Dashboard

This project provides an exploratory data analysis and interactive dashboard for the US vehicles advertisement dataset (`vehicles_us.csv`).

The Jupyter notebook in `notebooks/EDA.ipynb` performs initial exploration and visualizations using Pandas and Plotly Express.  
The Streamlit application in `app.py` allows users to interactively explore the dataset, view histograms, scatter plots, and apply filters.

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

# Repo Url: github.com/aurascoper/Sprint4.git

# Render Url: https://sprint4-s6ej.onrender.com/
