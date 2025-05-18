# Happy Viz: World Happiness Explorer

**Live App:** [https://happyviz.streamlit.app](https://happyviz.streamlit.app)  
**Course:** Data Visualisation and Narratives – UTS 2025  
**Team:** 3  
**Repo:** GitHub-hosted Streamlit deployment  
**Total Commits:** 190+  
**Data Period:** 2019–2024 (cleaned)

---

## Overview

Happy Viz is an interactive data storytelling dashboard built with Streamlit, designed to help global stakeholders explore patterns in happiness rankings across 140+ countries. Inspired by Bhutan's vision of Gross National Happiness, our app encourages deeper insight into what truly drives well-being — beyond GDP.

---

## Features

- Animated Global Map – Visualise trends across time and region  
- Top/Bottom Insights – Track yearly highs and lows  
- Custom Line Plots – Explore individual country trends  
- Metric Correlation Explorer – Compare happiness factors  
- Global Benchmark Comparison – See how countries measure up

---

## Dataset

**Source:**  
[World Happiness Report – Figure 2.1 Dataset](https://worldhappiness.report/data-sharing/)  
→ Used exclusively (no external datasets)  
→ Focused on years 2019–2024 for consistency

---

## Tech Stack

- Python (pandas, plotly, streamlit)  
- Streamlit Cloud for deployment  
- GitHub for version control and workflows  
- No external data or dashboard tools used

---

## Repo Structure

```
├── app.py                      # Main Streamlit app
├── happinessreport.csv        # Raw data file
├── happinessreport_cleaned.csv# Processed dataset (2019–2024)
├── requirements.txt           # App dependencies
├── .streamlit/                # Streamlit config
├── .github/workflows/         # Keep-alive workflow
├── team/                      # Team member images
└── README.md                  # Project summary (this file)
```

---

## Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/happyviz.git
   cd happyviz
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Team 3 Members

- Krishnan Unni Prasad – Project Manager  
- Aryan Bansal – Data Engineer  
- Ting Chen – Visualisation Designer  
- Gowtham K. Prasanna – Data Analyst  
- Dinh Hung Nguyen – Audience Experience Specialist

---

© UTS 2025 – Built for DVN Assignment 3
