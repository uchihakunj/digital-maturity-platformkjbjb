import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import database
import logic
import os
import sqlite3
from fpdf import FPDF
import tempfile
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital Maturity Platform", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🖥️"
)

# --- 2. SESSION STATE MANAGEMENT ---
if 'page_selection' not in st.session_state:
    st.session_state['page_selection'] = 'Home'

def set_page_selection(page_name):
    """Callback to update page selection safely."""
    st.session_state.page_selection = page_name

# --- 3. SIDEBAR NAVIGATION ---
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

# --- 4. CSS STYLING ---
chart_template = "plotly_dark" if dark_mode else "plotly_white"
text_color = "white" if dark_mode else "black"

# Define colors
bg_gradient_dark = "linear-gradient(-45deg, #020617, #1e1b4b, #172554, #0f172a)"
bg_gradient_light = "linear-gradient(-45deg, #ffffff, #f8fafc, #f1f5f9, #e2e8f0)"
card_bg_dark = "rgba(30, 41, 59, 0.8)"
card_bg_light = "#ffffff"
text_color_dark = "#ffffff"
text_color_light = "#0f172a"

st.markdown(f"""
<style>
    /* GLOBAL: Main Container Background */
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

    /* HEADER: Transparent */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
        backdrop-filter: blur(5px);
    }}

    /* --- SIDEBAR VISIBILITY FIX --- */
    [data-testid="stSidebar"] {{
        background-color: {'#0f172a' if dark_mode else '#ffffff'};
        border-right: 1px solid {'#334155' if dark_mode else '#e2e8f0'};
    }}
    
    /* Sidebar Navigation Text */
    [data-testid="stSidebar"] [data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {{
        color: {text_color_dark if dark_mode else text_color_light} !important;
        font-size: 1rem;
        font-weight: 500;
    }}
    
    /* Sidebar Headers */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] label {{
        color: {text_color_dark if dark_mode else text_color_light} !important;
    }}

    /* --- GENERAL TEXT VISIBILITY --- */
    label, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
        color: {text_color_dark if dark_mode else text_color_light} !important;
    }}
    
    /* Slider Labels */
    div[data-testid="stWidgetLabel"] p {{
        color: {text_color_dark if dark_mode else text_color_light} !important;
        font-weight: 500;
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
    
    /* PLACEHOLDERS */
    ::placeholder {{ color: #94a3b8 !important; opacity: 1; }}

    /* BUTTONS */
    div[data-testid="stButton"] > button, 
    div[data-testid="stFormSubmitButton"] > button {{
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }}
    div[data-testid="stButton"] > button:hover, 
    div[data-testid="stFormSubmitButton"] > button:hover {{
        transform: translateY(-2px);
    }}

    /* SECONDARY BUTTONS */
    button[kind="secondary"] {{
        background-color: transparent !important;
        border: 1px solid #ef4444 !important; 
        color: #ef4444 !important; 
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

    /* METRICS */
    [data-testid="stMetricValue"] {{ color: #22d3ee !important; }}
    div[data-testid="stMetric"] {{
        background-color: {'rgba(15, 23, 42, 0.6)' if dark_mode else '#ffffff'};
        border: 1px solid {'#334155' if dark_mode else '#e2e8f0'};
        border-radius: 8px;
    }}

    /* EXPANDER HEADERS */
    .streamlit-expanderHeader, 
    div[data-testid="stExpander"] details summary {{
        background-color: {'#1e293b' if dark_mode else '#f8fafc'} !important;
        color: {text_color_dark if dark_mode else text_color_light} !important; 
        border: 1px solid {'#475569' if dark_mode else '#e2e8f0'};
        border-radius: 6px;
    }}
    
    .streamlit-expanderHeader p, 
    div[data-testid="stExpander"] details summary p {{
        color: inherit !important;
        font-weight: 600;
    }}
    
    div[data-testid="stExpander"] details summary svg {{
        fill: {text_color_dark if dark_mode else text_color_light} !important;
    }}
    
    /* UPLOAD BUTTON */
    [data-testid="stFileUploaderDropzone"] button {{
       background-color: #3B82F6 !important;
       color: white !important;
       border: none !important;
    }}

</style>
""", unsafe_allow_html=True)

# Footer Injection
st.markdown("""
<div style="position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; opacity: 0.7; color: #94a3b8; pointer-events: none;">
    <p>Copyright © 2025 by Team-9 | Digital Maturity Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Digital Maturity Assessment Tool v5.5")

# --- 5. PAGE LOGIC ---

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
        with c1:
            st.button(
                "Start New Assessment", 
                use_container_width=True,
                on_click=set_page_selection,
                args=("Assessment",)
            )
        with c2:
            st.button(
                "View Live Dashboard", 
                type="secondary", 
                use_container_width=True,
                on_click=set_page_selection,
                args=("Dashboard",)
            )

    with col_hero_2:
        if os.path.exists("tech_image.png"):
            st.image("tech_image.png", use_container_width=True)
        elif os.path.exists("tech.png.jpg"):
             st.image("tech.png.jpg", use_container_width=True)
        else:
            st.image("https://cdn.pixabay.com/photo/2018/03/29/21/51/concept-3273322_1280.png", use_container_width=True)
    
    st.markdown("---")
    st.subheader("Core Capabilities")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="prof-card">
            <h4 style="color: #3B82F6;">Assessment Engine</h4>
            <p>Evaluate departments on five critical dimensions: Tech Stack, Culture, Process, Skills, and Risk. 
            Utilize granular scoring for precise gap analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("") 
        st.markdown(f"""
        <div class="prof-card">
            <h4 style="color: #3B82F6;">Interactive Dashboard</h4>
            <p>Visualize performance metrics through dynamic Heatmaps and Radar Charts. 
            Identify high-performing units and strategic bottlenecks instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="prof-card">
            <h4 style="color: #3B82F6;">Bulk Data Integration</h4>
            <p>Seamlessly ingest enterprise data via CSV uploads. 
            The system automatically aggregates, validates, and visualizes large datasets in real-time.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("") 
        st.markdown(f"""
        <div class="prof-card">
            <h4 style="color: #3B82F6;">Strategic Roadmap</h4>
            <p>Generate tailored, rule-based recommendations based on specific maturity scores. 
            Transition from foundational capabilities to optimized leadership.</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- ASSESSMENT PAGE -----------------
elif page == "Assessment":
    st.title("Comprehensive Assessment")
    st.markdown("Evaluate your department across key dimensions. Please provide detailed scoring.")
    
    with st.form("assessment_form"):
        col_main_1, col_main_2 = st.columns([1, 2])
        
        with col_main_1:
            st.subheader("Department Info")
            dept = st.text_input("Department Name", placeholder="e.g. Finance")
            assessor = st.text_input("Assessor Name", placeholder="Optional")
        
        with col_main_2:
            st.subheader("Maturity Dimensions")
            
            with st.expander("Technological Maturity", expanded=True):
                tech = st.slider("Tech Stack Modernization", 1.0, 5.0, 3.0, 0.1, help="1=Legacy, 5=Cutting Edge")
            
            with st.expander("Cultural Readiness"):
                culture = st.slider("Innovation Culture", 1.0, 5.0, 3.0, 0.1, help="1=Resistant, 5=Agile")
                
            with st.expander("Process & Operations"):
                process = st.slider("Process Automation", 1.0, 5.0, 3.0, 0.1, help="1=Manual, 5=Autonomous")
            
            with st.expander("Workforce Skills"):
                skills = st.slider("Talent & Skills", 1.0, 5.0, 3.0, 0.1, help="1=Gap, 5=Expertise")
                
            with st.expander("Risk & Compliance"):
                risk = st.slider("Risk Management", 1.0, 5.0, 3.0, 0.1, help="1=High Risk, 5=Secure")
            
        st.markdown("---")
        notes = st.text_area("Additional Notes / Context")
            
        submitted = st.form_submit_button("Submit Assessment")
        
        if submitted:
            if dept:
                database.save_assessment(dept, tech, culture, process, skills, risk)
                st.toast("Assessment saved successfully!", icon="✅")
            else:
                st.error("Please enter a Department Name.")

# ----------------- CONTACT PAGE -----------------
elif page == "Contact":
    st.title("Contact Us")
    st.markdown("We'd love to hear from you. Reach out for support or enterprise consultancy.")
    
    st.markdown("""
    <div class="prof-card">
        <h3 style="color:#60A5FA !important; margin-bottom: 20px;">Get in Touch</h3>
        <p><strong>Address:</strong> Bose House, IIIT NR</p>
        <p><strong>Email:</strong> support@Team-9.com</p>
        <p><strong>Phone:</strong> +1 (555) 123-4567</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Your Name")
        st.text_input("Your Email")
    with c2:
        st.text_area("Message")
        st.button("Send Message")

# ----------------- UPLOAD PAGE -----------------
elif page == "Upload Data":
    st.title("Upload Enterprise Data")
    st.markdown("Upload a CSV file with columns: `Department`, `Tech`, `Culture`, `Process`, `Skills`, `Risk`")
    
    col_up, col_reset = st.columns([3, 1])
    with col_up:
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    with col_reset:
        st.write("") 
        st.write("") 
        if st.button("Clear Previous Data", type="secondary", help="Deletes all existing records from the database"):
            try:
                database.clear_data()
                st.toast("Database cleared successfully!", icon="🗑️")
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing data: {e}")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = ['Department', 'Tech', 'Culture', 'Process', 'Skills', 'Risk']
            if all(col in df.columns for col in required_cols):
                st.write("Preview:", df.head())
                if st.button("Import Data to Database"):
                    for _, row in df.iterrows():
                        database.save_assessment(
                            row['Department'], row['Tech'], row['Culture'], 
                            row['Process'], row['Skills'], row['Risk']
                        )
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
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Assessments", len(df))
        kpi2.metric("Avg Maturity Index", f"{df['Maturity Index'].mean():.2f}")
        
        top_dept_idx = df['Maturity Index'].idxmax()
        top_dept_name = df.loc[top_dept_idx]['department']
        kpi3.metric("Top Department", top_dept_name)
        
        st.markdown("### Organizational Heatmap")
        
        heatmap_data = df[['department', 'tech_score', 'culture_score', 'process_score', 'skills_score', 'risk_score']].set_index('department')
        dynamic_height = max(250, len(heatmap_data) * 15) # Adjusted height
        
        # --- FIXED HEATMAP COLORSCALE (PLASMA for Contrast) ---
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=['Tech', 'Culture', 'Process', 'Skills', 'Risk'],
            y=heatmap_data.index,
            colorscale='Plasma', 
            text=heatmap_data.values,
            texttemplate="%{text:.1f}", 
            textfont={"size": 10, "color": "white" if dark_mode else "black"},
            zmin=1, zmax=5,
            xgap=3, ygap=3
        ))
        
        fig.update_layout(
            title="Maturity Heatmap", 
            template=chart_template,
            height=dynamic_height,
            xaxis_title="", yaxis_title="",
            yaxis=dict(autorange="reversed"),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',  
            font=dict(color=text_color),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)
        
        st.markdown("### Compare Departments")
        dept_filter = st.multiselect("Select Departments", df['department'].unique(), default=df['department'].unique()[:2])
        
        if dept_filter:
            filtered_df = df[df['department'].isin(dept_filter)]
            categories = ['Tech', 'Culture', 'Process', 'Skills', 'Risk']
            fig_radar = go.Figure()

            for i, row in filtered_df.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[row['tech_score'], row['culture_score'], row['process_score'], row['skills_score'], row['risk_score']],
                    theta=categories,
                    fill='toself',
                    name=row['department']
                ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 4]),
                    bgcolor='rgba(0,0,0,0)' 
                ),
                showlegend=True,
                title="Maturity Radar",
                template=chart_template,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=text_color)
            )
            st.plotly_chart(fig_radar, use_container_width=True, theme=None)
    else:
        st.info("No data available. Please complete an assessment or upload data.")

# ----------------- ROADMAP PAGE -----------------
elif page == "Roadmap":
    st.title("Transformation Roadmap")
    df = database.load_data()
    
    # PDF Generator Function
    def generate_pdf(dept, row, recs, all_df):
        pdf = FPDF()
        
        # --- Page 1: Heatmap & Overview ---
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 10, 'Digital Maturity Report', ln=True, align='C')
        pdf.set_font('Arial', 'I', 12)
        pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d")}', ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Organizational Heatmap', ln=True)
        
        # Generate Global Heatmap for PDF
        try:
            heatmap_data = all_df[['department', 'tech_score', 'culture_score', 'process_score', 'skills_score', 'risk_score']].set_index('department')
            fig_hm = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=['Tech', 'Culture', 'Process', 'Skills', 'Risk'],
                y=heatmap_data.index,
                colorscale='Plasma',
                zmin=1, zmax=5
            ))
            fig_hm.update_layout(
                width=800, height=500,
                yaxis=dict(autorange="reversed")
            )
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_hm:
                fig_hm.write_image(tmp_hm.name)
                pdf.image(tmp_hm.name, x=10, y=50, w=190)
                
        except Exception as e:
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 10, f"Heatmap generation failed: {e}", ln=True)
        
        # --- Page 2: Specific Roadmap ---
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Transformation Roadmap: {dept}', ln=True)
        pdf.ln(5)
        
        # Scores Table
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Dimension', 1)
        pdf.cell(30, 10, 'Score', 1)
        pdf.cell(120, 10, 'Recommendation Summary', 1, ln=True)
        
        pdf.set_font('Arial', '', 11)
        
        # Dimensions Data
        dims = {
            'Tech': (row['tech_score'], recs.get('Tech', '')),
            'Process': (row['process_score'], recs.get('Process', '')),
            'Culture': (row['culture_score'], recs.get('Culture', '')),
            'Skills': (row['skills_score'], recs.get('Skills', '')),
            'Risk': (row['risk_score'], recs.get('Risk', ''))
        }
        
        for dim, (score, txt) in dims.items():
            pdf.cell(40, 10, dim, 1)
            pdf.cell(30, 10, str(score), 1)
            # Truncate text for table row
            short_text = (txt[:75] + '...') if len(txt) > 75 else txt
            pdf.cell(120, 10, short_text, 1, ln=True)
        
        pdf.ln(10)
        
        # Detailed Recommendations
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Detailed Recommendations', ln=True)
        pdf.set_font('Arial', '', 12)
        
        for dim, (score, txt) in dims.items():
            pdf.set_text_color(0, 50, 150) # Blue header
            pdf.cell(0, 8, f"{dim} (Current Score: {score})", ln=True)
            pdf.set_text_color(0, 0, 0) # Black text
            pdf.multi_cell(0, 6, txt)
            pdf.ln(4)

        return pdf.output(dest='S').encode('latin-1')

    if not df.empty:
        selected_dept = st.selectbox("Select Department for Recommendations", df['department'].unique())
        
        if selected_dept:
            row = df[df['department'] == selected_dept].iloc[0]
            recs = logic.get_recommendations(row)
            
            # --- Report Download Button ---
            c_head_1, c_head_2 = st.columns([3, 1])
            with c_head_1:
                st.subheader(f"Transformation Roadmap for {selected_dept}")
            with c_head_2:
                # Generate PDF button
                try:
                    pdf_bytes = generate_pdf(selected_dept, row, recs, df)
                    st.download_button(
                        label="📄 Download Report (PDF)",
                        data=pdf_bytes,
                        file_name=f"{selected_dept}_Maturity_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.warning("Install 'kaleido' to enable PDF charts: pip install kaleido")
            
            c1, c2, c3, c4, c5 = st.columns(5)
            
            def show_card(col, title, score, rec):
                with col:
                    color = '#48BB78' if score > 4 else '#ECC94B' if score > 2.5 else '#F56565'
                    
                    st.markdown(f"""
                    <div class="prof-card" style="padding: 20px; border-left: 5px solid {color};">
                        <h4 style="margin-top:0; color:{color} !important; -webkit-text-fill-color: {color};">{title}</h4>
                        <div style="font-size: 1.2rem; font-weight:bold; color: {color}; margin-bottom: 10px;">
                            Score: {score}
                        </div>
                        <p style="font-size: 0.9rem; line-height: 1.4;">{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)

            show_card(c1, "Tech", row['tech_score'], recs.get('Tech'))
            show_card(c2, "Process", row['process_score'], recs.get('Process'))
            show_card(c3, "Culture", row['culture_score'], recs.get('Culture'))
            show_card(c4, "Skills", row['skills_score'], recs.get('Skills'))
            show_card(c5, "Risk", row['risk_score'], recs.get('Risk'))
            
            st.markdown("---")
            st.caption("Auto-generated based on the Digital Maturity Scoring Engine.")
    else:
        st.info("No data available.")