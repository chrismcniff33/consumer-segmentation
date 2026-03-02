import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Category Strategy Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- 2. MOCK DATA GENERATION (National Stats & Brand Estimates) ---
@st.cache_data
def load_data():
    # Brand Data: Country, Category, Brand, Market Share (%), Avg Price ($)
    brand_data = pd.DataFrame([
        # USA - Shampoo
        {"Country": "USA", "Category": "Shampoo", "Brand": "Head & Shoulders", "Share": 22, "Price": 6.50},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Pantene", "Share": 18, "Price": 5.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Olaplex", "Share": 8, "Price": 30.00},
        # USA - Fragrances
        {"Country": "USA", "Category": "Fragrances", "Brand": "Chanel", "Share": 15, "Price": 135.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Calvin Klein", "Share": 12, "Price": 65.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Tom Ford", "Share": 7, "Price": 250.00},
        # USA - Moisturisers
        {"Country": "USA", "Category": "Moisturisers", "Brand": "CeraVe", "Share": 25, "Price": 15.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Neutrogena", "Share": 18, "Price": 12.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "La Mer", "Share": 5, "Price": 200.00},
        
        # UK - Shampoo
        {"Country": "UK", "Category": "Shampoo", "Brand": "Tresemme", "Share": 20, "Price": 5.50},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Aussie", "Share": 15, "Price": 6.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Kerastase", "Share": 9, "Price": 28.00},
        # UK - Fragrances
        {"Country": "UK", "Category": "Fragrances", "Brand": "Dior", "Share": 18, "Price": 110.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Jo Malone", "Share": 14, "Price": 95.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Hugo Boss", "Share": 10, "Price": 60.00},
        # UK - Moisturisers
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Simple", "Share": 22, "Price": 4.50},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "No7", "Share": 16, "Price": 25.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Elemis", "Share": 8, "Price": 85.00},
        
        # Germany - Shampoo
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Schauma", "Share": 24, "Price": 3.50},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Guhl", "Share": 16, "Price": 5.50},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Alpecin", "Share": 12, "Price": 8.00},
        # Germany - Fragrances
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Hugo Boss", "Share": 20, "Price": 70.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Chanel", "Share": 14, "Price": 140.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "4711", "Share": 8, "Price": 25.00},
        # Germany - Moisturisers
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Nivea", "Share": 35, "Price": 6.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Balea", "Share": 20, "Price": 3.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Eucerin", "Share": 12, "Price": 22.00},
    ])

    # Demographic Data: Country, Generation, Pop Split (%), Avg Income ($), 5Yr Growth (%)
    demo_data = pd.DataFrame([
        # USA
        {"Country": "USA", "Generation": "Gen Z (1997-2012)", "Pop_Split": 20, "Avg_Income": 35000, "Growth_Rate": 12.5},
        {"Country": "USA", "Generation": "Millennials (1981-1996)", "Pop_Split": 22, "Avg_Income": 85000, "Growth_Rate": 8.2},
        {"Country": "USA", "Generation": "Gen X (1965-1980)", "Pop_Split": 19, "Avg_Income": 110000, "Growth_Rate": 2.1},
        {"Country": "USA", "Generation": "Boomers (1946-1964)", "Pop_Split": 21, "Avg_Income": 75000, "Growth_Rate": -3.5},
        # UK
        {"Country": "UK", "Generation": "Gen Z (1997-2012)", "Pop_Split": 19, "Avg_Income": 28000, "Growth_Rate": 11.0},
        {"Country": "UK", "Generation": "Millennials (1981-1996)", "Pop_Split": 22, "Avg_Income": 65000, "Growth_Rate": 7.5},
        {"Country": "UK", "Generation": "Gen X (1965-1980)", "Pop_Split": 20, "Avg_Income": 80000, "Growth_Rate": 1.5},
        {"Country": "UK", "Generation": "Boomers (1946-1964)", "Pop_Split": 22, "Avg_Income": 55000, "Growth_Rate": -4.0},
        # Germany
        {"Country": "Germany", "Generation": "Gen Z (1997-2012)", "Pop_Split": 18, "Avg_Income": 30000, "Growth_Rate": 10.5},
        {"Country": "Germany", "Generation": "Millennials (1981-1996)", "Pop_Split": 20, "Avg_Income": 70000, "Growth_Rate": 6.8},
        {"Country": "Germany", "Generation": "Gen X (1965-1980)", "Pop_Split": 23, "Avg_Income": 90000, "Growth_Rate": 1.0},
        {"Country": "Germany", "Generation": "Boomers (1946-1964)", "Pop_Split": 25, "Avg_Income": 60000, "Growth_Rate": -5.2},
    ])
    
    # Historical Cohort Growth Data (for line chart)
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    growth_data = []
    for _, row in demo_data.iterrows():
        base_pop = row["Pop_Split"]
        for i, year in enumerate(years):
            # Simulate a compounding trend based on the overall growth rate
            adjusted_pop = base_pop * (1 + (row["Growth_Rate"]/100 / len(years)) * i)
            growth_data.append({"Country": row["Country"], "Generation": row["Generation"], "Year": year, "Pop_Index": adjusted_pop})
    
    growth_df = pd.DataFrame(growth_data)

    return brand_data, demo_data, growth_df

df_brands, df_demos, df_growth = load_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.title("Strategic Filters")
st.sidebar.markdown("Define your market perimeter.")
selected_country = st.sidebar.selectbox("Select Country", options=["USA", "UK", "Germany"])
selected_category = st.sidebar.selectbox("Select Category", options=["Shampoo", "Fragrances", "Moisturisers"])

# Filter Datasets
filtered_brands = df_brands[(df_brands["Country"] == selected_country) & (df_brands["Category"] == selected_category)]
filtered_demos = df_demos[df_demos["Country"] == selected_country]
filtered_growth = df_growth[df_growth["Country"] == selected_country]

# --- 4. MAIN DASHBOARD ---
st.title("🎯 Category Strategy & Audience Dashboard")
st.markdown(f"**Market:** {selected_country} | **Category:** {selected_category}")
st.divider()

# --- KPI ROW ---
col1, col2, col3 = st.columns(3)
market_leader = filtered_brands.loc[filtered_brands['Share'].idxmax()]
highest_earner = filtered_demos.loc[filtered_demos['Avg_Income'].idxmax()]
fastest_growing = filtered_demos.loc[filtered_demos['Growth_Rate'].idxmax()]

col1.metric("👑 Market Leader (Volume)", f"{market_leader['Brand']}", f"{market_leader['Share']}% Share")
col2.metric("💰 Most Lucrative Cohort", f"{highest_earner['Generation'].split()[0]}", f"${highest_earner['Avg_Income']:,.0f} Avg Income")
col3.metric("📈 Fastest Growing Cohort", f"{fastest_growing['Generation'].split()[0]}", f"+{fastest_growing['Growth_Rate']}% (5 Yr)")

st.write("")

# --- CHARTS ROW 1 ---
st.subheader("1. Where to Play: Brand Competitive Landscape")
st.markdown("Identifies brand positioning based on average price point vs. market share.")

# Scatter/Bubble Chart for Brands
fig_brands = px.scatter(
    filtered_brands, 
    x="Price", 
    y="Share", 
    size="Share", 
    color="Brand",
    hover_name="Brand",
    text="Brand",
    size_max=40,
    labels={"Price": "Average Price Point ($)", "Share": "Market Share (%)"}
)
fig_brands.update_traces(textposition='top center')
fig_brands.update_layout(height=400, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
# Add quadrants for visual flair
avg_price = filtered_brands['Price'].mean()
avg_share = filtered_brands['Share'].mean()
fig_brands.add_vline(x=avg_price, line_width=1, line_dash="dash", line_color="gray")
fig_brands.add_hline(y=avg_share, line_width=1, line_dash="dash", line_color="gray")
st.plotly_chart(fig_brands, use_container_width=True)

# --- CHARTS ROW 2 ---
st.subheader("2. Who to Target: Demographic Opportunity")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**Cohort Size vs. Purchasing Power**")
    # Combo chart: Bar for Pop Split, Line/Markers for Income
    fig_demos = go.Figure()
    fig_demos.add_trace(go.Bar(
        x=filtered_demos['Generation'], 
        y=filtered_demos['Pop_Split'], 
        name='Population %', 
        marker_color='rgb(55, 83, 109)'
    ))
    fig_demos.add_trace(go.Scatter(
        x=filtered_demos['Generation'], 
        y=filtered_demos['Avg_Income'], 
        name='Avg Income ($)', 
        yaxis='y2',
        marker=dict(color='rgb(26, 118, 255)', size=10),
        mode='lines+markers'
    ))
    fig_demos.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(title='Population Share (%)'),
        yaxis2=dict(title='Avg Household Income ($)', overlaying='y', side='right', showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_demos, use_container_width=True)

with col_chart2:
    st.markdown("**Purchasing Power Growth Trend (2019-2024)**")
    fig_growth = px.line(
        filtered_growth, 
        x="Year", 
        y="Pop_Index", 
        color="Generation", 
        markers=True,
        labels={"Pop_Index": "Relative Cohort Size Index", "Year": ""}
    )
    fig_growth.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig_growth, use_container_width=True)

# --- CALLOUTS & INSIGHTS ---
st.subheader("💡 Strategic Insights")

# Automated text generation based on data filters
insight_text = f"""
* **Defensive Strategy:** **{market_leader['Brand']}** currently dominates the {selected_category} market in {selected_country} at a lower price point (${market_leader['Price']:.2f}). To compete for volume, marketing should target the largest demographic blocks. 
* **Premiumization Opportunity:** There is white space to target **{highest_earner['Generation']}**. They hold the highest average income (${highest_earner['Avg_Income']:,.0f}) but are often underserved by mass-market brands. Launching a premium line priced closer to the quadrant averages could capture this wealth.
* **Future Proofing:** **{fastest_growing['Generation']}** is the fastest-growing cohort (+{fastest_growing['Growth_Rate']}%) in {selected_country}. If creating an entry-level {selected_category} product, establishing brand loyalty with this group now is critical for long-term category share.
"""
st.info(insight_text)
