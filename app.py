import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="World Happiness Explorer", page_icon="😊")

st.title("🌍 World Happiness Explorer")


# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("happinessreport.csv")
    df.rename(columns={
        "Country name": "Country",
        "Ladder score": "Ladder Score",
        "Explained by: Log GDP per capita": "Log GDP per capita",
        "Explained by: Social support": "Social support",
        "Explained by: Healthy life expectancy": "Healthy life expectancy",
        "Explained by: Freedom to make life choices": "Freedom to make life choices",
        "Explained by: Generosity": "Generosity",
        "Explained by: Perceptions of corruption": "Perceptions of corruption",
        "Dystopia + residual": "Dystopia + residual"
    }, inplace=True)
    return df

df = load_data()
countries = df["Country"].unique().tolist()
years = int(sorted(df["Year"].unique()))

# ---------- TABS ----------
tabs = st.tabs([
    "📌 How is Happiness Measured?",
    "🗺️ Map View",
    "📊 Compare Countries",
    "🌐 Global Avg Context",
    "testing"
])

with tabs[0]:
    with stylable_container("story-intro", css_styles="padding: 1rem; background-color:#f0f4f8; border-radius:8px"):
        st.header("📌 How is Happiness Measured?")
        st.write("The **Ladder Score** represents life evaluation by respondents, influenced by GDP per capita, social support, life expectancy, freedom, generosity, and perceived corruption.")

with tabs[1]:
    with stylable_container("map", css_styles="padding: 1rem; background-color:#eef6ff; border-radius:8px"):
        selected_year = st.slider("Select Year", min(years), max(years), value=max(years))
        map_metric = st.selectbox("Metric to show on map", ["Ladder Score", "Log GDP per capita"])
        filtered_df = df[df["Year"] == selected_year]

        st.subheader("🗺️ Global Happiness Map")
        fig_map = px.choropleth(
            filtered_df,
            locations="Country",
            locationmode="country names",
            color=map_metric,
            hover_name="Country",
            animation_frame="Year",
            hover_data={
        "RANK": True,
        "Rank change YOY": True
    },
            color_continuous_scale="Turbo"
        )
        fig_map.update_geos(
            showocean=True, oceancolor="LightBlue", landcolor="white", projection_type="natural earth"
        )
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)

with tabs[2]:
    with stylable_container("comparison", css_styles="padding: 1rem; background-color:#fff8f2; border-radius:8px"):
        st.header("📊 Compare Countries Over Time")
        country_options = ["All Countries"] + countries
        selected_countries = st.multiselect("Countries", country_options, default=["Finland", "India"])

        if "All Countries" in selected_countries:
            comp_df = df.copy()
        else:
            comp_df = df[df["Country"].isin(selected_countries)]

        compare_metric = st.selectbox("Compare Metric", df.columns[3:-1], key="compare_metric")
        fig_line = px.line(comp_df, x="Year", y=compare_metric, color="Country", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

        st.header("📈 Metric Correlation")
        year_corr = st.selectbox("Select Year", years, index=len(years)-1, key="year_corr")
        x_metric = st.selectbox("X Axis", df.columns[3:-1], index=0, key="x_metric")
        y_metric = st.selectbox("Y Axis", df.columns[3:-1], index=1, key="y_metric")
        corr_df = df[df["Year"] == year_corr]

        if "All Countries" not in selected_countries:
            corr_df = corr_df[corr_df["Country"].isin(selected_countries)]

        fig_corr = px.scatter(corr_df, x=x_metric, y=y_metric, size='Ladder Score', color='Country')
        st.plotly_chart(fig_corr, use_container_width=True)


with tabs[3]:
    with stylable_container("global", css_styles="padding: 1rem; background-color:#fefefe; border-radius:8px"):
        st.header("🌐 Global Average vs Specific Country")
        selected_countries = st.multiselect("Select Countries", countries, default=["Finland", "India"], key="global_countries")
        compare_metric = st.selectbox("Compare Metric", df.columns[3:-1], index=0, key="global_metric")

        filtered_countries_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
        global_avg = filtered_df[compare_metric].mean()

        st.metric(f"Global Avg {compare_metric}", f"{round(global_avg, 2)}")
        fig_global = px.bar(
            filtered_countries_df,
            x='Country',
            y=compare_metric,
            color='Country',
            title=f"{compare_metric} vs Global Average"
        )
        fig_global.add_hline(
            y=global_avg,
            line_dash="dot",
            annotation_text="Global Avg",
            line_color="red"
        )
        st.plotly_chart(fig_global, use_container_width=True)

with tabs[4]:
    with stylable_container("map", css_styles="padding: 1rem; background-color:#eef6ff; border-radius:8px"):
        st.subheader("🗺️ Global Happiness Map")

        map_metric = st.selectbox("Metric to show on map", ["Ladder Score", "Log GDP per capita"])
        df = df[df["Year"].notna()]
        df["Year"] = df["Year"].astype(int)

        fig_map = px.choropleth(
            df,
            locations="Country",
            locationmode="country names",
            color=map_metric,
            hover_name="Country",
            animation_frame="Year",
            hover_data={
                "Country": True,
                "Ladder Score": True,
                "Log GDP per capita": True
            },
            color_continuous_scale="Turbo"
        )
        fig_map.update_geos(
            showocean=True, oceancolor="LightBlue", landcolor="white", projection_type="natural earth"
        )
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 1000, "redraw": True}, "fromcurrent": True}],
                        "label": "▶️ Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                        "label": "⏸️ Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }]
        )
        st.plotly_chart(fig_map, use_container_width=True)
