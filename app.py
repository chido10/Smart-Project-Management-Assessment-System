from dotenv import load_dotenv # type: ignore
import os
import streamlit as st # type: ignore
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import google.generativeai as genai # type: ignore
import textwrap

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to handle API calls for different project aspects
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Define each function with prompts for each specific task
def estimate_cost(project_description):
    prompt = f"Provide a cost estimation for the following project: {project_description}"
    return get_gemini_response(prompt)

def assess_sustainability(project_description):
    prompt = f"Evaluate the sustainability and environmental impact of this project: {project_description}"
    return get_gemini_response(prompt)

def optimize_resources(project_description):
    prompt = f"Suggest an optimal allocation of resources (equipment, personnel, time) for this project: {project_description}"
    return get_gemini_response(prompt)

def manage_risks(project_description):
    prompt = f"Identify potential risks and suggest mitigation strategies for this project: {project_description}"
    return get_gemini_response(prompt)

def prioritize_tasks(project_description):
    prompt = f"List and prioritize critical tasks for the successful completion of this project: {project_description}"
    return get_gemini_response(prompt)

def optimize_schedule(project_description):
    prompt = f"Create an efficient timeline and schedule for this project: {project_description}"
    return get_gemini_response(prompt)

# Streamlit App Layout
st.set_page_config(page_title="Project Planning & Assessment Tool", layout="wide")

# Title with color and emojis
st.markdown("<h1 style='text-align: center; color: #ff6347;'>Project Planning & Assessment Tool 🎨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4682b4;'>by Ginikanwa Nnenna</h3>", unsafe_allow_html=True)
st.write("---")

# Sidebar for Task Selection with Colored Headers
st.sidebar.markdown("<h2 style='color: #4CAF50;'>Select Analysis Task</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #FF6347; font-size: 14px;'>Choose an analysis to perform on the project description:</p>", unsafe_allow_html=True)

# Define task options with associated colors
task_options = {
    "Cost Estimation": "#ff6347",
    "Sustainability Assessment": "#4682b4",
    "Resource Optimization": "#32cd32",
    "Risk Management": "#ff8c00",
    "Task Prioritization": "#8a2be2",
    "Schedule Optimization": "#ff1493",
}

# Initialize selected task in session state if not already set
if "selected_task" not in st.session_state:
    st.session_state["selected_task"] = None  # No task selected by default

# Display each task as an interactive button in the sidebar
for option, color in task_options.items():
    if st.sidebar.button(option):
        st.session_state["selected_task"] = option  # Update selected task in session state

# Retrieve the currently selected task
selected_task = st.session_state["selected_task"]

# Input Field for Project Description with placeholder behavior
if 'description_input' not in st.session_state:
    st.session_state['description_input'] = ""  # Initialize as empty

project_description = st.text_area("Enter Project Description", st.session_state['description_input'])

# Run All Analyses button beside the Project Description
st.write("")
if st.button("Run All Analyses"):
    st.session_state["selected_task"] = "Run All"

# Display current selected task only if a task is selected
if selected_task and selected_task != "Run All":
    st.write(f"## Current Task: {selected_task}")
elif not selected_task:
    st.write("## Please select a task from the sidebar.")

# Display tables and diagrams where appropriate
def display_sample_table():
    data = {
        'Category': ['Materials', 'Labor', 'Equipment', 'Software', 'Services', 'Travel'],
        'Cost Estimate ($)': [5000, 10000, 8000, 2000, 3000, 1500]
    }
    df = pd.DataFrame(data)
    st.table(df)

def display_sample_chart():
    data = {
        'Risk Factor': ['Financial', 'Operational', 'Compliance', 'Strategic'],
        'Likelihood (%)': [35, 20, 25, 20],
    }
    df = pd.DataFrame(data)
    fig, ax = plt.subplots()
    ax.bar(df['Risk Factor'], df['Likelihood (%)'], color='#ff8c00')
    ax.set_title("Risk Factor Likelihood")
    st.pyplot(fig)

# Only show results if project description is provided
if project_description.strip():
    st.write("### Task Result")
    
    # Display selected task result if it's not "Run All"
    if selected_task and selected_task != "Run All":
        if selected_task == "Cost Estimation":
            st.markdown(f"<h4 style='color: {task_options[selected_task]};'>Cost Estimation Result 💸</h4>", unsafe_allow_html=True)
            st.write(estimate_cost(project_description))
            display_sample_table()  # Show a sample table for cost estimation
        
        elif selected_task == "Sustainability Assessment":
            st.markdown(f"<h4 style='color: {task_options[selected_task]};'>Sustainability Assessment Result 🌍</h4>", unsafe_allow_html=True)
            st.write(assess_sustainability(project_description))
        
        elif selected_task == "Resource Optimization":
            st.markdown(f"<h4 style='color: {task_options[selected_task]};'>Resource Optimization Result 📊</h4>", unsafe_allow_html=True)
            st.write(optimize_resources(project_description))
        
        elif selected_task == "Risk Management":
            st.markdown(f"<h4 style='color: {task_options[selected_task]};'>Risk Management Result ⚠️</h4>", unsafe_allow_html=True)
            st.write(manage_risks(project_description))
            display_sample_chart()  # Show a sample chart for risk management
        
        elif selected_task == "Task Prioritization":
            st.markdown(f"<h4 style='color: {task_options[selected_task]};'>Task Prioritization Result 📋</h4>", unsafe_allow_html=True)
            st.write(prioritize_tasks(project_description))
        
        elif selected_task == "Schedule Optimization":
            st.markdown(f"<h4 style='color: {task_options[selected_task]};'>Schedule Optimization Result 📅</h4>", unsafe_allow_html=True)
            st.write(optimize_schedule(project_description))

    # Run All Analysis section with demarcation and colored headers
    if selected_task == "Run All":
        st.write("## All Analyses Results")
        st.markdown(f"<h4 style='color: #ff6347;'>Cost Estimation Result 💸</h4>", unsafe_allow_html=True)
        st.write(estimate_cost(project_description))
        display_sample_table()
        st.write("---")
        
        st.markdown(f"<h4 style='color: #4682b4;'>Sustainability Assessment Result 🌍</h4>", unsafe_allow_html=True)
        st.write(assess_sustainability(project_description))
        st.write("---")
        
        st.markdown(f"<h4 style='color: #32cd32;'>Resource Optimization Result 📊</h4>", unsafe_allow_html=True)
        st.write(optimize_resources(project_description))
        st.write("---")
        
        st.markdown(f"<h4 style='color: #ff8c00;'>Risk Management Result ⚠️</h4>", unsafe_allow_html=True)
        st.write(manage_risks(project_description))
        display_sample_chart()
        st.write("---")
        
        st.markdown(f"<h4 style='color: #8a2be2;'>Task Prioritization Result 📋</h4>", unsafe_allow_html=True)
        st.write(prioritize_tasks(project_description))
        st.write("---")
        
        st.markdown(f"<h4 style='color: #ff1493;'>Schedule Optimization Result 📅</h4>", unsafe_allow_html=True)
        st.write(optimize_schedule(project_description))

# Footer with some padding and styling
st.write("---")
st.markdown("<p style='text-align: center; color: #808080;'>Designed by Ginikanwa Nnenna | Powered by AI</p>", unsafe_allow_html=True)
