import streamlit as st
import io
import pandas as pd
import plotly.express as px

st.header("Vehicle Dataset Dashboard")

# Load the dataset
df = pd.read_csv("vehicles_us.csv")

if st.checkbox("Show raw data"):
    st.subheader("Raw Dataset")
    st.dataframe(df)

st.subheader("Dataset Info")
buf = io.StringIO()
df.info(buf=buf)
s = buf.getvalue()
st.text(s)

st.subheader("Price Distribution Histogram")
price_hist = px.histogram(df, x="price", nbins=50, title="Distribution of Vehicle Prices")
st.plotly_chart(price_hist)

st.subheader("Year Distribution Histogram")
year_hist = px.histogram(df, x="model_year", nbins=30, title="Distribution of Vehicle Model Years")
st.plotly_chart(year_hist)

# Scatter plot: Price vs Mileage with filter
filter_newer = st.checkbox("Filter: Vehicles from 2015 onwards")
if filter_newer:
    df_filtered = df[df["model_year"] >= 2015]
else:
    df_filtered = df

st.subheader("Price vs. Mileage Scatter Plot")
scatter_pm = px.scatter(
    df_filtered,
    x="odometer",
    y="price",
    color="model_year",
    title="Price vs Mileage Scatter",
    hover_data=["model", "fuel"]
)
st.plotly_chart(scatter_pm)
