import streamlit as st
import os
import pandas as pd
import plotly.express as px
from scipy.stats import linregress
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "vehicles_us.csv"))
    df["manufacturer"] = df["model"].astype(str).str.split().str[0].str.lower()
    for col in ["price", "model_year", "cylinders", "odometer", "days_listed"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    return df
# Helper functions for scatterplot
def prepare_scatter_df(df, x_col, y_col, clip_outliers, max_points):
    df2 = df.dropna(subset=[x_col, y_col]).copy()
    if clip_outliers:
        x_low, x_high = df2[x_col].quantile(0.01), df2[x_col].quantile(0.99)
        y_low, y_high = df2[y_col].quantile(0.01), df2[y_col].quantile(0.99)
        df2 = df2[
            (df2[x_col] >= x_low) & (df2[x_col] <= x_high) &
            (df2[y_col] >= y_low) & (df2[y_col] <= y_high)
        ]
    if len(df2) > max_points:
        df2 = df2.sample(max_points, random_state=42)
    return df2

def add_regression_line(fig, x_vals, y_vals):
    if len(x_vals) < 2:
        return fig, None
    res = linregress(x_vals, y_vals)
    x_min, x_max = x_vals.min(), x_vals.max()
    y_min = res.slope * x_min + res.intercept
    y_max = res.slope * x_max + res.intercept
    fig.add_trace(
        go.Scatter(
            x=[x_min, x_max],
            y=[y_min, y_max],
            mode="lines",
            name="Regression line",
        )
    )
    metrics = {
        "slope": res.slope,
        "intercept": res.intercept,
        "r_value": res.rvalue,
        "p_value": res.pvalue,
    }
    return fig, metrics

def main():
    st.title("Vehicle Dataset Dashboard")

    df = load_data()

    # Section 1 — Data viewer
    st.header("Data viewer")
    include_less = st.checkbox(
        "Include manufacturers with less than 1000 ads", value=True
    )
    if include_less:
        filtered_df = df.copy()
    else:
        counts = df["manufacturer"].value_counts()
        keep = counts[counts >= 1000].index
        filtered_df = df[df["manufacturer"].isin(keep)]
    st.dataframe(filtered_df)
    if filtered_df.empty:
        st.write("No data matches the current selection.")
        return

    # Fill categorical missing values
    filtered_df["type"] = filtered_df["type"].fillna("unknown")
    filtered_df["condition"] = filtered_df["condition"].fillna("unknown")

    # Section 2 — Vehicle types by manufacturer
    st.header("Vehicle types by manufacturer")
    fig2 = px.bar(
        filtered_df,
        x="manufacturer",
        color="type",
        barmode="stack",
    )
    fig2.update_layout(xaxis={"categoryorder": "category ascending"})
    st.plotly_chart(fig2, use_container_width=True)

    # Section 3 — Histogram of `condition` vs `model_year`
    st.header("Histogram of `condition` vs `model_year`")
    df3 = filtered_df.dropna(subset=["model_year"])
    fig3 = px.histogram(
        df3,
        x="model_year",
        color="condition",
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Section 4 — Compare price distribution between manufacturers
    st.header("Compare price distribution between manufacturers")
    manufacturers = sorted(filtered_df["manufacturer"].unique())
    default1 = "chevrolet" if "chevrolet" in manufacturers else manufacturers[0]
    default2 = (
        "bmw"
        if "bmw" in manufacturers
        else (manufacturers[1] if len(manufacturers) > 1 else manufacturers[0])
    )
    m1 = st.selectbox("Select manufacturer 1", manufacturers, index=manufacturers.index(default1))
    m2 = st.selectbox("Select manufacturer 2", manufacturers, index=manufacturers.index(default2))
    normalize = st.checkbox("Normalize histogram", value=True)

    df4 = filtered_df.dropna(subset=["price"])
    df4 = df4[df4["manufacturer"].isin([m1, m2])]
    if df4.empty:
        st.write("No data matches the current selection.")
        return

    histnorm = "percent" if normalize else None
    fig4 = px.histogram(
        df4,
        x="price",
        color="manufacturer",
        barmode="overlay",
        opacity=0.7,
        histnorm=histnorm,
    )
    yaxis_title = "Percent" if normalize else "Count"
    fig4.update_layout(yaxis_title=yaxis_title)
    st.plotly_chart(fig4, use_container_width=True)
    # Section 5 — Interactive scatterplot
    st.header("Interactive scatterplot")
    st.write("Interact with the plot: hover, zoom, pan, box select, lasso select using the Plotly toolbar.")

    with st.expander("Scatterplot settings", expanded=True):
        numeric_cols = ["price", "odometer", "model_year", "cylinders", "days_listed"]
        categorical_cols = ["condition", "type", "fuel", "transmission", "paint_color", "is_4wd", "manufacturer"]

        # Axis selectors
        x_axis = st.selectbox("X-axis", numeric_cols, index=numeric_cols.index("odometer"))
        y_options = [col for col in numeric_cols if col != x_axis]
        default_y = "price" if x_axis != "price" else y_options[0]
        y_axis = st.selectbox("Y-axis", y_options, index=y_options.index(default_y))

        # Color grouping
        color_by = st.selectbox("Color by", categorical_cols, index=categorical_cols.index("condition"))

        # Point density / performance
        max_points = st.slider("Max points to plot", min_value=1000, max_value=50000, value=20000, step=1000)

        # Outlier handling
        clip_outliers = st.checkbox("Clip outliers (1st–99th percentile)", value=True)

        # Axis transforms
        log_x = st.checkbox("Log scale X", value=False)
        log_y = st.checkbox("Log scale Y", value=False)

        # Regression line
        show_regression = st.checkbox("Show regression line", value=True)

    # Prepare scatter data
    scatter_df = prepare_scatter_df(filtered_df, x_axis, y_axis, clip_outliers, max_points)

    # Fill/convert categorical columns
    for col in ["condition", "type", "fuel", "transmission", "paint_color", "manufacturer"]:
        if col in scatter_df.columns:
            scatter_df[col] = scatter_df[col].fillna("unknown").astype(str)
    # Map is_4wd values
    def map_4wd(val):
        if pd.isna(val):
            return "unknown"
        try:
            if float(val) == 1.0:
                return "4wd"
            elif float(val) == 0.0:
                return "not_4wd"
        except:
            pass
        return "unknown"
    scatter_df["is_4wd"] = scatter_df["is_4wd"].apply(map_4wd)

    if scatter_df.empty:
        st.write("No data available for the scatterplot with the current settings.")
    else:
        # Plot scatter
        fig5 = px.scatter(
            scatter_df,
            x=x_axis,
            y=y_axis,
            color=color_by,
            hover_name="model",
            hover_data=[
                "manufacturer", "model", "model_year", "price", "odometer",
                "condition", "type", "fuel", "transmission", "cylinders",
                "is_4wd", "days_listed", "date_posted"
            ],
            opacity=0.6,
        )

        # Handle log scales
        if log_x and (scatter_df[x_axis] <= 0).any():
            st.warning("Cannot apply log scale to X-axis with non-positive values; using linear scale.")
            log_x = False
        if log_y and (scatter_df[y_axis] <= 0).any():
            st.warning("Cannot apply log scale to Y-axis with non-positive values; using linear scale.")
            log_y = False
        if log_x:
            fig5.update_xaxes(type="log")
        if log_y:
            fig5.update_yaxes(type="log")

        st.plotly_chart(fig5, use_container_width=True)

        # Regression line and metrics
        if show_regression:
            fig5, metrics = add_regression_line(fig5, scatter_df[x_axis], scatter_df[y_axis])
            if metrics:
                slope = metrics["slope"]
                intercept = metrics["intercept"]
                r_val = metrics["r_value"]
                p_val = metrics["p_value"]
                st.caption(
                    f"Slope: {slope:.4f}, Intercept: {intercept:.4f}, R-value: {r_val:.4f}, R-squared: {r_val**2:.4f}, P-value: {p_val:.4g}"
                )
            else:
                st.warning("Not enough points to perform regression (need at least 2).")

if __name__ == "__main__":
    main()
