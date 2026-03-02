import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Category Strategy Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to inject some extra sleekness (padding, font smoothing)
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 600; color: #1f2937; }
        .stMetric { background-color: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOCK DATA GENERATION ---
@st.cache_data
def load_data():
    brand_data = pd.DataFrame([
        # USA - Shampoo
        {"Country": "USA", "Category": "Shampoo", "Brand": "Pantene", "Share": 22, "Price": 5.00, "Price_Min": 3.50, "Price_Max": 7.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Head & Shoulders", "Share": 19, "Price": 6.50, "Price_Min": 4.50, "Price_Max": 8.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Garnier", "Share": 12, "Price": 4.50, "Price_Min": 3.00, "Price_Max": 6.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "L'Oreal Elvive", "Share": 10, "Price": 7.00, "Price_Min": 5.00, "Price_Max": 9.50},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Redken", "Share": 6, "Price": 24.00, "Price_Min": 20.00, "Price_Max": 28.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Olaplex", "Share": 5, "Price": 30.00, "Price_Min": 28.00, "Price_Max": 35.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Ouai", "Share": 3, "Price": 32.00, "Price_Min": 28.00, "Price_Max": 38.00},
        
        # USA - Fragrances
        {"Country": "USA", "Category": "Fragrances", "Brand": "Bath & Body Works", "Share": 18, "Price": 25.00, "Price_Min": 15.00, "Price_Max": 45.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Calvin Klein", "Share": 12, "Price": 65.00, "Price_Min": 45.00, "Price_Max": 85.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Chanel", "Share": 11, "Price": 140.00, "Price_Min": 120.00, "Price_Max": 180.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Dior", "Share": 10, "Price": 130.00, "Price_Min": 110.00, "Price_Max": 160.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Jo Malone", "Share": 7, "Price": 155.00, "Price_Min": 85.00, "Price_Max": 210.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Tom Ford", "Share": 5, "Price": 250.00, "Price_Min": 180.00, "Price_Max": 390.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Le Labo", "Share": 3, "Price": 220.00, "Price_Min": 95.00, "Price_Max": 310.00},

        # USA - Moisturisers
        {"Country": "USA", "Category": "Moisturisers", "Brand": "CeraVe", "Share": 20, "Price": 16.00, "Price_Min": 12.00, "Price_Max": 22.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Neutrogena", "Share": 15, "Price": 18.00, "Price_Min": 14.00, "Price_Max": 26.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Olay", "Share": 12, "Price": 25.00, "Price_Min": 18.00, "Price_Max": 38.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Clinique", "Share": 9, "Price": 45.00, "Price_Min": 30.00, "Price_Max": 75.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Kiehl's", "Share": 6, "Price": 65.00, "Price_Min": 40.00, "Price_Max": 95.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Tatcha", "Share": 4, "Price": 85.00, "Price_Min": 70.00, "Price_Max": 110.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "La Mer", "Share": 2, "Price": 250.00, "Price_Min": 190.00, "Price_Max": 450.00},

        # UK - Shampoo
        {"Country": "UK", "Category": "Shampoo", "Brand": "Tresemme", "Share": 18, "Price": 6.50, "Price_Min": 5.00, "Price_Max": 8.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Pantene", "Share": 15, "Price": 5.50, "Price_Min": 4.00, "Price_Max": 7.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Aussie", "Share": 12, "Price": 7.00, "Price_Min": 5.50, "Price_Max": 9.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "John Frieda", "Share": 9, "Price": 8.50, "Price_Min": 6.50, "Price_Max": 11.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "OGX", "Share": 8, "Price": 9.50, "Price_Min": 7.00, "Price_Max": 12.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Kerastase", "Share": 6, "Price": 32.00, "Price_Min": 28.00, "Price_Max": 40.00},
        
        # UK - Fragrances
        {"Country": "UK", "Category": "Fragrances", "Brand": "Dior", "Share": 16, "Price": 120.00, "Price_Min": 90.00, "Price_Max": 160.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Chanel", "Share": 14, "Price": 135.00, "Price_Min": 110.00, "Price_Max": 180.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Jo Malone", "Share": 12, "Price": 110.00, "Price_Min": 65.00, "Price_Max": 160.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Hugo Boss", "Share": 10, "Price": 75.00, "Price_Min": 55.00, "Price_Max": 95.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Paco Rabanne", "Share": 8, "Price": 85.00, "Price_Min": 60.00, "Price_Max": 110.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Penhaligon's", "Share": 4, "Price": 210.00, "Price_Min": 180.00, "Price_Max": 280.00},

        # UK - Moisturisers
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Simple", "Share": 19, "Price": 5.50, "Price_Min": 3.50, "Price_Max": 8.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "No7", "Share": 15, "Price": 28.00, "Price_Min": 18.00, "Price_Max": 40.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Nivea", "Share": 14, "Price": 7.00, "Price_Min": 5.00, "Price_Max": 12.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "CeraVe", "Share": 10, "Price": 15.00, "Price_Min": 12.00, "Price_Max": 20.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Elemis", "Share": 7, "Price": 85.00, "Price_Min": 55.00, "Price_Max": 130.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Charlotte Tilbury", "Share": 5, "Price": 95.00, "Price_Min": 75.00, "Price_Max": 120.00},

        # Germany - Shampoo
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Schauma", "Share": 22, "Price": 3.50, "Price_Min": 2.50, "Price_Max": 5.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Nivea", "Share": 16, "Price": 4.50, "Price_Min": 3.00, "Price_Max": 6.50},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Guhl", "Share": 14, "Price": 6.00, "Price_Min": 4.50, "Price_Max": 8.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Alpecin", "Share": 10, "Price": 9.50, "Price_Min": 7.00, "Price_Max": 12.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Plantur", "Share": 8, "Price": 11.00, "Price_Min": 9.00, "Price_Max": 14.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Kerastase", "Share": 5, "Price": 30.00, "Price_Min": 25.00, "Price_Max": 38.00},

        # Germany - Fragrances
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Hugo Boss", "Share": 18, "Price": 80.00, "Price_Min": 60.00, "Price_Max": 110.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Chanel", "Share": 15, "Price": 145.00, "Price_Min": 125.00, "Price_Max": 190.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Dior", "Share": 12, "Price": 135.00, "Price_Min": 110.00, "Price_Max": 175.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "4711", "Share": 9, "Price": 28.00, "Price_Min": 15.00, "Price_Max": 45.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Joop!", "Share": 7, "Price": 55.00, "Price_Min": 35.00, "Price_Max": 75.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Tom Ford", "Share": 4, "Price": 260.00, "Price_Min": 190.00, "Price_Max": 380.00},

        # Germany - Moisturisers
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Nivea", "Share": 30, "Price": 6.50, "Price_Min": 4.00, "Price_Max": 12.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Balea", "Share": 22, "Price": 3.50, "Price_Min": 2.00, "Price_Max": 6.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Eucerin", "Share": 14, "Price": 24.00, "Price_Min": 18.00, "Price_Max": 35.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "La Roche-Posay", "Share": 10, "Price": 28.00, "Price_Min": 20.00, "Price_Max": 40.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Weleda", "Share": 8, "Price": 15.00, "Price_Min": 10.00, "Price_Max": 22.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Dr. Hauschka", "Share": 5, "Price": 38.00, "Price_Min": 25.00, "Price_Max": 55.00},
    ])

    demo_data = pd.DataFrame([
        # USA
        {"Country": "USA", "Generation": "Gen Z", "Pop_Split": 20, "Avg_Income": 35000, "Growth_Rate": 12.5},
        {"Country": "USA", "Generation": "Millennials", "Pop_Split": 22, "Avg_Income": 85000, "Growth_Rate": 8.2},
        {"Country": "USA", "Generation": "Gen X", "Pop_Split": 19, "Avg_Income": 110000, "Growth_Rate": 2.1},
        {"Country": "USA", "Generation": "Boomers", "Pop_Split": 21, "Avg_Income": 75000, "Growth_Rate": -3.5},
        # UK
        {"Country": "UK", "Generation": "Gen Z", "Pop_Split": 19, "Avg_Income": 28000, "Growth_Rate": 11.0},
        {"Country": "UK", "Generation": "Millennials", "Pop_Split": 22, "Avg_Income": 65000, "Growth_Rate": 7.5},
        {"Country": "UK", "Generation": "Gen X", "Pop_Split": 20, "Avg_Income": 80000, "Growth_Rate": 1.5},
        {"Country": "UK", "Generation": "Boomers", "Pop_Split": 22, "Avg_Income": 55000, "Growth_Rate": -4.0},
        # Germany
        {"Country": "Germany", "Generation": "Gen Z", "Pop_Split": 18, "Avg_Income": 30000, "Growth_Rate": 10.5},
        {"Country": "Germany", "Generation": "Millennials", "Pop_Split": 20, "Avg_Income": 70000, "Growth_Rate": 6.8},
        {"Country": "Germany", "Generation": "Gen X", "Pop_Split": 23, "Avg_Income": 90000, "Growth_Rate": 1.0},
        {"Country": "Germany", "Generation": "Boomers", "Pop_Split": 25, "Avg_Income": 60000, "Growth_Rate": -5.2},
    ])

    return brand_data, demo_data

df_brands, df_demos = load_data()

# --- 3. MAIN DASHBOARD & TOP FILTERS ---
st.title("🎯 Category Strategy & Audience Dashboard")
st.markdown("Identify white space, track competitors, and target high-value cohorts.")

# Top-level filters
filter_col1, filter_col2, _ = st.columns([1, 1, 2]) # Added an empty column to keep filters compact
selected_country = filter_col1.selectbox("🌐 Market Selection", options=["USA", "UK", "Germany"])
selected_category = filter_col2.selectbox("🛍️ Category Selection", options=["Shampoo", "Fragrances", "Moisturisers"])

st.markdown("<br>", unsafe_allow_html=True) # Sleek spacing

# Apply Filters
filtered_brands = df_brands[(df_brands["Country"] == selected_country) & (df_brands["Category"] == selected_category)]
filtered_demos = df_demos[df_demos["Country"] == selected_country]

# --- 4. KPI ROW ---
kpi1, kpi2, kpi3 = st.columns(3)
market_leader = filtered_brands.loc[filtered_brands['Share'].idxmax()]
highest_earner = filtered_demos.loc[filtered_demos['Avg_Income'].idxmax()]
fastest_growing = filtered_demos.loc[filtered_demos['Growth_Rate'].idxmax()]

kpi1.metric("👑 Market Leader (Volume)", f"{market_leader['Brand']}", f"{market_leader['Share']}% Share")
kpi2.metric("💰 Most Lucrative Cohort", f"{highest_earner['Generation']}", f"${highest_earner['Avg_Income']:,.0f} Avg Income")
kpi3.metric("📈 Fastest Growing Cohort", f"{fastest_growing['Generation']}", f"+{fastest_growing['Growth_Rate']}% (5 Yr)")

st.divider()

# Shared Layout configuration for a sleek, grid-less look
sleek_layout_updates = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='#e5e7eb'),
    yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='#e5e7eb'),
    margin=dict(l=40, r=40, t=40, b=40),
    font=dict(color="#4b5563")
)

# --- 5. CHART 1: BRAND LANDSCAPE (FULL WIDTH) ---
st.subheader("1. Where to Play: Competitive Brand Landscape")
st.markdown("Price elasticity vs Market Share. Shaded backgrounds indicate typical cohort purchasing power thresholds.")

fig_brands = go.Figure()

max_price = filtered_brands['Price_Max'].max()
mass_threshold = filtered_brands['Price'].quantile(0.33)
premium_threshold = filtered_brands['Price'].quantile(0.75)

# Shaded Overlays for Demographics (Soft, modern colors)
fig_brands.add_hrect(y0=0, y1=mass_threshold, line_width=0, fillcolor="rgba(243, 244, 246, 0.8)", annotation_text="Gen Z / Entry Tier", annotation_position="top right", annotation_font_color="#9ca3af")
fig_brands.add_hrect(y0=mass_threshold, y1=premium_threshold, line_width=0, fillcolor="rgba(224, 242, 254, 0.5)", annotation_text="Millennial / Premium Tier", annotation_position="top right", annotation_font_color="#7dd3fc")
fig_brands.add_hrect(y0=premium_threshold, y1=max_price * 1.1, line_width=0, fillcolor="rgba(254, 240, 138, 0.3)", annotation_text="Gen X / Ultra-Premium Tier", annotation_position="top right", annotation_font_color="#fde047")

# Brand markers with error bars representing the price range
fig_brands.add_trace(go.Scatter(
    x=filtered_brands["Share"],
    y=filtered_brands["Price"],
    mode="markers+text",
    text=filtered_brands["Brand"],
    textposition="top center",
    marker=dict(symbol="square", size=16, color="#2563eb", line=dict(width=2, color="#1e40af")),
    error_y=dict(
        type='data',
        symmetric=False,
        array=filtered_brands["Price_Max"] - filtered_brands["Price"],
        arrayminus=filtered_brands["Price"] - filtered_brands["Price_Min"],
        color='#9ca3af',
        thickness=2,
        width=6
    ),
    name="Brands"
))

fig_brands.update_layout(
    height=500,
    xaxis_title="Market Share (%)",
    yaxis_title="Average Price (USD $)",
    showlegend=False,
    **sleek_layout_updates
)
st.plotly_chart(fig_brands, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- 6. CHART 2: DEMOGRAPHIC BUBBLE CHART (FULL WIDTH) ---
st.subheader("2. Who to Target: Cohort Momentum Matrix")
st.markdown("Bubble size represents Total Population percentage. Visualizing the relationship between growing cohorts and their household wealth.")

fig_demos = px.scatter(
    filtered_demos,
    x="Growth_Rate",
    y="Avg_Income",
    size="Pop_Split",
    color="Generation",
    text="Generation",
    size_max=80, # Larger bubbles for emphasis
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Add quadrant lines based on averages
avg_growth = filtered_demos['Growth_Rate'].mean()
avg_inc = filtered_demos['Avg_Income'].mean()
fig_demos.add_vline(x=avg_growth, line_width=1, line_dash="dash", line_color="#d1d5db")
fig_demos.add_hline(y=avg_inc, line_width=1, line_dash="dash", line_color="#d1d5db")

# Clean styling and remove grid
fig_demos.update_traces(textposition='top center', textfont=dict(color="#374151", size=14), marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig_demos.update_layout(
    height=500,
    xaxis_title="5-Year Growth Rate (%)",
    yaxis_title="Average Household Income (USD $)",
    showlegend=False,
    **sleek_layout_updates
)
# Ensure x-axis shows the zero point if there is negative growth
fig_demos.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#e5e7eb')

st.plotly_chart(fig_demos, use_container_width=True)

st.divider()

# --- 7. DYNAMIC INSIGHTS ENGINE ---
st.subheader("💡 Strategic Insights & White Space")

premium_brands = filtered_brands[filtered_brands['Price'] > premium_threshold]
mass_brands = filtered_brands[filtered_brands['Price'] <= mass_threshold]
premium_brand_names = ", ".join(premium_brands['Brand'].tolist()) if not premium_brands.empty else "None"

st.info(f"""
* **The Momentum Play (Bottom-Right Quadrant):** **{fastest_growing['Generation']}** is driving the most aggressive growth (+{fastest_growing['Growth_Rate']}%) in {selected_country}. Tracking this back to the brand landscape, the primary players targeting their accessible price-points (Under ${mass_threshold:.2f}) are {mass_brands['Brand'].iloc[0] if not mass_brands.empty else 'mass-market labels'}. Winning this cohort now secures the category pipeline for the next decade.
* **The Wealth Vacuum (Top-Left Quadrant):** **{highest_earner['Generation']}** commands the highest average income (${highest_earner['Avg_Income']:,.0f}) but is growing slower. On the brand chart, volume is heavily skewed toward the bottom half. Brands like {premium_brand_names} play here, but their low market share reveals massive untapped potential for a "masstige" line designed to capture this specific density of wealth.
* **Defending the Crown:** As the absolute market leader, **{market_leader['Brand']}** holds a strong defensive position in volume. To drive margin expansion without cannibalizing core share, they should explore strategic sub-branding explicitly targeting the blue Millennial/Premium tier.
""")
