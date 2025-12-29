import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime
from PIL import Image
import base64
import secrets
import string
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Al Raed Security - Work Management",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# EXECUTIVE COMMAND CENTER CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: #fafbfc; }
    
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem; max-width: 100%; }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1rem 1.25rem;
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.8125rem;
        color: #718096;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    /* Task Row */
    .task-row {
        padding: 0.875rem 1rem;
        border-bottom: 1px solid #e2e8f0;
        cursor: pointer;
        transition: background 0.1s;
    }
    .task-row:hover {
        background: #f7fafc;
    }
    .task-row.selected {
        background: #edf2f7;
        border-left: 3px solid #9f7928;
    }
    .task-title {
        font-size: 0.9375rem;
        font-weight: 500;
        color: #2d3748;
        margin-bottom: 0.25rem;
    }
    .task-meta {
        font-size: 0.8125rem;
        color: #718096;
    }
    
    /* Priority Dots */
    .priority-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    .priority-high { background: #e53e3e; }
    .priority-medium { background: #ed8936; }
    .priority-low { background: #48bb78; }
    
    /* Clean Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        padding: 0.625rem 0.875rem !important;
        font-size: 0.9375rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #9f7928 !important;
        box-shadow: 0 0 0 1px #9f7928 !important;
    }
    
    /* Clean Buttons */
    .stButton > button {
        background: #9f7928 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.625rem 1.25rem !important;
        font-size: 0.9375rem !important;
        font-weight: 500 !important;
        transition: background 0.15s !important;
    }
    
    .stButton > button:hover {
        background: #8a6a24 !important;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 0.875rem;
        font-weight: 600;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* Detail Panel */
    .detail-panel {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1.5rem;
        min-height: 600px;
    }
    
    /* Activity Item */
    .activity-item {
        padding: 0.75rem;
        background: #f7fafc;
        border-left: 2px solid #e2e8f0;
        margin-bottom: 0.75rem;
        border-radius: 4px;
    }
    .activity-author {
        font-weight: 600;
        color: #2d3748;
        font-size: 0.875rem;
    }
    .activity-content {
        color: #4a5568;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.625rem;
        border-radius: 4px;
        font-size: 0.8125rem;
        font-weight: 500;
    }
    .status-pending { background: #bee3f8; color: #2c5282; }
    .status-finished { background: #c6f6d5; color: #22543d; }
    
    /* Remove labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label { display: none !important; }
    
    /* Tabs - Login Only */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #e2e8f0;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #718096;
        font-weight: 500;
        padding: 0.875rem 2rem;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #2d3748;
        font-weight: 600;
        border-bottom-color: #9f7928;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATABASE CONNECTION
# ==========================================
URL = st.secrets["URL"]
KEY = st.secrets["KEY"]
supabase = create_client(URL, KEY)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_file_icon(file_type):
    icons = {'pdf': '📄', 'doc': '📝', 'docx': '📝', 'xls': '📊', 'xlsx': '📊',
             'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'default': '📎'}
    extension = file_type.lower().replace('.', '')
    return icons.get(extension, icons['default'])

def format_file_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def save_file_to_database(file, task_id, uploaded_by):
    try:
        file_bytes = file.read()
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')
        file_record = {
            "task_id": task_id, "file_name": file.name, "file_type": file.type,
            "file_size": len(file_bytes), "file_data": file_base64,
            "uploaded_by": uploaded_by, "uploaded_at": datetime.now().isoformat()
        }
        supabase.table("TaskFilesTable").insert(file_record).execute()
        return True, "File uploaded"
    except Exception as e:
        return False, str(e)

def get_task_files(task_id):
    try:
        response = supabase.table("TaskFilesTable").select("*").eq("task_id", task_id).execute()
        return response.data if response.data else []
    except:
        return []

def create_download_link(file_data, file_name, file_type):
    try:
        href = f'<a href="data:{file_type};base64,{file_data}" download="{file_name}" style="color: #9f7928; text-decoration: none; font-weight: 500;">Download</a>'
        return href
    except:
        return 'Error'

# ==========================================
# LOGIN SYSTEM
# ==========================================
if "user" not in st.session_state:
    # Login header
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <h1 style='color: #2d3748; font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0 0.2rem 0;'>
            Al Raed Security
        </h1>
        <p style='color: #718096; font-size: 0.875rem; margin: 0;'>
            Work Management System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    login_tab, register_tab = st.tabs(["Login", "Request Access"])
    
    # LOGIN TAB
    with login_tab:
        col1, col2, col3 = st.columns([1, 2.5, 1])
        with col2:
            st.markdown("<div style='background: white; padding: 2rem 2.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: -1rem;'></div>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                user_username = st.text_input("", placeholder="Username or Email", label_visibility="collapsed")
                user_password = st.text_input("", type="password", placeholder="Password", label_visibility="collapsed")
                col_check, col_forgot = st.columns([1, 1])
                with col_check:
                    remember = st.checkbox("Remember me", value=False)
                with col_forgot:
                    st.markdown("<p style='text-align: right; margin-top: 0.5rem;'><a href='#' style='color: #9f7928; text-decoration: none; font-size: 0.875rem;'>Forgot Password?</a></p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Sign In", use_container_width=True)
            
            # Handle login OUTSIDE the form to avoid message stacking
            if submit:
                if user_username and user_password:
                    try:
                        res = supabase.table("UsersTable").select("*").eq("username", user_username).eq("password", user_password).execute()
                        if res.data:
                            user_data = res.data[0]
                            if user_data.get("status") == "pending":
                                st.warning("Account pending approval")
                            elif user_data.get("status") == "rejected":
                                st.error("Account access denied")
                            else:
                                st.session_state.user = {"name": user_data["full_name"], "role": str(user_data["role"]).strip()}
                                st.session_state.selected_task = None
                                st.success(f"Welcome, {user_data['full_name']}")
                                st.rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error("Authentication failed - please check your credentials")
                else:
                    st.warning("Please enter both fields")
    
    # REGISTRATION TAB
    with register_tab:
        col1, col2, col3 = st.columns([1, 2.5, 1])
        with col2:
            st.markdown("<div style='background: white; padding: 2rem 2.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: -1rem;'></div>", unsafe_allow_html=True)
            
            with st.form("registration_form", clear_on_submit=True):
                reg_name = st.text_input("", placeholder="Full Name", label_visibility="collapsed")
                reg_username = st.text_input("", placeholder="Choose Username", label_visibility="collapsed")
                reg_email = st.text_input("", placeholder="Email Address", label_visibility="collapsed")
                reg_phone = st.text_input("", placeholder="Phone Number", label_visibility="collapsed")
                reg_department = st.selectbox("Department", ["Security Operations", "Administration", "Technical", "HR", "Finance", "Other"])
                st.markdown("<br>", unsafe_allow_html=True)
                register_btn = st.form_submit_button("Submit Request", use_container_width=True)
                
                if register_btn:
                    if reg_name and reg_username:
                        try:
                            existing = supabase.table("UsersTable").select("*").eq("username", reg_username).execute()
                            if existing.data:
                                st.error("Username already taken")
                            else:
                                temp_password = generate_temp_password()
                                new_user = {
                                    "full_name": reg_name, "username": reg_username, "password": temp_password,
                                    "role": "staff", "status": "pending", "email": reg_email,
                                    "phone": reg_phone, "department": reg_department,
                                    "requested_at": datetime.now().isoformat()
                                }
                                supabase.table("UsersTable").insert(new_user).execute()
                                st.success("Request submitted! Wait for admin approval.")
                        except Exception as e:
                            st.error("Registration failed")
                    else:
                        st.error("Name and username required")
    
    st.stop()

# ==========================================
# EXECUTIVE DASHBOARD - LOGGED IN
# ==========================================
curr_user = st.session_state.user

# Header
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    try:
        logo = Image.open("logo_alraed_Security.png")
        st.image(logo, width=50)
    except:
        pass
with col2:
    st.markdown(f"""
    <div style='padding: 0.5rem 0;'>
        <h1 style='color: #2d3748; font-size: 1.25rem; font-weight: 600; margin: 0;'>
            Al Raed Security
        </h1>
        <p style='color: #718096; font-size: 0.8125rem; margin: 0;'>
            {curr_user['name']} • {curr_user['role'].upper()}
        </p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    if st.button("Logout", use_container_width=True):
        del st.session_state.user
        st.rerun()

st.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

# Get tasks
if curr_user["role"].lower() == "boss":
    all_tasks = supabase.table("TasksTable").select("*").order("deadline").execute().data or []
else:
    all_tasks = supabase.table("TasksTable").select("*").ilike("assigned_to", curr_user["name"]).order("deadline").execute().data or []

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    active = len([t for t in all_tasks if t.get('status') == 'Pending'])
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{active}</div>
        <div class="kpi-label">ACTIVE TASKS</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    completed = len([t for t in all_tasks if t.get('status') == 'Finished'])
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{completed}</div>
        <div class="kpi-label">COMPLETED</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    high_priority = len([t for t in all_tasks if t.get('priority') == 'High'])
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{high_priority}</div>
        <div class="kpi-label">HIGH PRIORITY</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    total = len(all_tasks)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total}</div>
        <div class="kpi-label">TOTAL TASKS</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Two-Column Layout
col_list, col_detail = st.columns([2, 3])

# LEFT: Task List
with col_list:
    st.markdown('<div class="section-header">TASK LIST</div>', unsafe_allow_html=True)
    
    # Filter for boss
    if curr_user["role"].lower() == "boss":
        filter_status = st.selectbox("Filter", ["All Tasks", "Pending Only", "Completed Only"], label_visibility="collapsed")
        if filter_status == "Pending Only":
            all_tasks = [t for t in all_tasks if t.get('status') == 'Pending']
        elif filter_status == "Completed Only":
            all_tasks = [t for t in all_tasks if t.get('status') == 'Finished']
    
    # Task rows
    if all_tasks:
        for task in all_tasks:
            priority_class = f"priority-{task.get('priority', 'medium').lower()}"
            selected_class = "selected" if st.session_state.get('selected_task') == task['id'] else ""
            
            # Using a container with button
            if st.button(f"{task['title']}", key=f"task_{task['id']}", use_container_width=True):
                st.session_state.selected_task = task['id']
                st.rerun()
            
            # Show task info below button
            st.markdown(f"""
            <div style='margin-top: -0.5rem; margin-bottom: 1rem; padding-left: 1rem; font-size: 0.8125rem; color: #718096;'>
                <span class='priority-dot {priority_class}'></span>
                {task.get('priority', 'Medium')} • Due: {task.get('deadline', 'N/A')} • {task.get('status', 'Pending')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tasks found")
    
    # Quick add for staff
    if curr_user["role"].lower() != "boss":
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("➕ Create New Task"):
            with st.form("quick_add", clear_on_submit=True):
                title = st.text_input("", placeholder="Task title")
                deadline = st.date_input("Deadline")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                if st.form_submit_button("Create"):
                    if title:
                        supabase.table("TasksTable").insert({
                            "title": title, "deadline": str(deadline), "priority": priority,
                            "status": "Pending", "assigned_to": curr_user["name"]
                        }).execute()
                        st.success("Task created!")
                        st.rerun()

# RIGHT: Task Detail
with col_detail:
    st.markdown('<div class="section-header">TASK DETAILS</div>', unsafe_allow_html=True)
    
    selected_id = st.session_state.get('selected_task')
    if selected_id and all_tasks:
        task = next((t for t in all_tasks if t['id'] == selected_id), None)
        if task:
            # Task info
            st.markdown(f"### {task['title']}")
            st.markdown(f"""
            <div style='margin: 1rem 0;'>
                <span class='status-badge status-{task.get('status', 'pending').lower()}'>{task.get('status', 'Pending')}</span>
                <span class='status-badge' style='background: #edf2f7; color: #2d3748;'>Priority: {task.get('priority', 'Medium')}</span>
                <span class='status-badge' style='background: #edf2f7; color: #2d3748;'>Due: {task.get('deadline', 'N/A')}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 1.5rem 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
            
            # Activity log
            st.markdown("**Activity Log:**")
            activities = supabase.table("FollowupsTable").select("*").eq("task_id", task['id']).order("id", desc=True).execute().data or []
            if activities:
                for act in activities:
                    st.markdown(f"""
                    <div class='activity-item'>
                        <div class='activity-author'>{act.get('author_name', 'Unknown')}</div>
                        <div class='activity-content'>{act.get('content', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("No activity yet")
            
            st.markdown("<hr style='margin: 1.5rem 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
            
            # Actions
            if task.get('status') != 'Finished':
                with st.form("add_update", clear_on_submit=True):
                    update_text = st.text_area("", placeholder="Add progress update...", label_visibility="collapsed")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.form_submit_button("Add Update", use_container_width=True):
                            if update_text:
                                prefix = "BOSS: " if curr_user["role"].lower() == "boss" else ""
                                supabase.table("FollowupsTable").insert({
                                    "task_id": task['id'],
                                    "author_name": f"{prefix}{curr_user['name']}",
                                    "content": update_text
                                }).execute()
                                st.success("Update added!")
                                st.rerun()
                    with col_b:
                        if st.form_submit_button("Mark Complete", use_container_width=True):
                            supabase.table("TasksTable").update({"status": "Finished"}).eq("id", task['id']).execute()
                            st.success("Task completed!")
                            st.rerun()
                
                # File upload
                st.markdown("<br>", unsafe_allow_html=True)
                uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, label_visibility="collapsed")
                if uploaded_files:
                    if st.button("Upload"):
                        for file in uploaded_files:
                            save_file_to_database(file, task['id'], curr_user['name'])
                        st.success("Files uploaded!")
                        st.rerun()
            
            # Show files
            files = get_task_files(task['id'])
            if files:
                st.markdown("<hr style='margin: 1.5rem 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
                st.markdown("**Attached Files:**")
                for file in files:
                    col_f1, col_f2 = st.columns([3, 1])
                    with col_f1:
                        st.markdown(f"{get_file_icon(file['file_name'])} {file['file_name']} ({format_file_size(file['file_size'])})")
                    with col_f2:
                        st.markdown(create_download_link(file['file_data'], file['file_name'], file['file_type']), unsafe_allow_html=True)
        else:
            st.info("Task not found")
    else:
        st.info("Select a task from the list")
