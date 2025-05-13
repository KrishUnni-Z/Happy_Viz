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
metrics = ["Rank", "Log GDP per capita", "Social support", "Healthy life expectancy",
             "Freedom to make life choices", "Generosity", "Perceptions of corruption"]

# ---------- TABS ----------
tabs = st.tabs([
    "📋 How is Happiness Measured?",
    "🗺️ Global Happiness Map",
    "🔍 Country Trends & Correlation Explorer",
    "📌 Conclusions"
])

with tabs[0]:
    with stylable_container("story-intro", css_styles="padding: 1rem; background-color:#f0f4f8; border-radius:8px"):
        st.header("📋 How is Happiness Measured?")
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

# ---------- TAB 1 (ENHANCED) ----------
with tabs[1]:
    with stylable_container("map", css_styles="padding: 1rem; background-color:#eef6ff; border-radius:8px"):
        selected_year = st.selectbox("📅 Select Year", years, index=len(years)-1)
        map_metric = st.selectbox("📈 Choose a Happiness Indicator", metrics)
        filtered_df = df[df["Year"] == selected_year]

        regions = {
            "All": countries,
            "Asia": ["India", "Thailand", "Japan", "Singapore"],
            "Europe": ["Finland", "Spain", "Germany", "France", "Italy"],
            "Americas": ["United States", "Canada", "Brazil", "Argentina"],
            "Oceania": ["Australia", "New Zealand"]
        }
        selected_region = st.selectbox("🌎 Filter Region", list(regions.keys()), index=0)
        region_countries = regions[selected_region]
        region_df = filtered_df[filtered_df["Country"].isin(region_countries)] if selected_region != "All" else filtered_df

        st.subheader("🗺️ Happiness Around the World")
        fig_map = px.choropleth(
            region_df,
            locations="Country",
            locationmode="country names",
            color=map_metric,
            hover_name="Country",
            hover_data=["Country", "Rank"] if "Rank" in region_df.columns else ["Country"],
            color_continuous_scale="Turbo",
            height=500
        )
        fig_map.update_geos(showocean=True, oceancolor="LightBlue", landcolor="white")
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)

        st.caption("⚪ White areas indicate countries with no available data.")

        if st.checkbox("🔍 Highlight countries above global average"):
            avg_val = round(region_df[map_metric].mean(), 2)
            above_avg = region_df[region_df[map_metric] > avg_val]
            st.success(f"🌟 {len(above_avg)} countries scored above the global average ({avg_val}) for '{map_metric}'")
            st.dataframe(above_avg[["Country", map_metric]].sort_values(by=map_metric, ascending=False), use_container_width=True)

# ---------- TAB 2 (ENHANCED) ----------
with tabs[2]:
    with stylable_container("global", css_styles="padding: 1rem; background-color:#fefefe; border-radius:8px"):
        st.header("📈 Animated Trends Across Years")

        trend_metric = st.selectbox("📊 Choose Metric", metrics, key="trend_metric")
        selected_countries = st.multiselect("🌍 Choose Countries", countries, default=["Australia", "Finland", "India"])

        if selected_countries:
            animated_df = df[df["Country"].isin(selected_countries)]
            fig_line = px.line(
                animated_df, x="Year", y=trend_metric, color="Country", markers=True,
                animation_frame="Year", range_y=[animated_df[trend_metric].min(), animated_df[trend_metric].max()]
            )
            st.plotly_chart(fig_line, use_container_width=True)

    with stylable_container("correlation", css_styles="padding: 1rem; background-color:#fff8f2; border-radius:8px"):
        st.header("🧭 Explore Correlations")

        year_corr = st.selectbox("📅 Select Year", years, index=len(years)-1)
        x_metric = st.selectbox("X-Axis", metrics, index=0)
        y_metric = st.selectbox("Y-Axis", metrics, index=1)

        corr_df = df[df["Year"] == year_corr]
        if selected_countries:
            corr_df = corr_df[corr_df["Country"].isin(selected_countries)]

        fig_corr = px.scatter(
            corr_df, x=x_metric, y=y_metric,
            size='Ladder Score', color='Country',
            hover_name='Country'
        )
        st.plotly_chart(fig_corr, use_container_width=True)

        clicked_country = st.selectbox("🔎 View Specific Country", ["None"] + selected_countries)
        if clicked_country != "None":
            st.write(df[df["Country"] == clicked_country][["Year", x_metric, y_metric, "Ladder Score"]])

with tabs[3]:
    with stylable_container("Conclusions", css_styles="padding: 1rem; background-color:#f0f4f8; border-radius:8px"):
        st.header("📌 Conclusions")
        st.write("Tobefilled.")
