import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.text_cleaner import clean_text
from analysis.skill_extractor import extract_skills
from analysis.role_analyzer import detect_experience_level
from generation.insight_generator import get_generator
from data.data_manager import load_data, save_data

# Set page config
st.set_page_config(
    page_title="AI Job Description Analyzer",
    page_icon="💼",
    layout="wide"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4b6cb7;
        color: white;
        font-weight: bold;
    }
    .skill-badge {
        display: inline-block;
        padding: 5px 12px;
        background-color: #e3f2fd;
        color: #1565c0;
        border-radius: 15px;
        margin: 5px;
        font-size: 0.9em;
        font-weight: 500;
    }
    .exp-junior { color: #2e7d32; font-weight: bold; }
    .exp-mid { color: #f57c00; font-weight: bold; }
    .exp-senior { color: #c62828; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Load AI model
@st.cache_resource
def load_ai():
    return get_generator()

ai_model = load_ai()

# Sidebar Navigation
st.sidebar.title("🚀 AI JD Analyzer")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Job Analysis", "Insights Dashboard", "History"])

if page == "Job Analysis":
    st.title("📄 Job Description Analysis")
    st.markdown("Paste a job description below to extract skills, experience levels, and generate AI insights.")
    
    jd_input = st.text_area("Job Description", height=300, placeholder="Enter job description here...")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Analyze Job Description"):
            if not jd_input.strip():
                st.error("Please provide a job description.")
            else:
                with st.spinner("Processing with AI..."):
                    # 1. Clean
                    cleaned_jd = clean_text(jd_input)
                    
                    # 2. Extract Skills
                    skills = extract_skills(cleaned_jd)
                    
                    # 3. Detect Experience
                    exp_level = detect_experience_level(cleaned_jd)
                    
                    # 4. Generate AI Insight
                    insight = ai_model.generate_insight(cleaned_jd, skills, exp_level)
                    
                    # 5. Save
                    result = {
                        "original_text": jd_input,
                        "cleaned_text": cleaned_jd,
                        "skills": skills,
                        "experience_level": exp_level,
                        "insight": insight
                    }
                    save_data(result)
                    
                    st.success("Analysis Complete!")
                    
                    # Display Results
                    st.markdown("---")
                    res_col1, res_col2 = st.columns(2)
                    
                    with res_col1:
                        st.subheader("🛠 Technical Skills")
                        if skills['technical_skills']:
                            skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in skills['technical_skills']])
                            st.markdown(skills_html, unsafe_allow_html=True)
                        else:
                            st.info("No specific technical skills detected.")
                            
                        st.subheader("🤝 Soft Skills")
                        if skills['soft_skills']:
                            skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in skills['soft_skills']])
                            st.markdown(skills_html, unsafe_allow_html=True)
                        else:
                            st.info("No specific soft skills detected.")
                            
                    with res_col2:
                        st.subheader("📊 Experience Level")
                        color_class = {
                            "Junior": "exp-junior",
                            "Mid-level": "exp-mid",
                            "Senior": "exp-senior"
                        }.get(exp_level, "exp-mid")
                        st.markdown(f'<p class="{color_class}" style="font-size: 1.5em;">{exp_level}</p>', unsafe_allow_html=True)
                        
                        st.subheader("💡 AI Generated Insight")
                        st.info(insight)

elif page == "Insights Dashboard":
    st.title("📈 Analytics Dashboard")
    history = load_data()
    
    if not history:
        st.warning("No data found. Please analyze some job descriptions first.")
    else:
        df = pd.DataFrame(history)
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Jobs Analyzed", len(df))
        m2.metric("Unique Tech Skills", len(set([s for row in df['skills'] for s in row['technical_skills']])))
        m3.metric("Senior Roles identified", len(df[df['experience_level'] == 'Senior']))
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        # Chart 1: Experience Level Distribution
        with col1:
            st.subheader("Experience Level Breakdown")
            exp_counts = df['experience_level'].value_counts().reset_index()
            exp_counts.columns = ['Level', 'Count']
            fig1 = px.pie(exp_counts, values='Count', names='Level', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig1, use_container_width=True)
            
        # Chart 2: Top Skills Distribution
        with col2:
            st.subheader("Top Technical Skills")
            all_tech_skills = [s for row in df['skills'] for s in row['technical_skills']]
            if all_tech_skills:
                skill_df = pd.Series(all_tech_skills).value_counts().reset_index()
                skill_df.columns = ['Skill', 'Frequency']
                fig2 = px.bar(skill_df.head(10), x='Frequency', y='Skill', orientation='h',
                             color='Frequency', color_continuous_scale='Viridis')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No technical skills detected yet.")

elif page == "History":
    st.title("📜 Analysis History")
    history = load_data()
    
    if not history:
        st.warning("No history found.")
    else:
        # Search and Filter
        search_query = st.text_input("🔍 Search job titles, skills or insights...", "")
        
        # Sort history: newest first
        history.reverse()
        
        for item in history:
            text_to_search = f"{item['original_text']} {item['insight']} {' '.join(item['skills']['technical_skills'])}".lower()
            if search_query.lower() in text_to_search:
                with st.expander(f"Analysis #{item['id']} - {item['experience_level']} role - {item['timestamp'][:10]}"):
                    st.markdown(f"**Experience Level:** `{item['experience_level']}`")
                    st.markdown(f"**Insight:** {item['insight']}")
                    
                    t_col, s_col = st.columns(2)
                    with t_col:
                        st.write("**Tech Skills:**")
                        st.write(", ".join(item['skills']['technical_skills']) if item['skills']['technical_skills'] else "None")
                    with s_col:
                        st.write("**Soft Skills:**")
                        st.write(", ".join(item['skills']['soft_skills']) if item['skills']['soft_skills'] else "None")
                    
                    st.markdown("**Original Text:**")
                    st.text(item['original_text'][:1000] + ("..." if len(item['original_text']) > 1000 else ""))
