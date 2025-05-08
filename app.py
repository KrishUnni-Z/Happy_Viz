import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="World Happiness Explorer", page_icon="😊")

st.title("🌍 World Happiness Explorer")

def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://www.loopnews.com/wp-content/uploads/2024/03/istock-happy-sad_a278859f233bb569042db30cffe4f8ab-4.jpg");
            background-size: cover;
            background-attachment: fixed;
            position: relative;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(255, 255, 255, 0.8);  /* Light overlay with alpha */
            z-index: 0;
        }}

        /* Push content above overlay */
        [data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("happinessreport_cleaned.csv")
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
    df['Year'] = df['Year'].astype(int)
    return df

df = load_data()
countries = df["Country"].unique().tolist()
years = sorted(df["Year"].dropna().astype(int).unique())
metrics = ["Ladder Score", "Log GDP per capita", "Social support", "Healthy life expectancy",
             "Freedom to make life choices", "Generosity", "Perceptions of corruption", "Dystopia + residual"]

# ---------- TABS ----------
tabs = st.tabs([
    "📌 How is Happiness Measured?",
    "🗺️ Map View",
    "🌐 Country Comparisons",
    "📊 Conclusions"
])

with tabs[0]:
    with stylable_container("story-intro", css_styles="padding: 1rem; background-color:#f0f4f8; border-radius:8px"):
        st.header("📌 How is Happiness Measured?")
        st.markdown("""
        The **World Happiness Report** collects data from respondents in over **160 countries and territories**, covering more than **98% of the world’s adult population**.

        The **happiness scores** (`ladder`) are central values with upper and lower bounds, calculated from several key factors:
        """)

        st.subheader("📊 Key Factors in Happiness Scores")

        st.markdown("""
        - **GDP per capita**: Indicates purchasing power parity (PPP) at constant 2021 international dollar prices (from *World Development Indicators*).
        - **Social support**: Based on responses to the question:  
          *“If you were in trouble, do you have relatives or friends you can count on to help you whenever you need them, or not?”*
        - **Healthy life expectancy**: Data extracted from the **World Health Organization (WHO)** Global Health Observatory.
        - **Freedom to make life choices**: Based on responses to:  
          *“Are you satisfied or dissatisfied with your freedom to choose what you do with your life?”*
        - **Generosity**: Calculated as the residual from regressing national averages of the question:  
          *“Have you donated money to a charity in the past month?”* on GDP per capita.
        - **Perceptions of corruption**: National average of responses to two questions:  
          1. *“Is corruption widespread throughout the government or not?”*  
          2. *“Is corruption widespread within businesses or not?”*
        - **Dystopia and residual**: Capture the baseline and unexplained variations in national happiness levels.
        """)

        st.subheader("📚 Source")

        st.markdown("""
        - [The World Happiness Report](https://worldhappiness.report/data-sharing/)
        """)

with tabs[1]:
    with stylable_container("map", css_styles="padding: 1rem; background-color:#eef6ff; border-radius:8px"):
        selected_year = st.selectbox("Select Year", years, index=len(years) - 1, key="selected_year")
        map_metric = st.selectbox("Metric to show on map", metrics)
        filtered_df = df[df["Year"] == selected_year]

        # Hover details
        hover_cols = ["Country"]
        for col in ["Rank", "Position Changes YOY"]:
            if col in filtered_df.columns:
                hover_cols.append(col)

        st.subheader("🗺️ Global Happiness Map")
        fig_map = px.choropleth(
            filtered_df,
            locations="Country",
            locationmode="country names",
            color=map_metric,
            hover_name="Country",
            hover_data=hover_cols,
            color_continuous_scale="Turbo"
        )
        fig_map.update_geos(
            showocean=True, oceancolor="LightBlue", landcolor="white", projection_type="natural earth"
        )
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
    # Add footnote
    st.caption("⚪ Countries shown in white have no data available for the selected year.")

with tabs[2]:
    with stylable_container("global", css_styles="padding: 1rem; background-color:#fefefe; border-radius:8px"):
        st.header("🌐 Global Average vs Specific Country")
        selected_countries = st.multiselect("Select Countries", countries, default=["Australia", "Finland", "United States", "Singapore", "Spain", "India", "Thailand", "Japan"], key="global_countries")
        compare_metric = st.selectbox("Compare Metric", metrics, index=0, key="global_metric")

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

    with stylable_container("comparison", css_styles="padding: 1rem; background-color:#fff8f2; border-radius:8px"):
        st.header("📊 Compare Countries Over Time")
        country_options = ["All Countries"] + countries
        selected_countries = st.multiselect("Countries", country_options, default=["Australia", "Finland", "United States", "Singapore", "Spain", "India", "Thailand", "Japan"])

        if "All Countries" in selected_countries:
            comp_df = df.copy()
        else:
            comp_df = df[df["Country"].isin(selected_countries)]

        compare_metric = st.selectbox("Compare Metric", metrics, key="compare_metric")
        fig_line = px.line(comp_df, x="Year", y=compare_metric, color="Country", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

        st.header("📈 Metric Correlation")
        year_corr = st.selectbox("Select Year", years, index=len(years)-1, key="year_corr")
        x_metric = st.selectbox("X Axis", df.columns[3:-1], index=df.columns[3:-1].tolist().index("Log GDP per capita")
            , key="x_metric")
        y_metric = st.selectbox("Y Axis", df.columns[3:-1], index=df.columns[3:-1].tolist().index("Ladder Score")
            , key="y_metric")
        corr_df = df[df["Year"] == year_corr]

        if "All Countries" not in selected_countries:
            corr_df = corr_df[corr_df["Country"].isin(selected_countries)]

        fig_corr = px.scatter(corr_df, x=x_metric, y=y_metric, size='Ladder Score', color='Country')
        st.plotly_chart(fig_corr, use_container_width=True)

with tabs[3]:
    with stylable_container("Conclusions", css_styles="padding: 1rem; background-color:#f0f4f8; border-radius:8px"):
        st.header("📌 Conclusions")
        st.write("Tobefilled.")