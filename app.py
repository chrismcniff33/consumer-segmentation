import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Category Strategy Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 600; color: #1f2937; }
        .stMetric { background-color: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; }
    </style>
""", unsafe_allow_html=True)

# --- 2. COLOR PALETTE DICTIONARY ---
# Ensuring exact color matching between demographic bubbles and brand chart shaded zones.
GEN_COLORS = {
    "Gen Z": "#7dd3fc",       # Soft Light Blue
    "Millennials": "#6ee7b7", # Soft Mint Green
    "Gen X": "#fcd34d",       # Soft Warm Yellow/Peach
    "Boomers": "#c4b5fd"      # Soft Lavender
}

# --- 3. MOCK DATA GENERATION (Expanded & Realistic) ---
@st.cache_data
def load_data():
    brand_data = pd.DataFrame([
        # USA - Shampoo (Story: Heavy mass market, high-end niche, gap in the middle "masstige")
        {"Country": "USA", "Category": "Shampoo", "Brand": "Pantene", "Share": 19, "Price": 5.50, "Price_Min": 4.00, "Price_Max": 7.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Head & Shoulders", "Share": 17, "Price": 6.50, "Price_Min": 5.00, "Price_Max": 8.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Suave", "Share": 12, "Price": 3.50, "Price_Min": 2.50, "Price_Max": 4.50},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Garnier Fructis", "Share": 10, "Price": 4.50, "Price_Min": 3.50, "Price_Max": 6.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "L'Oreal Elvive", "Share": 9, "Price": 7.00, "Price_Min": 5.50, "Price_Max": 9.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "OGX", "Share": 7, "Price": 9.50, "Price_Min": 7.50, "Price_Max": 11.50},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Redken", "Share": 5, "Price": 24.00, "Price_Min": 20.00, "Price_Max": 28.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Olaplex", "Share": 4, "Price": 30.00, "Price_Min": 28.00, "Price_Max": 32.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Ouai", "Share": 3, "Price": 32.00, "Price_Min": 28.00, "Price_Max": 36.00},
        {"Country": "USA", "Category": "Shampoo", "Brand": "Oribe", "Share": 2, "Price": 49.00, "Price_Min": 45.00, "Price_Max": 55.00},
        
        # USA - Fragrances 
        {"Country": "USA", "Category": "Fragrances", "Brand": "Bath & Body Works", "Share": 18, "Price": 25.00, "Price_Min": 15.00, "Price_Max": 45.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Victoria's Secret", "Share": 12, "Price": 35.00, "Price_Min": 20.00, "Price_Max": 55.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Calvin Klein", "Share": 10, "Price": 65.00, "Price_Min": 45.00, "Price_Max": 85.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Chanel", "Share": 9, "Price": 140.00, "Price_Min": 120.00, "Price_Max": 180.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Dior", "Share": 8, "Price": 130.00, "Price_Min": 110.00, "Price_Max": 160.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Marc Jacobs", "Share": 6, "Price": 95.00, "Price_Min": 75.00, "Price_Max": 120.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Jo Malone", "Share": 5, "Price": 155.00, "Price_Min": 85.00, "Price_Max": 210.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Tom Ford", "Share": 4, "Price": 250.00, "Price_Min": 180.00, "Price_Max": 390.00},
        {"Country": "USA", "Category": "Fragrances", "Brand": "Le Labo", "Share": 3, "Price": 220.00, "Price_Min": 95.00, "Price_Max": 310.00},

        # USA - Moisturisers
        {"Country": "USA", "Category": "Moisturisers", "Brand": "CeraVe", "Share": 18, "Price": 16.00, "Price_Min": 12.00, "Price_Max": 22.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Cetaphil", "Share": 14, "Price": 14.00, "Price_Min": 10.00, "Price_Max": 18.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Neutrogena", "Share": 12, "Price": 18.00, "Price_Min": 14.00, "Price_Max": 26.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Olay", "Share": 11, "Price": 25.00, "Price_Min": 18.00, "Price_Max": 38.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "La Roche-Posay", "Share": 8, "Price": 32.00, "Price_Min": 22.00, "Price_Max": 45.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Clinique", "Share": 7, "Price": 45.00, "Price_Min": 30.00, "Price_Max": 75.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Kiehl's", "Share": 5, "Price": 65.00, "Price_Min": 40.00, "Price_Max": 95.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "Tatcha", "Share": 3, "Price": 85.00, "Price_Min": 70.00, "Price_Max": 110.00},
        {"Country": "USA", "Category": "Moisturisers", "Brand": "La Mer", "Share": 2, "Price": 250.00, "Price_Min": 190.00, "Price_Max": 450.00},

        # UK - Shampoo
        {"Country": "UK", "Category": "Shampoo", "Brand": "Tresemme", "Share": 16, "Price": 6.50, "Price_Min": 5.00, "Price_Max": 8.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Pantene", "Share": 14, "Price": 5.50, "Price_Min": 4.00, "Price_Max": 7.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Aussie", "Share": 10, "Price": 7.00, "Price_Min": 5.50, "Price_Max": 9.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Alberto Balsam", "Share": 9, "Price": 2.50, "Price_Min": 1.50, "Price_Max": 3.50},
        {"Country": "UK", "Category": "Shampoo", "Brand": "John Frieda", "Share": 8, "Price": 8.50, "Price_Min": 6.50, "Price_Max": 11.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "OGX", "Share": 7, "Price": 9.50, "Price_Min": 7.00, "Price_Max": 12.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Shea Moisture", "Share": 5, "Price": 12.00, "Price_Min": 9.00, "Price_Max": 15.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Kerastase", "Share": 4, "Price": 32.00, "Price_Min": 28.00, "Price_Max": 40.00},
        {"Country": "UK", "Category": "Shampoo", "Brand": "Pureology", "Share": 2, "Price": 26.00, "Price_Min": 22.00, "Price_Max": 30.00},
        
        # UK - Fragrances
        {"Country": "UK", "Category": "Fragrances", "Brand": "Dior", "Share": 14, "Price": 120.00, "Price_Min": 90.00, "Price_Max": 160.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Chanel", "Share": 13, "Price": 135.00, "Price_Min": 110.00, "Price_Max": 180.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Jo Malone", "Share": 11, "Price": 110.00, "Price_Min": 65.00, "Price_Max": 160.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Hugo Boss", "Share": 9, "Price": 75.00, "Price_Min": 55.00, "Price_Max": 95.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Paco Rabanne", "Share": 8, "Price": 85.00, "Price_Min": 60.00, "Price_Max": 110.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "YSL", "Share": 7, "Price": 105.00, "Price_Min": 80.00, "Price_Max": 140.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Tom Ford", "Share": 4, "Price": 220.00, "Price_Min": 160.00, "Price_Max": 350.00},
        {"Country": "UK", "Category": "Fragrances", "Brand": "Penhaligon's", "Share": 3, "Price": 210.00, "Price_Min": 180.00, "Price_Max": 280.00},

        # UK - Moisturisers
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Simple", "Share": 16, "Price": 5.50, "Price_Min": 3.50, "Price_Max": 8.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "No7", "Share": 14, "Price": 28.00, "Price_Min": 18.00, "Price_Max": 40.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Nivea", "Share": 12, "Price": 7.00, "Price_Min": 5.00, "Price_Max": 12.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "CeraVe", "Share": 11, "Price": 15.00, "Price_Min": 12.00, "Price_Max": 20.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Byoma", "Share": 8, "Price": 14.00, "Price_Min": 11.00, "Price_Max": 16.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Clarins", "Share": 6, "Price": 48.00, "Price_Min": 35.00, "Price_Max": 70.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Elemis", "Share": 5, "Price": 85.00, "Price_Min": 55.00, "Price_Max": 130.00},
        {"Country": "UK", "Category": "Moisturisers", "Brand": "Charlotte Tilbury", "Share": 4, "Price": 95.00, "Price_Min": 75.00, "Price_Max": 120.00},

        # Germany - Shampoo
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Schauma", "Share": 18, "Price": 3.50, "Price_Min": 2.50, "Price_Max": 5.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Nivea", "Share": 15, "Price": 4.50, "Price_Min": 3.00, "Price_Max": 6.50},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Balea", "Share": 12, "Price": 1.50, "Price_Min": 0.90, "Price_Max": 2.50},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Guhl", "Share": 11, "Price": 6.00, "Price_Min": 4.50, "Price_Max": 8.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Alpecin", "Share": 9, "Price": 9.50, "Price_Min": 7.00, "Price_Max": 12.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Plantur", "Share": 7, "Price": 11.00, "Price_Min": 9.00, "Price_Max": 14.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Syoss", "Share": 6, "Price": 5.50, "Price_Min": 4.00, "Price_Max": 7.00},
        {"Country": "Germany", "Category": "Shampoo", "Brand": "Kerastase", "Share": 4, "Price": 30.00, "Price_Min": 25.00, "Price_Max": 38.00},

        # Germany - Fragrances
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Hugo Boss", "Share": 16, "Price": 80.00, "Price_Min": 60.00, "Price_Max": 110.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Chanel", "Share": 13, "Price": 145.00, "Price_Min": 125.00, "Price_Max": 190.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Dior", "Share": 11, "Price": 135.00, "Price_Min": 110.00, "Price_Max": 175.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "4711", "Share": 8, "Price": 28.00, "Price_Min": 15.00, "Price_Max": 45.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Joop!", "Share": 6, "Price": 55.00, "Price_Min": 35.00, "Price_Max": 75.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Jil Sander", "Share": 5, "Price": 65.00, "Price_Min": 45.00, "Price_Max": 90.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Tom Ford", "Share": 4, "Price": 260.00, "Price_Min": 190.00, "Price_Max": 380.00},
        {"Country": "Germany", "Category": "Fragrances", "Brand": "Creed", "Share": 2, "Price": 310.00, "Price_Min": 250.00, "Price_Max": 400.00},

        # Germany - Moisturisers
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Nivea", "Share": 25, "Price": 6.50, "Price_Min": 4.00, "Price_Max": 12.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Balea", "Share": 18, "Price": 3.50, "Price_Min": 2.00, "Price_Max": 6.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Eucerin", "Share": 12, "Price": 24.00, "Price_Min": 18.00, "Price_Max": 35.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "La Roche-Posay", "Share": 9, "Price": 28.00, "Price_Min": 20.00, "Price_Max": 40.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Weleda", "Share": 8, "Price": 15.00, "Price_Min": 10.00, "Price_Max": 22.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Dr. Hauschka", "Share": 5, "Price": 38.00, "Price_Min": 25.00, "Price_Max": 55.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Annemarie Börlind", "Share": 4, "Price": 45.00, "Price_Min": 30.00, "Price_Max": 65.00},
        {"Country": "Germany", "Category": "Moisturisers", "Brand": "Biotherm", "Share": 3, "Price": 55.00, "Price_Min": 40.00, "Price_Max": 80.00},
    ])

    # Realistic western demographic approximations (2024-2026 data)
    demo_data = pd.DataFrame([
        # USA
        {"Country": "USA", "Generation": "Gen Z", "Pop_Split": 20.5, "Avg_Income": 45000, "Growth_Rate": 14.5},
        {"Country": "USA", "Generation": "Millennials", "Pop_Split": 21.8, "Avg_Income": 92000, "Growth_Rate": 6.2},
        {"Country": "USA", "Generation": "Gen X", "Pop_Split": 19.2, "Avg_Income": 118000, "Growth_Rate": 1.1},
        {"Country": "USA", "Generation": "Boomers", "Pop_Split": 20.1, "Avg_Income": 78000, "Growth_Rate": -4.5},
        # UK (Income in USD for dashboard consistency)
        {"Country": "UK", "Generation": "Gen Z", "Pop_Split": 19.4, "Avg_Income": 38000, "Growth_Rate": 12.0},
        {"Country": "UK", "Generation": "Millennials", "Pop_Split": 22.1, "Avg_Income": 75000, "Growth_Rate": 5.5},
        {"Country": "UK", "Generation": "Gen X", "Pop_Split": 20.0, "Avg_Income": 98000, "Growth_Rate": 0.8},
        {"Country": "UK", "Generation": "Boomers", "Pop_Split": 21.3, "Avg_Income": 62000, "Growth_Rate": -5.0},
        # Germany (Older population skew)
        {"Country": "Germany", "Generation": "Gen Z", "Pop_Split": 16.5, "Avg_Income": 42000, "Growth_Rate": 11.5},
        {"Country": "Germany", "Generation": "Millennials", "Pop_Split": 19.8, "Avg_Income": 84000, "Growth_Rate": 4.8},
        {"Country": "Germany", "Generation": "Gen X", "Pop_Split": 23.1, "Avg_Income": 105000, "Growth_Rate": 0.5},
        {"Country": "Germany", "Generation": "Boomers", "Pop_Split": 24.5, "Avg_Income": 68000, "Growth_Rate": -6.2},
    ])

    return brand_data, demo_data

df_brands, df_demos = load_data()

# --- 4. TOP FILTERS & KPI ROW ---
st.title("🎯 Category Strategy & Audience Dashboard")
st.markdown("Identify white space, track competitors, and target high-value cohorts.")

filter_col1, filter_col2, _ = st.columns([1, 1, 2])
selected_country = filter_col1.selectbox("🌐 Market Selection", options=["USA", "UK", "Germany"])
selected_category = filter_col2.selectbox("🛍️ Category Selection", options=["Shampoo", "Fragrances", "Moisturisers"])

filtered_brands = df_brands[(df_brands["Country"] == selected_country) & (df_brands["Category"] == selected_category)]
filtered_demos = df_demos[df_demos["Country"] == selected_country]

st.markdown("<br>", unsafe_allow_html=True)

kpi1, kpi2, kpi3 = st.columns(3)
market_leader = filtered_brands.loc[filtered_brands['Share'].idxmax()]
highest_earner = filtered_demos.loc[filtered_demos['Avg_Income'].idxmax()]
fastest_growing = filtered_demos.loc[filtered_demos['Growth_Rate'].idxmax()]

kpi1.metric("👑 Market Leader (Volume)", f"{market_leader['Brand']}", f"{market_leader['Share']}% Share")
kpi2.metric("💰 Peak Earning Cohort", f"{highest_earner['Generation']}", f"${highest_earner['Avg_Income']:,.0f} Avg Income")
kpi3.metric("📈 Fastest Growing Cohort", f"{fastest_growing['Generation']}", f"+{fastest_growing['Growth_Rate']}% (5 Yr)")

st.divider()

# Shared Layout configuration for a sleek, grid-less look
sleek_layout_updates = dict(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='#e5e7eb'),
    yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='#e5e7eb'),
    margin=dict(l=20, r=20, t=40, b=20), font=dict(color="#4b5563")
)

# --- 5. SIDE-BY-SIDE CHARTS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Competitive Brand Landscape")
    st.markdown("Price vs Market Share. Background layers reflect demographic wealth bands.")

    fig_brands = go.Figure()

    max_price = filtered_brands['Price_Max'].max()
    mass_threshold = filtered_brands['Price'].quantile(0.33)
    premium_threshold = filtered_brands['Price'].quantile(0.75)

    # Background Demographic Overlays (Using exact colors from dict, with opacity, strictly below data)
    fig_brands.add_hrect(y0=0, y1=mass_threshold, line_width=0, fillcolor=GEN_COLORS["Gen Z"], opacity=0.2, layer="below", annotation_text="Gen Z / Entry Tier", annotation_position="top right", annotation_font_color="#64748b")
    fig_brands.add_hrect(y0=mass_threshold, y1=premium_threshold, line_width=0, fillcolor=GEN_COLORS["Millennials"], opacity=0.2, layer="below", annotation_text="Millennial / Premium Tier", annotation_position="top right", annotation_font_color="#64748b")
    fig_brands.add_hrect(y0=premium_threshold, y1=max_price * 1.1, line_width=0, fillcolor=GEN_COLORS["Gen X"], opacity=0.2, layer="below", annotation_text="Gen X / Ultra-Premium Tier", annotation_position="top right", annotation_font_color="#64748b")

    # Brand markers (Circles)
    fig_brands.add_trace(go.Scatter(
        x=filtered_brands["Share"],
        y=filtered_brands["Price"],
        mode="markers+text",
        text=filtered_brands["Brand"],
        textposition="top center",
        marker=dict(symbol="circle", size=16, color="#1e40af", line=dict(width=2, color="#ffffff")),
        error_y=dict(
            type='data', symmetric=False,
            array=filtered_brands["Price_Max"] - filtered_brands["Price"],
            arrayminus=filtered_brands["Price"] - filtered_brands["Price_Min"],
            color='#9ca3af', thickness=1.5, width=4
        ),
        name="Brands"
    ))

    fig_brands.update_layout(height=450, xaxis_title="Market Share (%)", yaxis_title="Average Price (USD $)", showlegend=False, **sleek_layout_updates)
    st.plotly_chart(fig_brands, use_container_width=True)

with col_right:
    st.subheader("2. Cohort Momentum Matrix")
    st.markdown("Bubble size = Population %. Matching colors map directly to brand pricing tiers.")

    fig_demos = px.scatter(
        filtered_demos,
        x="Growth_Rate",
        y="Avg_Income",
        size="Pop_Split",
        color="Generation",
        text="Generation",
        size_max=80,
        color_discrete_map=GEN_COLORS # Hardcoded color mapping to match the left chart
    )

    avg_growth = filtered_demos['Growth_Rate'].mean()
    avg_inc = filtered_demos['Avg_Income'].mean()
    fig_demos.add_vline(x=avg_growth, line_width=1, line_dash="dash", line_color="#d1d5db", layer="below")
    fig_demos.add_hline(y=avg_inc, line_width=1, line_dash="dash", line_color="#d1d5db", layer="below")

    fig_demos.update_traces(textposition='top center', textfont=dict(color="#374151", size=13), marker=dict(line=dict(width=1.5, color='#ffffff')))
    fig_demos.update_layout(height=450, xaxis_title="5-Year Growth Rate (%)", yaxis_title="Average Household Income (USD $)", showlegend=False, **sleek_layout_updates)
    fig_demos.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#e5e7eb')

    st.plotly_chart(fig_demos, use_container_width=True)


# --- 6. DYNAMIC INSIGHTS ENGINE ---
st.subheader("💡 Strategic Insights & White Space")

premium_brands = filtered_brands[filtered_brands['Price'] > premium_threshold]
middle_brands = filtered_brands[(filtered_brands['Price'] > mass_threshold) & (filtered_brands['Price'] <= premium_threshold)]
mass_brands = filtered_brands[filtered_brands['Price'] <= mass_threshold]

middle_share = middle_brands['Share'].sum() if not middle_brands.empty else 0
mass_share = mass_brands['Share'].sum() if not mass_brands.empty else 0

st.info(f"""
* **The "Masstige" White Space (Green Zone):** While the **Millennial** demographic commands significant purchasing power (Avg. ${filtered_demos.loc[filtered_demos['Generation']=='Millennials', 'Avg_Income'].values[0]:,.0f}), the brand landscape shows a potential gap. Brands currently playing in this mid-to-premium tier capture roughly {middle_share}% of the market, compared to the {mass_share}% captured by mass brands. This indicates high-margin white space for a brand looking to elevate out of the mass tier or create an accessible diffusion line from the ultra-premium tier.
* **Volume Defense (Blue Zone):** **{market_leader['Brand']}** relies on the high-growth **Gen Z** and price-conscious segments. As Gen Z ages into the Millennial income brackets, {market_leader['Brand']} must innovate upward (premiumization) or risk losing them to mid-tier competitors. 
* **Targeting Peak Wealth (Yellow Zone):** **{highest_earner['Generation']}** has the highest spending power but slower population growth. Brands in this ultra-premium space ({', '.join(premium_brands['Brand'].tolist()[:3]) if not premium_brands.empty else 'luxury players'}) are competing intensely for a shrinking, but highly lucrative, slice of the pie.
""")
