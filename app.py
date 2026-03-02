import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Category Strategy Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- 2. MOCK DATA GENERATION ---
@st.cache_data
def load_data():
    # Brand Data: 6-8 brands per Country x Category combo.
    # Added Price_Min and Price_Max to simulate price variance for the box/whisker look.
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
        {"Country": "USA", "Generation": "Gen Z", "Pop_Split": 20, "Avg_Income": 35000, "Growth_Rate": 12.5, "Price_Target": "Mass / Entry"},
        {"Country": "USA", "Generation": "Millennials", "Pop_Split": 22, "Avg_Income": 85000, "Growth_Rate": 8.2, "Price_Target": "Premium"},
        {"Country": "USA", "Generation": "Gen X", "Pop_Split": 19, "Avg_Income": 110000, "Growth_Rate": 2.1, "Price_Target": "Ultra-Premium"},
        {"Country": "USA", "Generation": "Boomers", "Pop_Split": 21, "Avg_Income": 75000, "Growth_Rate": -3.5, "Price_Target": "Mid-Tier"},
        # UK
        {"Country": "UK", "Generation": "Gen Z", "Pop_Split": 19, "Avg_Income": 28000, "Growth_Rate": 11.0, "Price_Target": "Mass / Entry"},
        {"Country": "UK", "Generation": "Millennials", "Pop_Split": 22, "Avg_Income": 65000, "Growth_Rate": 7.5, "Price_Target": "Premium"},
        {"Country": "UK", "Generation": "Gen X", "Pop_Split": 20, "Avg_Income": 80000, "Growth_Rate": 1.5, "Price_Target": "Ultra-Premium"},
        {"Country": "UK", "Generation": "Boomers", "Pop_Split": 22, "Avg_Income": 55000, "Growth_Rate": -4.0, "Price_Target": "Mid-Tier"},
        # Germany
        {"Country": "Germany", "Generation": "Gen Z", "Pop_Split": 18, "Avg_Income": 30000, "Growth_Rate": 10.5, "Price_Target": "Mass / Entry"},
        {"Country": "Germany", "Generation": "Millennials", "Pop_Split": 20, "Avg_Income": 70000, "Growth_Rate": 6.8, "Price_Target": "Premium"},
        {"Country": "Germany", "Generation": "Gen X", "Pop_Split": 23, "Avg_Income": 90000, "Growth_Rate": 1.0, "Price_Target": "Ultra-Premium"},
        {"Country": "Germany", "Generation": "Boomers", "Pop_Split": 25, "Avg_Income": 60000, "Growth_Rate": -5.2, "Price_Target": "Mid-Tier"},
    ])

    return brand_data, demo_data

df_brands, df_demos = load_data()

# --- 3. MAIN DASHBOARD & TOP FILTERS ---
st.title("🎯 Category Strategy & Audience Dashboard")
st.markdown("Identify white space, track competitors, and target high-value cohorts.")

# Top-level filters (Moved from sidebar)
filter_col1, filter_col2 = st.columns(2)
selected_country = filter_col1.selectbox("🌐 Select Country", options=["USA", "UK", "Germany"])
selected_category = filter_col2.selectbox("🛍️ Select Category", options=["Shampoo", "Fragrances", "Moisturisers"])

st.divider()

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

st.write("")

# --- 5. CHARTS LAYOUT ---
col_left, col_right = st.columns((5, 4)) # 50/50 split roughly

with col_left:
    st.subheader("Where to Play: Brand Landscape")
    st.markdown("Price elasticity vs Market Share (Shaded areas indicate cohort targets)")
    
    # Square / Box-and-Whisker style Scatter Chart
    fig_brands = go.Figure()
    
    # Calculate target zones based on brand prices to map generations
    max_price = filtered_brands['Price_Max'].max()
    mass_threshold = filtered_brands['Price'].quantile(0.33)
    premium_threshold = filtered_brands['Price'].quantile(0.75)

    # Shaded Overlays for Demographics
    fig_brands.add_hrect(y0=0, y1=mass_threshold, line_width=0, fillcolor="rgba(173, 216, 230, 0.2)", annotation_text="Gen Z Target (Mass)", annotation_position="top right")
    fig_brands.add_hrect(y0=mass_threshold, y1=premium_threshold, line_width=0, fillcolor="rgba(144, 238, 144, 0.2)", annotation_text="Millennial Target (Premium)", annotation_position="top right")
    fig_brands.add_hrect(y0=premium_threshold, y1=max_price * 1.1, line_width=0, fillcolor="rgba(255, 182, 193, 0.2)", annotation_text="Gen X Target (Ultra-Premium)", annotation_position="top right")

    # Brand markers with error bars (representing price range)
    fig_brands.add_trace(go.Scatter(
        x=filtered_brands["Share"],
        y=filtered_brands["Price"],
        mode="markers+text",
        text=filtered_brands["Brand"],
        textposition="top center",
        marker=dict(symbol="square", size=14, color="royalblue", line=dict(width=2, color="darkblue")),
        error_y=dict(
            type='data',
            symmetric=False,
            array=filtered_brands["Price_Max"] - filtered_brands["Price"],
            arrayminus=filtered_brands["Price"] - filtered_brands["Price_Min"],
            color='gray',
            thickness=1.5,
            width=5
        ),
        name="Brands"
    ))

    fig_brands.update_layout(
        height=450,
        xaxis_title="Market Share (%)",
        yaxis_title="Average Price (USD $)",
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    st.plotly_chart(fig_brands, use_container_width=True)

with col_right:
    st.subheader("Who to Target: Cohort Matrix")
    st.markdown("Demographic deep-dive: Size, Wealth, and Momentum.")

    # Prepare data for Matrix Heatmap
    generations = filtered_demos['Generation'].tolist()
    
    # Standardize data column-wise to create a proper heatmap color scale, 
    # but display the raw text values inside the blocks.
    pop = filtered_demos['Pop_Split'].values
    inc = filtered_demos['Avg_Income'].values
    gro = filtered_demos['Growth_Rate'].values
    
    # Normalized Z-values for coloring (0 to 1 scaling per column)
    z_pop = (pop - pop.min()) / (pop.max() - pop.min())
    z_inc = (inc - inc.min()) / (inc.max() - inc.min())
    z_gro = (gro - gro.min()) / (gro.max() - gro.min())
    z_matrix = np.array([z_pop, z_inc, z_gro]).T  # Transpose to match rows/cols

    # Raw text values for display
    text_matrix = np.array([
        [f"{p}%", f"${i:,.0f}", f"{g}%"] 
        for p, i, g in zip(pop, inc, gro)
    ])

    fig_matrix = go.Figure(data=go.Heatmap(
        z=z_matrix,
        x=["Population Size", "Avg Income (USD)", "5-Yr Growth"],
        y=generations,
        text=text_matrix,
        texttemplate="%{text}",
        textfont={"size": 14, "color": "black"},
        colorscale="Blues",
        showscale=False,
        hoverinfo="skip"
    ))

    fig_matrix.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(side="bottom")
    )
    st.plotly_chart(fig_matrix, use_container_width=True)


# --- 6. DYNAMIC INSIGHTS ENGINE ---
st.subheader("💡 Strategic Insights & White Space")

# Calculate metrics for dynamic text
premium_brands = filtered_brands[filtered_brands['Price'] > premium_threshold]
mass_brands = filtered_brands[filtered_brands['Price'] <= mass_threshold]
premium_brand_names = ", ".join(premium_brands['Brand'].tolist()) if not premium_brands.empty else "None"

st.info(f"""
* **The Gen Z Pipeline (Mass/Entry):** **{fastest_growing['Generation']}** is driving the most aggressive growth (+{fastest_growing['Growth_Rate']}%) in the {selected_country} market. The primary players targeting their price-points (Under ${mass_threshold:.2f}) are brands like {mass_brands['Brand'].iloc[0] if not mass_brands.empty else 'mass brands'}. To secure long-term category loyalty, focus innovation on accessible price points with high perceived value.
* **The Premium White Space:** **{highest_earner['Generation']}** possesses the highest average income (${highest_earner['Avg_Income']:,.0f}). However, looking at the brand landscape, volume (Market Share) is heavily skewed toward the bottom half of the y-axis. Brands like {premium_brand_names} are currently capturing this demographic, but their lower market share suggests massive untapped potential for a "masstige" (mass-prestige) product line targeting this wealth density.
* **Competitive Stance for {market_leader['Brand']}:** As the market leader, {market_leader['Brand']} holds a strong defensive position in volume. To drive margin expansion without losing share, they should explore strategic cross-selling or sub-branding targeted directly at the upwardly mobile Millennials mapped in the green shaded territory.
""")
