import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="World Happiness Explorer", page_icon="😊")

st.title("🌍 World Happiness Explorer")
st.markdown("**From Data to Joy: Insights from Data Across Nations**")
st.caption("Connecting metrics to meaning in the pursuit of global well-being")

# ---------- BACKGROUND ----------
def set_background():
    st.markdown(
        f"""
        <style>
        html, body, .stApp {{
            color: #1a1a1a;
        }}
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
            background-color: rgba(255, 255, 255, 0.85);
            z-index: 0;
        }}
        [data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 1;
        }}
        section.main > div {{
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

def set_viewport_alerts():
    st.markdown("""
    <script>
    function showPopup(message) {
        const existing = document.getElementById("custom-popup");
        if (existing) return;

        const div = document.createElement("div");
        div.id = "custom-popup";
        div.innerHTML = message;
        div.style.position = "fixed";
        div.style.top = "10px";
        div.style.left = "50%";
        div.style.transform = "translateX(-50%)";
        div.style.padding = "12px 18px";
        div.style.backgroundColor = "#fff3cd";
        div.style.color = "#664d03";
        div.style.border = "1px solid #ffeeba";
        div.style.borderRadius = "8px";
        div.style.boxShadow = "0 2px 6px rgba(0,0,0,0.1)";
        div.style.zIndex = "9999";
        div.style.maxWidth = "90vw";
        div.style.fontSize = "14px";
        div.style.textAlign = "center";
        document.body.appendChild(div);

        setTimeout(() => { div.remove(); }, 10000);
    }

    function detectAndShowTips() {
        const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const isPortrait = window.matchMedia("(orientation: portrait)").matches;

        if (isDarkMode) {
            showPopup("🔆 You're in dark mode. Tap the ⋮ menu → Settings → Theme → Light.");
        }
        if (isPortrait) {
            showPopup("📱 Tip: Rotate your phone sideways for a better experience.");
        }
    }

    window.addEventListener("load", () => {
        requestAnimationFrame(() => setTimeout(detectAndShowTips, 600));
    });
    </script>
    """, unsafe_allow_html=True)


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

        st.subheader("🗺️ Visualize Happiness Around the World")

        # Toggle between static and animated view
        view_mode = st.radio(
            "🗺️ Select Map Mode",
            ["Static View (Select Year)", "Animated View (2019–2024)"],
            horizontal=True
        )

        if view_mode == "Animated View (2019–2024)":
            map_metric = st.selectbox("📈 Choose Indicator", metrics, index=metrics.index("Rank"), key="animated_metric")
            st.caption("Use the slider below the map to scroll through the years.")

            anim_df = df[df["Year"].between(2019, 2024)].sort_values("Year", ascending=True)

            fig_map = px.choropleth(
                anim_df,
                locations="Country",
                locationmode="country names",
                color=map_metric,
                hover_name="Country",
                hover_data=["Country", map_metric],
                color_continuous_scale="Turbo",
                animation_frame="Year"
            )

        else:
            selected_year = st.selectbox("🗓️ Select Year", years, index=len(years) - 1, key="selected_year")
            map_metric = st.selectbox("📈 Choose Indicator", metrics, key="map_metric")

            filtered_df = df[df["Year"] == selected_year]
            hover_cols = ["Country", map_metric]

            fig_map = px.choropleth(
                filtered_df,
                locations="Country",
                locationmode="country names",
                color=map_metric,
                hover_name="Country",
                hover_data=hover_cols,
                color_continuous_scale="Turbo"
            )

        # Shared layout configuration
        fig_map.update_geos(
            projection_type="natural earth",
            showcoastlines=True,
            landcolor="white",
            oceancolor="LightBlue",
            showocean=True,
            showframe=False,
        )

        fig_map.update_layout(
            title=None,
            margin=dict(l=0, r=0, t=0, b=0),
            title_x=0.5
        )

        st.plotly_chart(fig_map, use_container_width=True)

        # Only show insights for static mode
        if view_mode == "Static View (Select Year)":
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
        st.header("📌 What This Explorer Shows")

        st.markdown("""
        This dashboard brings together six years of data to explore how different countries score on happiness and what contributes to it.

        Rather than focusing only on income, it highlights how **freedom**, **trust**, **health**, and **social support** affect how people experience their lives.
        """)

        st.header("🔍 Reflections on Happiness")
        st.markdown("""
        The happiest countries in the world share more than just wealth, they also offer freedom, health, and strong social bonds.

        This explorer helps reveal how different factors contribute to well-being, and how their impact varies across the globe.

        Happiness, it turns out, isn’t just felt, it’s shaped by real conditions we can measure, compare, and improve.
        """)

        st.header("🔗 Where the Data Comes From")
        st.markdown("""
        This dashboard is powered by the official [**World Happiness Report 2025**](https://worldhappiness.report/data-sharing/), which brings together data from:
        - Gallup World Poll  
        - WHO (Healthy Life Expectancy)  
        - World Bank (GDP, social indicators)  
        - Penn World Table & OECD

        The core dataset used in this app was compiled and cleaned by the team using the official release.
        """)

        st.subheader("📸 Meet the Team")
        cols = st.columns(5)
        
        with cols[0]:
            st.image("team/Unni.png.jpg", use_container_width=True)
            st.markdown("<div style='text-align:center'><b>Krishnan Unni Prasad</b><br>Project Manager</div>", unsafe_allow_html=True)
        
        with cols[1]:
            st.image("team/Aryan.jpg", use_container_width=True)
            st.markdown("<div style='text-align:center'><b>Aryan Bansal</b><br>Data Engineer</div>", unsafe_allow_html=True)
        
        with cols[2]:
            st.image("team/Ting.jpg", use_container_width=True)
            st.markdown("<div style='text-align:center'><b>Ting Chen</b><br>Visualisation Designer</div>", unsafe_allow_html=True)
        
        with cols[3]:
            st.image("team/Gowtham.jpg", use_container_width=True)
            st.markdown("<div style='text-align:center'><b>Gowtham K. Prasanna</b><br>Data Analyst</div>", unsafe_allow_html=True)
        
        with cols[4]:
            st.image("team/Dihn.jpg", use_container_width=True)
            st.markdown("<div style='text-align:center'><b>Dinh Hung Nguyen</b><br>Audience Experience Specialist</div>", unsafe_allow_html=True)




        st.caption("Built for DVN Assignment 3 – UTS, 2025")
