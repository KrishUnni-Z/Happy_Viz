import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="World Happiness Explorer", page_icon="😊")

st.title("🌍 World Happiness Explorer")
st.markdown("**From Data to Joy: Insights from Data Across Nations**")
st.caption("Connecting metrics to meaning in the pursuit of global well-being")

# ---------- FORCE LIGHT MODE FULL OVERRIDE ----------
st.markdown("""
<style>
html, body, .stApp, [data-testid="stAppViewContainer"], .block-container {
    color-scheme: light !important;
    background-color: white !important;
    color: #1a1a1a !important;
}

body {
    background-color: white !important;
}

header, footer, .css-18ni7ap.e8zbici2 {
    background-color: white !important;
    color: #1a1a1a !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- BACKGROUND ----------
def set_background():
    st.markdown("""
    <style>
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        color-scheme: light !important;
        background: white;
    }

    .stApp {
        background-image: url("https://www.loopnews.com/wp-content/uploads/2024/03/istock-happy-sad_a278859f233bb569042db30cffe4f8ab-4.jpg");
        background-size: cover;
        background-attachment: scroll;
        background-position: center top;
        background-repeat: no-repeat;
    }

    .block-container {
        background-color: rgba(255, 255, 255, 0.88);  /* white with some transparency */
        padding: 2rem 1rem;
        border-radius: 0;
    }

    [data-testid="stAppViewContainer"] {
        height: auto;
        overflow: auto;
    }
    </style>
    """, unsafe_allow_html=True)


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
    df = df[df["Year"] % 1 == 0]
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()
countries = sorted(df["Country"].unique().tolist())
years = sorted(df["Year"].unique())
metrics = ["Rank", "Log GDP per capita", "Social support", "Healthy life expectancy",
           "Freedom to make life choices", "Generosity", "Perceptions of corruption"]

tabs = st.tabs([
    "📋 How Is Happiness Measured?",
    "🗺️ Global Happiness Map",
    "🔍 Country Trends & Correlation Explorer",
    "📌 Conclusions"
])

with tabs[0]:
    st.header("📋 How Is Happiness Measured?")
    st.markdown("""
The **World Happiness Report 2025** brings together responses from people in over **140 countries and regions**, capturing how individuals rate their current lives.

To measure happiness, participants are asked to imagine a ladder with steps numbered from 0 to 10. The top of the ladder represents the best possible life, and the bottom represents the worst. Then they’re asked:

> *"On which step of the ladder would you say you personally feel you stand at this time?"*

The average response across each country becomes its **happiness score**.

This score is not random. It correlates strongly with several measurable indicators such as income, health, freedom, generosity, and social connection. Together they offer a data-driven view of well-being.
""")

    st.subheader("📊 Indicators in This Explorer")
    st.markdown("Choose a metric below to see how it is defined and where the data originally comes from.")

    metric_details = {
        "🏆 Rank": {
            "title": "Rank",
            "desc": "This is where a country stands on the global happiness list. A lower rank means higher happiness.",
            "source": "From the World Happiness Report 2025 dataset. Score derived from weighted combination of indicator values."
        },
        "💰 GDP": {
            "title": "Log GDP per capita",
            "desc": "Income level adjusted for cost of living and population size. Reflects average living standards.",
            "source": "From the World Happiness Report 2025 dataset. Originally sourced from World Bank WDI, OECD, and Penn World Table."
        },
        "🤝 Support": {
            "title": "Social support",
            "desc": "Measures whether people feel they have someone they can count on in times of trouble.",
            "source": "From the World Happiness Report 2025 dataset. Based on Gallup World Poll question on social reliability."
        },
        "❤️ Health": {
            "title": "Healthy life expectancy",
            "desc": "Estimates how long people live in good health, not just total lifespan.",
            "source": "From the World Happiness Report 2025 dataset. Derived using WHO, WDI, and global health models from Lancet."
        },
        "🕊️ Freedom": {
            "title": "Freedom to make life choices",
            "desc": "Reflects how free people feel to live their lives as they choose.",
            "source": "From the World Happiness Report 2025 dataset. Originally from Gallup World Poll life satisfaction items."
        },
        "🎁 Generosity": {
            "title": "Generosity",
            "desc": "Based on recent charitable donations, adjusted to account for income effects.",
            "source": "From the World Happiness Report 2025 dataset. Derived from Gallup donation responses and income regression."
        },
        "🚨 Corruption": {
            "title": "Perceptions of corruption",
            "desc": "Captures how common people believe corruption is in government and business.",
            "source": "From the World Happiness Report 2025 dataset. Based on Gallup survey questions on perceived corruption."
        }
    }

    selected_metric = st.radio(
        "Select a metric to view details:",
        list(metric_details.keys()),
        horizontal=True
    )

    selected = metric_details[selected_metric]
    st.markdown(f"### {selected['title']}")
    st.markdown(f"**What it means:** {selected['desc']}")
    st.markdown(f"<span style='font-size: 0.9em; color: gray;'>{selected['source']}</span>", unsafe_allow_html=True)


# ---------- TAB 1 ----------
with tabs[1]:
    with stylable_container("map", css_styles="padding: 1rem; background-color:#eef6ff; border-radius:8px"):
        selected_year = st.selectbox("📅 Select Year for Map View", years, index=len(years) - 1, key="selected_year")
        map_metric = st.selectbox("📈 Choose a Happiness Indicator", metrics)
        filtered_df = df[df["Year"] == selected_year]

        hover_cols = ["Country"]
        for col in ["Rank", "Position Changes YOY"]:
            if col in filtered_df.columns:
                hover_cols.append(col)

        st.subheader("🗺️ Visualize Happiness Around the World")
        fig_map = px.choropleth(
            filtered_df,
            locations="Country",
            locationmode="country names",
            color=map_metric,
            hover_name="Country",
            hover_data=hover_cols,
            color_continuous_scale="Turbo",
            title=f"{map_metric} by Country in {selected_year}",
        )
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), title_x=0.5)
        fig_map.update_geos(showocean=True, oceancolor="LightBlue", landcolor="white")
        st.plotly_chart(fig_map, use_container_width=True)

        st.caption("⚪ White areas indicate countries with no available data.")

    if st.checkbox("🔍 Show countries performing better than global average"):
        avg_val = filtered_df[map_metric].mean()
        if map_metric == "Rank":
            top_countries = filtered_df[filtered_df["Rank"] < avg_val]
            st.success(f"{len(top_countries)} countries ranked better than average (Rank < {round(avg_val, 1)})")
        else:
            top_countries = filtered_df[filtered_df[map_metric] > avg_val]
            st.success(f"{len(top_countries)} countries scored above average ({round(avg_val, 2)}) in '{map_metric}'")

        fig_bar = px.bar(
            top_countries.sort_values(map_metric, ascending=(map_metric == "Rank")).head(10),
            x="Country", y=map_metric, color="Country",
            title=f"Top Performing Countries in {map_metric}",
        )
        fig_bar.update_layout(title_x=0.5)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("🏅 Top 3 and Bottom 3 Countries")

    ascending = True if map_metric == "Rank" else False
    top3 = filtered_df.sort_values(map_metric, ascending=ascending).head(3)
    bottom3 = filtered_df.sort_values(map_metric, ascending=ascending).tail(3)

    col1, col2 = st.columns(2)

    with col1:
        fig_top = px.bar(top3, x="Country", y=map_metric, color="Country", title="Top 3")
        fig_top.update_layout(title_x=0.5)
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        fig_bottom = px.bar(bottom3, x="Country", y=map_metric, color="Country", title="Bottom 3")
        fig_bottom.update_layout(title_x=0.5)
        st.plotly_chart(fig_bottom, use_container_width=True)

# ---------- TAB 2 ----------
with tabs[2]:
    with stylable_container("global", css_styles="padding: 1rem; background-color:#fefefe; border-radius:8px"):
        st.header("🌐 Global Average vs. Your Chosen Countries")

        selected_countries = st.multiselect(
            "🌏 Countries of Interest", sorted(countries),
            default=["Australia", "Finland", "India", "Singapore"],
            key="global_countries"
        )
        compare_metric = st.selectbox("📈 Select Metric to Compare", metrics, key="global_metric")

        filtered_df_current = df[df["Year"] == years[-1]]
        filtered_countries_df = filtered_df_current[filtered_df_current["Country"].isin(selected_countries)]
        global_avg = filtered_df_current[compare_metric].mean()

        st.metric(f"Global Avg ({compare_metric})", f"{round(global_avg, 2)}")
        fig_bar = px.bar(
            filtered_countries_df, x="Country", y=compare_metric, color="Country",
            title=f"{compare_metric} vs Global Avg"
        )
        fig_bar.add_hline(y=global_avg, line_dash="dot", line_color="red", annotation_text="Global Avg")
        fig_bar.update_layout(title_x=0.5)
        st.plotly_chart(fig_bar, use_container_width=True)

    with stylable_container("comparison", css_styles="padding: 1rem; background-color:#fff8f2; border-radius:8px"):
        st.header("📊 Track Trends Across Countries")

        country_options = ["All Countries"] + sorted(countries)
        selected_trend_countries = st.multiselect("🌍 Country Selection", country_options, default=["Australia", "Finland", "India"])
        trend_metric = st.selectbox("📈 Metric to Track Over Time", metrics, index=metrics.index("Healthy life expectancy"), key="compare_metric")

        if "All Countries" in selected_trend_countries:
            comp_df = df.copy()
        else:
            comp_df = df[df["Country"].isin(selected_trend_countries)]

        fig_trend = px.line(comp_df, x="Year", y=trend_metric, color="Country", markers=True, title="Yearly Trends")
        fig_trend.update_layout(title_x=0.5)
        st.plotly_chart(fig_trend, use_container_width=True)

        st.header("🧭 Explore Correlation Between Metrics")
        year_corr = st.selectbox("📅 Year", years, index=len(years) - 1, key="year_corr")
        x_metric = st.selectbox("🔻 X-Axis", metrics, index=0, key="x_metric")
        y_metric = st.selectbox("🔺 Y-Axis", metrics, index=1, key="y_metric")

        corr_df = df[df["Year"] == year_corr]
        if "All Countries" not in selected_trend_countries:
            corr_df = corr_df[corr_df["Country"].isin(selected_trend_countries)]

        fig_corr = px.scatter(corr_df, x=x_metric, y=y_metric, size='Ladder Score', color='Country',
                              title=f"{y_metric} vs {x_metric} ({year_corr})")
        fig_corr.update_layout(title_x=0.5)

        # Annotate top-scoring country
        top_country = corr_df.sort_values(y_metric, ascending=False).iloc[0]
        fig_corr.add_annotation(
            x=top_country[x_metric], y=top_country[y_metric],
            text=f"🏆 {top_country['Country']}",
            showarrow=True, arrowhead=1
        )

        st.plotly_chart(fig_corr, use_container_width=True)

        clicked = st.selectbox("🔍 View Country Data", ["None"] + sorted(selected_trend_countries))
        if clicked != "None":
            st.dataframe(df[df["Country"] == clicked][["Year", x_metric, y_metric, "Ladder Score"]])

# ---------- TAB 3 ----------
with tabs[3]:
    with stylable_container("Conclusions", css_styles="padding: 1rem; background-color:#f0f4f8; border-radius:8px"):
        st.header("📌 Conclusions")
        st.write("Tobefilled.")

        
    st.subheader("📂 Where the Data Comes From")
    st.markdown("""
    All data shown here is based on the official World Happiness Report datasets.  
    To explore the full data or download it yourself, visit:  
    👉 [**worldhappiness.report/data-sharing**](https://worldhappiness.report/data-sharing/)
    """)
