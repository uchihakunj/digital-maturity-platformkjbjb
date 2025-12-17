import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import database
import logic
import os
from fpdf import FPDF

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital Maturity Platform", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. SESSION STATE MANAGEMENT ---
if 'page_selection' not in st.session_state:
    st.session_state['page_selection'] = 'Home'

def set_page_selection(page_name):
    st.session_state.page_selection = page_name

# --- 3. HELPER FUNCTION: PDF GENERATION ---
def create_pdf(department, scores, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, f"Digital Maturity Report: {department}", ln=True, align="C")
    pdf.ln(5)
    
    # Section 1: Scores
    pdf.set_font("Arial", "B", 14)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, "1. Assessment Scores (Weighted Model)", ln=True, fill=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 12)
    for category, score in scores.items():
        pdf.cell(100, 10, f"{category}: {score} / 5.0", ln=True)
    
    pdf.ln(10)
    
    # Section 2: Strategic Roadmap
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. Strategic Roadmap & Recommendations", ln=True, fill=True)
    pdf.ln(5)
    
    for category, rec in recommendations.items():
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 102, 204) # Blue header
        pdf.cell(0, 8, category, ln=True)
        
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0) # Black text
        pdf.multi_cell(0, 6, f"- {rec}")
        pdf.ln(3)
        
    return pdf.output(dest="S").encode("latin-1")

# --- 4. SIDEBAR NAVIGATION ---
if os.path.exists("logo.svg"):
    st.sidebar.image("logo.svg", width=180)

st.sidebar.title("Navigation")
dark_mode = st.sidebar.toggle("Dark Mode", value=True) 

# Navigation Widget
page = st.sidebar.radio(
    "Go to", 
    ["Home", "Assessment", "Upload Data", "Dashboard", "Roadmap", "Contact"],
    key="page_selection" 
)

# --- 5. CSS STYLING ---
chart_template = "plotly_dark" if dark_mode else "plotly_white"
text_color = "white" if dark_mode else "black"

# Define colors
bg_gradient_dark = "linear-gradient(-45deg, #020617, #1e1b4b, #172554, #0f172a)"
bg_gradient_light = "linear-gradient(-45deg, #ffffff, #f8fafc, #f1f5f9, #e2e8f0)"
card_bg_dark = "rgba(30, 41, 59, 0.8)"
card_bg_light = "#ffffff"
text_color_dark = "#ffffff"
text_color_light = "#0f172a"

# Dynamic Component Colors
comp_bg = "#1e293b" if dark_mode else "#ffffff"
comp_border = "#475569" if dark_mode else "#cbd5e1"
comp_text = "white" if dark_mode else "#0f172a"
comp_hover_bg = "#334155" if dark_mode else "#f1f5f9"
comp_primary = "#3B82F6" # Blue stays same

st.markdown(f"""
<style>
    /* GLOBAL: Main Container */
    [data-testid="stAppViewContainer"] {{
        background: {bg_gradient_dark if dark_mode else bg_gradient_light};
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: {text_color_dark if dark_mode else text_color_light};
    }}
    
    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* HEADER: Clean & Transparent */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
        backdrop-filter: none !important;
    }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{
        background-color: {'#0f172a' if dark_mode else '#ffffff'};
        border-right: 1px solid {'#334155' if dark_mode else '#e2e8f0'};
    }}
    
    /* GLOBAL TEXT VISIBILITY */
    h1, h2, h3, h4, h5, h6, p, li, span, label, 
    .stMarkdown, [data-testid="stCaptionContainer"], [data-testid="stWidgetLabel"] {{
        color: {text_color_dark if dark_mode else text_color_light} !important;
    }}
    
    /* METRICS FIX */
    [data-testid="stMetricValue"] {{
        color: #22d3ee !important; 
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {text_color_dark if dark_mode else text_color_light} !important;
        font-size: 1rem !important;
        opacity: 0.9;
    }}
    
    /* INPUTS */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stNumberInput > div > div > input {{
        background-color: {'#0f172a' if dark_mode else '#ffffff'} !important; 
        color: {text_color_dark if dark_mode else text_color_light} !important;
        border: 1px solid {'#475569' if dark_mode else '#cbd5e1'} !important;
        border-radius: 6px;
    }}
    
    /* --- FIX: MULTISELECT & SELECTBOX DROPDOWN (AGGRESSIVE) --- */
    /* 1. The Container Box (Added .stSelectbox for Roadmap page) */
    .stMultiSelect div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: {comp_bg} !important;
        border-color: {comp_border} !important;
        color: {comp_text} !important;
    }}
    
    /* 2. The Dropdown Menu (The White Box Issue) */
    div[data-baseweb="popover"] {{
        background-color: {comp_bg} !important;
        border: 1px solid {comp_border} !important;
    }}
    
    /* 3. The Menu Container inside Popover */
    div[data-baseweb="menu"] {{
        background-color: {comp_bg} !important;
    }}
    
    /* 4. The Options in the list */
    li[data-baseweb="option"] {{
        background-color: {comp_bg} !important;
        color: {comp_text} !important;
    }}
    
    /* 5. Highlighted Option (Hover State) */
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {{
        background-color: {comp_hover_bg} !important;
        color: {comp_primary} !important;
    }}
    
    /* 6. The Selected Tags (e.g., "IT Services") */
    span[data-baseweb="tag"] {{
        background-color: {comp_primary} !important;
        color: white !important;
    }}
    
    /* --- FIX: FILE UPLOADER (Drag & Drop Box) --- */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: {comp_bg} !important;
        border: 1px dashed {comp_primary} !important;
        color: {comp_text} !important;
    }}
    [data-testid="stFileUploaderDropzone"] div {{
        color: {comp_text} !important;
    }}
    [data-testid="stFileUploaderDropzone"] small {{
        color: {text_color} !important; /* Use existing text_color variable for subtlety */
    }}
    [data-testid="stFileUploaderDropzone"] button {{
       background-color: {comp_primary} !important;
       color: white !important;
       border: none !important;
    }}
    
    /* --- FIX: EXPANDERS (Maturity Dimensions) --- */
    div[data-testid="stExpander"] {{
        background-color: {comp_bg} !important;
        border: 1px solid {comp_border} !important;
        border-radius: 8px !important;
        color: {comp_text} !important;
    }}
    div[data-testid="stExpander"] details summary {{
        background-color: {comp_bg} !important;
        color: {comp_text} !important; 
        border-radius: 8px;
    }}
    div[data-testid="stExpander"] details div {{
        color: {comp_text} !important;
    }}
    div[data-testid="stExpander"] svg {{
        fill: {comp_text} !important;
    }}

    /* BUTTONS */
    div[data-testid="stButton"] > button, 
    div[data-testid="stFormSubmitButton"] > button {{
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }}

    /* CARDS */
    .prof-card {{
        background: {card_bg_dark if dark_mode else card_bg_light};
        border: 1px solid {'#475569' if dark_mode else '#e2e8f0'};
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
    }}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Digital Maturity Assessment Tool v7.4")

# --- 6. PAGE LOGIC ---

# ----------------- HOME PAGE -----------------
if page == "Home":
    st.markdown("<br>", unsafe_allow_html=True)
    col_hero_1, col_hero_2 = st.columns([1.5, 1])
    
    with col_hero_1:
        st.title("Digital Maturity Platform")
        st.markdown("### Enterprise Analytics Hub")
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); padding: 20px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-top: 10px;'>
            <p style='margin:0; font-size: 1.05rem; color: inherit;'>
            Benchmark, visualize, and optimize your organization's digital readiness. 
            This platform provides a centralized view of your strategic alignment across key technical and cultural dimensions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("Start New Assessment", use_container_width=True, on_click=set_page_selection, args=("Assessment",))
        c2.button("View Live Dashboard", type="secondary", use_container_width=True, on_click=set_page_selection, args=("Dashboard",))

    with col_hero_2:
        if os.path.exists("tech_image.png"):
            st.image("tech_image.png", use_container_width=True)
        else:
            st.image("https://cdn.pixabay.com/photo/2018/03/29/21/51/concept-3273322_1280.png", use_container_width=True)
    
    st.markdown("---")
    st.subheader("Core Capabilities")
    col1, col2 = st.columns(2)
    col1.markdown('<div class="prof-card"><h4 style="color: #3B82F6;">Assessment Engine</h4><p>Evaluate departments on five critical dimensions: Tech Stack, Culture, Process, Skills, and Risk.</p></div>', unsafe_allow_html=True)
    col1.write("")
    col1.markdown('<div class="prof-card"><h4 style="color: #3B82F6;">Interactive Dashboard</h4><p>Visualize performance metrics through dynamic Heatmaps and Radar Charts.</p></div>', unsafe_allow_html=True)
    col2.markdown('<div class="prof-card"><h4 style="color: #3B82F6;">Bulk Data Integration</h4><p>Seamlessly ingest enterprise data via CSV uploads.</p></div>', unsafe_allow_html=True)
    col2.write("")
    col2.markdown('<div class="prof-card"><h4 style="color: #3B82F6;">Strategic Roadmap</h4><p>Generate tailored, rule-based recommendations based on specific maturity scores.</p></div>', unsafe_allow_html=True)

# ----------------- ASSESSMENT PAGE -----------------
elif page == "Assessment":
    st.title("Comprehensive Assessment")
    st.markdown("Evaluate your department across key dimensions.")
    with st.form("assessment_form"):
        col_main_1, col_main_2 = st.columns([1, 2])
        with col_main_1:
            st.subheader("Department Info")
            dept = st.text_input("Department Name", placeholder="e.g. Finance")
            assessor = st.text_input("Assessor Name", placeholder="Optional")
        with col_main_2:
            st.subheader("Maturity Dimensions")
            with st.expander("Technological Maturity", expanded=True): tech = st.slider("Tech Stack Modernization", 1.0, 5.0, 3.0, 0.1)
            with st.expander("Cultural Readiness"): culture = st.slider("Innovation Culture", 1.0, 5.0, 3.0, 0.1)
            with st.expander("Process & Operations"): process = st.slider("Process Automation", 1.0, 5.0, 3.0, 0.1)
            with st.expander("Workforce Skills"): skills = st.slider("Talent & Skills", 1.0, 5.0, 3.0, 0.1)
            with st.expander("Risk & Compliance"): risk = st.slider("Risk Management", 1.0, 5.0, 3.0, 0.1)
        st.markdown("---")
        notes = st.text_area("Additional Notes / Context")
        if st.form_submit_button("Submit Assessment"):
            if dept:
                database.save_assessment(dept, tech, culture, process, skills, risk)
                st.toast("Assessment saved successfully!")
            else:
                st.error("Please enter a Department Name.")

# ----------------- UPLOAD PAGE -----------------
elif page == "Upload Data":
    st.title("Upload Enterprise Data")
    st.markdown("Upload a CSV file with columns: `Department`, `Tech`, `Culture`, `Process`, `Skills`, `Risk`")
    col_up, col_reset = st.columns([3, 1])
    uploaded_file = col_up.file_uploader("Choose a CSV file", type="csv")
    if col_reset.button("Clear Previous Data", type="secondary"):
        database.clear_data()
        st.rerun()
    
    if uploaded_file is not None:
        st.success(f"Selected File: {uploaded_file.name}")
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = ['Department', 'Tech', 'Culture', 'Process', 'Skills', 'Risk']
            if all(col in df.columns for col in required_cols):
                st.write("Preview:", df.head())
                if st.button("Import Data to Database"):
                    for _, row in df.iterrows():
                        database.save_assessment(row['Department'], row['Tech'], row['Culture'], row['Process'], row['Skills'], row['Risk'])
                    st.success(f"Successfully imported {len(df)} rows!")
                    st.rerun()
            else:
                st.error(f"CSV must contain strictly these columns: {required_cols}")
        except Exception as e:
            st.error(f"Error processing file: {e}")

# ----------------- DASHBOARD PAGE -----------------
elif page == "Dashboard":
    st.title("Maturity Dashboard")
    df = database.load_data()
    
    if not df.empty:
        df['Maturity Index'] = df.apply(logic.calculate_maturity_index, axis=1)
        
        def get_label(score):
            if score >= 4.0: return "Advanced"
            elif score >= 3.0: return "Established"
            elif score >= 2.0: return "Developing"
            else: return "Nascent"
            
        df['Maturity Label'] = df['Maturity Index'].apply(get_label)
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Assessments", len(df))
        kpi2.metric("Avg Maturity Index", f"{df['Maturity Index'].mean():.2f}")
        top_dept_idx = df['Maturity Index'].idxmax()
        kpi3.metric("Top Department", df.loc[top_dept_idx]['department'])
        
        st.markdown("---")
        
        col_dist, col_table = st.columns([1.3, 1])
        with col_dist:
            st.subheader("Distribution by Maturity Level")
            label_order = ["Advanced", "Established", "Developing", "Nascent"]
            dist_counts = df['Maturity Label'].value_counts().reindex(label_order, fill_value=0)
            
            fig_dist = go.Figure(data=[go.Bar(
                x=dist_counts.index, 
                y=dist_counts.values,
                text=dist_counts.values,
                textposition='auto',
                marker_color=['#00CC96', '#3B82F6', '#FFA15A', '#EF553B']
            )])
            fig_dist.update_layout(template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=text_color), margin=dict(l=20, r=20, t=30, b=20), height=350, xaxis_title="Maturity Status", yaxis_title="Count")
            st.plotly_chart(fig_dist, use_container_width=True, theme=None)

        with col_table:
            st.subheader("Overall Rankings")
            c_sort, c_slider = st.columns([1, 1])
            sort_order = c_sort.radio("View:", ["Top Performers", "Needs Attention"], label_visibility="collapsed", horizontal=True)
            top_n = c_slider.slider("Count", 3, 15, 5)
            
            if sort_order == "Top Performers":
                ranked_df = df.sort_values(by='Maturity Index', ascending=False).reset_index(drop=True)
            else:
                ranked_df = df.sort_values(by='Maturity Index', ascending=True).reset_index(drop=True)
            
            ranked_df.insert(0, 'Rank', ranked_df.index + 1)
            st.dataframe(ranked_df.head(top_n)[['Rank', 'department', 'Maturity Index', 'Maturity Label']], use_container_width=True, hide_index=True, column_config={"Rank": st.column_config.NumberColumn("Rank", format="%d"), "department": "Department", "Maturity Label": "Status", "Maturity Index": st.column_config.ProgressColumn("Score", help="Overall Maturity Score", format="%.2f", min_value=0, max_value=5)})

        st.markdown("---")
        
        st.markdown("### Deep Dive Analysis")
        heatmap_data = df[['department', 'tech_score', 'culture_score', 'process_score', 'skills_score', 'risk_score']].set_index('department')
        dynamic_height = max(300, len(heatmap_data) * 35)
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=heatmap_data.values, x=['Tech', 'Culture', 'Process', 'Skills', 'Risk'], y=heatmap_data.index,
            colorscale='Viridis',
            text=heatmap_data.values, texttemplate="%{text:.1f}", 
            textfont={"size": 12, "color": "white" if dark_mode else "black"}, zmin=1, zmax=5,
            colorbar=dict(title="Weighted Score")
        ))
        fig_heat.update_layout(title="Dimension Heatmap", template=chart_template, height=dynamic_height, yaxis=dict(autorange="reversed"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=text_color))
        st.plotly_chart(fig_heat, use_container_width=True, theme=None)
        
        st.markdown("##### Radar: Comparative Profiles ")
        dept_filter = st.multiselect("Select Departments", df['department'].unique(), default=df['department'].unique()[:2], label_visibility="collapsed")
        
        if dept_filter:
            filtered_df = df[df['department'].isin(dept_filter)]
            categories = ['Tech', 'Culture', 'Process', 'Skills', 'Risk']
            fig_radar = go.Figure()
            for i, row in filtered_df.iterrows():
                fig_radar.add_trace(go.Scatterpolar(r=[row['tech_score'], row['culture_score'], row['process_score'], row['skills_score'], row['risk_score']], theta=categories, fill='toself', name=row['department']))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5]), angularaxis=dict(tickfont=dict(size=14, color=text_color, family="Arial Black"))), 
                showlegend=True, template=chart_template, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color=text_color)
            )
            st.plotly_chart(fig_radar, use_container_width=True, theme=None)
    else:
        st.info("No data available.")

# ----------------- ROADMAP PAGE -----------------
elif page == "Roadmap":
    st.title("Transformation Roadmap")
    df = database.load_data()
    
    if not df.empty:
        selected_dept = st.selectbox("Select Department for Recommendations", df['department'].unique())
        
        if selected_dept:
            row = df[df['department'] == selected_dept].iloc[0]
            recs = logic.get_recommendations(row)
            scores = {'Technology': row['tech_score'], 'Process': row['process_score'], 'Culture': row['culture_score'], 'Skills': row['skills_score'], 'Risk': row['risk_score']}
            
            col_header, col_btn = st.columns([3, 1])
            with col_header:
                st.subheader(f"Strategy for {selected_dept}")
            with col_btn:
                pdf_data = create_pdf(selected_dept, scores, recs)
                st.download_button(label="Download PDF Report", data=pdf_data, file_name=f"{selected_dept}_Maturity_Report.pdf", mime="application/pdf", type="primary", use_container_width=True)
            
            c1, c2, c3, c4, c5 = st.columns(5)
            def show_card(col, title, score, rec):
                with col:
                    color = '#48BB78' if score > 4 else '#ECC94B' if score > 2.5 else '#F56565'
                    st.markdown(f"""<div class="prof-card" style="padding: 20px; border-left: 5px solid {color};"><h4 style="margin-top:0; color:{color} !important;">{title}</h4><div style="font-size: 1.2rem; font-weight:bold; color: {color}; margin-bottom: 10px;">Score: {score}</div><p style="font-size: 0.9rem; line-height: 1.4;">{rec}</p></div>""", unsafe_allow_html=True)

            show_card(c1, "Tech", row['tech_score'], recs.get('Tech'))
            show_card(c2, "Process", row['process_score'], recs.get('Process'))
            show_card(c3, "Culture", row['culture_score'], recs.get('Culture'))
            show_card(c4, "Skills", row['skills_score'], recs.get('Skills'))
            show_card(c5, "Risk", row['risk_score'], recs.get('Risk'))
    else:
        st.info("No data available.")

# ----------------- CONTACT PAGE -----------------
elif page == "Contact":
    st.title("Contact Us")
    st.markdown("""<div class="prof-card"><h3 style="color:#60A5FA !important; margin-bottom: 20px;">Get in Touch</h3><p><strong>Address:</strong> Bose House, IIIT NR</p><p><strong>Email:</strong> support@Team-9.com</p></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.text_input("Your Name"); c1.text_input("Your Email")
    c2.text_area("Message"); c2.button("Send Message")

# --- FOOTER (STATIC BOTTOM) ---
st.markdown("---")
st.markdown(f"""
<div style="width: 100%; text-align: center; padding: 20px; opacity: 0.8; color: {text_color_dark if dark_mode else text_color_light};">
    <p style="margin:0; font-weight: 500;">Copyright © 2025 by Team-9 | Digital Maturity Platform</p>
</div>
""", unsafe_allow_html=True)
