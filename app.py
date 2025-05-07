import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

# Dummy Data Creation
countries = ['Finland', 'India', 'Brazil', 'Norway', 'Japan', 'USA']
years = list(range(2019, 2024))
data = []

for country in countries:
    for year in years:
        gdp = np.round(np.random.uniform(0.8, 1.6), 2)
        social_support = np.round(np.random.uniform(0.6, 1.0), 2)
        life_expectancy = np.round(np.random.uniform(0.7, 1.0), 2)
        freedom = np.round(np.random.uniform(0.4, 0.9), 2)
        generosity = np.round(np.random.uniform(0.1, 0.4), 2)
        corruption = np.round(np.random.uniform(0.1, 0.5), 2)
        ladder_score = gdp + social_support + life_expectancy + freedom + generosity + (1 - corruption)
        rank = int(200 - ladder_score * 20)
        data.append({
            'Year': year,
            'Country': country,
            'Ladder Score': np.round(ladder_score, 2),
            'Rank': rank,
            'Log GDP per capita': gdp,
            'Social support': social_support,
            'Healthy life expectancy': life_expectancy,
            'Freedom to make life choices': freedom,
            'Generosity': generosity,
            'Perceptions of corruption': corruption
        })

df = pd.DataFrame(data)

# Streamlit UI Setup
st.set_page_config(layout="wide")
st.title("🌍 World Happiness Explorer (Dummy Data)")

# Tabs for visual story
tabs = st.tabs([
    "📌 How is Happiness Measured?",
    "🗺️ Map View",
    "📊 Compare Countries",
    "🏆 Top vs Bottom",
    "🌐 Global Avg Context"
])

with tabs[0]:
    with stylable_container("story-intro", css_styles="padding: 1rem; background-color:#f0f4f8; border-radius:8px"):
        st.header("📌 How is Happiness Measured?")
        st.write("The **Ladder Score** represents life evaluation by respondents, influenced by GDP per capita, social support, life expectancy, freedom, generosity, and perceived corruption.")

with tabs[1]:
    with stylable_container("map", css_styles="padding: 1rem; background-color:#eef6ff; border-radius:8px"):
          # Inputs
          selected_year = st.slider("Select Year", min(years), max(years), value=2021)
          map_metric = st.selectbox("Metric to show on map", ['Ladder Score', 'Log GDP per capita'])
        
          filtered_df = df[df['Year'] == selected_year]
          st.subheader("🗺️ Global Happiness Map")
          st.markdown(f"**Happiness Ranking - {selected_year}**")

          fig_map = px.choropleth(
            filtered_df,
            locations="Country",
            locationmode="country names",
            color=map_metric,
            hover_name="Country",
            color_continuous_scale="Turbo"
          )
          fig_map.update_geos(
            showocean=True,
            oceancolor="LightBlue",
            landcolor="white",
            projection_type="natural earth"
          )
          fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
          st.plotly_chart(fig_map, use_container_width=True)

with tabs[2]:
    with stylable_container("comparison", css_styles="padding: 1rem; background-color:#fff8f2; border-radius:8px"):
        st.header("📊 Compare Countries Over Time")
        selected_countries = st.multiselect("Countries", countries, default=["Finland", "India"])
        compare_metric = st.selectbox("Compare Metric", df.columns[3:-1])
        comp_df = df[df["Country"].isin(selected_countries)]
        fig_line = px.line(comp_df, x="Year", y=compare_metric, color="Country", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
        st.header("📈 Metric Correlation")
        x_metric = st.selectbox("X Axis", df.columns[3:-1], index=0)
        y_metric = st.selectbox("Y Axis", df.columns[3:-1], index=1)
        fig_corr = px.scatter(filtered_df, x=x_metric, y=y_metric, size='Ladder Score', color='Country')
        st.plotly_chart(fig_corr, use_container_width=True)

with tabs[3]:
    with stylable_container("top-bottom", css_styles="padding: 1rem; background-color:#fef3f7; border-radius:8px"):
        st.header("🏆 Top vs Bottom 5 in Happiness Rank")
        top5 = filtered_df.nsmallest(5, 'Rank')
        bottom5 = filtered_df.nlargest(5, 'Rank')
        fig_bar = px.bar(pd.concat([top5, bottom5]), x='Country', y='Ladder Score', color='Rank')
        st.plotly_chart(fig_bar, use_container_width=True)

with tabs[4]:
    with stylable_container("global", css_styles="padding: 1rem; background-color:#fefefe; border-radius:8px"):
        st.header("🌐 Global Average vs Specific Country")
        selected_countries = st.multiselect("Countries", countries, default=["Finland", "India"])
        compare_metric = st.selectbox("Compare Metric", df.columns[3:-1])
        global_avg = filtered_df[compare_metric].mean()
        st.metric("🌎 Global Avg "+compare_metric , f"{round(global_avg,2)}")
        fig_global = px.bar(filtered_df, x='Country', y='Ladder Score', color='Country')
        fig_global.add_hline(y=global_avg, line_dash="dot", annotation_text="Global Avg", line_color="red")
        st.plotly_chart(fig_global, use_container_width=True)
