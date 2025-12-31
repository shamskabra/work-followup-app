import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from supabase import create_client
import pandas as pd
from datetime import datetime
from PIL import Image
import base64
import secrets
import string
import os

# ==========================================
# COOKIE MANAGER SETUP - ADD THIS FIRST
# ==========================================
# Initialize cookies with encryption
cookies = EncryptedCookieManager(
    prefix="alraed_security_",
    password=os.environ.get("COOKIE_PASSWORD", "change-this-to-a-secure-random-string-in-production")
)

# Wait for cookies to be ready
if not cookies.ready():
    st.stop()

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
        color: #9f7928;
        border-bottom-color: #9f7928;
    }
    
    /* Login Card */
    .login-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 2.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SUPABASE INITIALIZATION
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in secrets or environment variables.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def save_file_to_database(uploaded_file, task_id, uploaded_by):
    file_bytes = uploaded_file.read()
    file_b64 = base64.b64encode(file_bytes).decode()
    supabase.table("TaskFilesTable").insert({
        "task_id": task_id,
        "file_name": uploaded_file.name,
        "file_type": uploaded_file.type,
        "file_size": len(file_bytes),
        "file_data": file_b64,
        "uploaded_by": uploaded_by
    }).execute()

def get_task_files(task_id):
    result = supabase.table("TaskFilesTable").select("*").eq("task_id", task_id).execute()
    return result.data or []

def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes/(1024**2):.1f} MB"

def get_file_icon(filename):
    ext = filename.split('.')[-1].lower()
    icons = {
        'pdf': '📄', 'doc': '📝', 'docx': '📝',
        'xls': '📊', 'xlsx': '📊', 'csv': '📊',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
        'zip': '📦', 'rar': '📦'
    }
    return icons.get(ext, '📎')

def create_download_link(b64_data, filename, file_type):
    href = f'<a href="data:{file_type};base64,{b64_data}" download="{filename}" style="text-decoration: none; color: #9f7928; font-weight: 500;">⬇️ Download</a>'
    return href

# ==========================================
# SESSION RESTORATION FROM COOKIES
# ==========================================
# Check if user is logged in via cookies (on page refresh/reload)
if 'logged_in' not in st.session_state:
    if cookies.get('logged_in') == 'true':
        # Restore session from cookies
        st.session_state.logged_in = True
        st.session_state.current_user = {
            "name": cookies.get('user_name', ''),
            "role": cookies.get('user_role', '')
        }
    else:
        st.session_state.logged_in = False
        st.session_state.current_user = None

# ==========================================
# LOGOUT FUNCTION
# ==========================================
def logout():
    # Clear session state
    st.session_state.logged_in = False
    st.session_state.current_user = None
    
    # Clear cookies
    cookies['logged_in'] = 'false'
    cookies['user_name'] = ''
    cookies['user_role'] = ''
    cookies.save()
    
    st.rerun()

# ==========================================
# MAIN APPLICATION LOGIC
# ==========================================
if not st.session_state.get('logged_in'):
    # ==========================================
    # LOGIN / SIGNUP SCREEN
    # ==========================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #9f7928; font-size: 2.5rem; margin-bottom: 0.5rem;'>🛡️ Al Raed Security</h1>
            <p style='color: #718096; font-size: 1.125rem;'>Work Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        login_tab, signup_tab = st.tabs(["LOGIN", "SIGN UP"])
        
        # LOGIN TAB
        with login_tab:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("login_form"):
                login_email = st.text_input("", placeholder="Email", key="login_email")
                login_pass = st.text_input("", placeholder="Password", type="password", key="login_pass")
                login_button = st.form_submit_button("LOGIN", use_container_width=True)
                
                if login_button:
                    if login_email and login_pass:
                        user_query = supabase.table("UsersTable").select("*").eq("email", login_email).eq("password", login_pass).execute()
                        if user_query.data:
                            user = user_query.data[0]
                            
                            # Set session state
                            st.session_state.logged_in = True
                            st.session_state.current_user = {"name": user['full_name'], "role": user['role']}
                            
                            # Save to cookies for persistence
                            cookies['logged_in'] = 'true'
                            cookies['user_name'] = user['full_name']
                            cookies['user_role'] = user['role']
                            cookies.save()
                            
                            st.success(f"Welcome back, {user['full_name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.error("Please fill in all fields")
        
        # SIGNUP TAB
        with signup_tab:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("signup_form"):
                signup_name = st.text_input("", placeholder="Full Name", key="signup_name")
                signup_email = st.text_input("", placeholder="Email", key="signup_email")
                signup_pass = st.text_input("", placeholder="Password (min 6 characters)", type="password", key="signup_pass")
                signup_button = st.form_submit_button("SIGN UP", use_container_width=True)
                
                if signup_button:
                    if signup_name and signup_email and signup_pass:
                        if len(signup_pass) < 6:
                            st.error("Password must be at least 6 characters")
                        else:
                            existing = supabase.table("UsersTable").select("*").eq("email", signup_email).execute()
                            if existing.data:
                                st.error("Email already registered")
                            else:
                                supabase.table("UsersTable").insert({
                                    "full_name": signup_name,
                                    "email": signup_email,
                                    "password": signup_pass,
                                    "role": "Staff"
                                }).execute()
                                st.success("Account created! Please login.")
                    else:
                        st.error("Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # ==========================================
    # LOGGED IN - SHOW APPROPRIATE DASHBOARD
    # ==========================================
    curr_user = st.session_state.current_user
    
    # Header with logout
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"""
        <div style='padding: 1rem 0;'>
            <h2 style='color: #2d3748; margin: 0;'>Welcome, {curr_user['name']}</h2>
            <p style='color: #718096; margin: 0;'>Role: {curr_user['role']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    
    # ==========================================
    # ADMIN DASHBOARD
    # ==========================================
    if curr_user['role'] == 'Admin':
        admin_tabs = st.tabs(["📊 Dashboard", "👥 Users", "📋 Tasks", "🔐 Change Password"])
        
        # ADMIN TAB 1: DASHBOARD
        with admin_tabs[0]:
            st.markdown('<div class="section-header">OVERVIEW</div>', unsafe_allow_html=True)
            
            all_tasks = supabase.table("TasksTable").select("*").execute().data or []
            all_users = supabase.table("UsersTable").select("*").execute().data or []
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_tasks = len(all_tasks)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{total_tasks}</div>
                    <div class="kpi-label">TOTAL TASKS</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                pending = len([t for t in all_tasks if t.get('status') == 'Pending'])
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{pending}</div>
                    <div class="kpi-label">PENDING</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                finished = len([t for t in all_tasks if t.get('status') == 'Finished'])
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{finished}</div>
                    <div class="kpi-label">COMPLETED</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                total_users = len(all_users)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{total_users}</div>
                    <div class="kpi-label">USERS</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            if all_tasks:
                df = pd.DataFrame(all_tasks)
                df = df[['title', 'assigned_to', 'status', 'priority', 'deadline']]
                df.columns = ['Task', 'Assigned To', 'Status', 'Priority', 'Deadline']
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No tasks yet")
        
        # ADMIN TAB 2: USERS
        with admin_tabs[1]:
            st.markdown('<div class="section-header">USER MANAGEMENT</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown("**Add New User**")
                with st.form("add_user", clear_on_submit=True):
                    new_name = st.text_input("", placeholder="Full Name")
                    new_email = st.text_input("", placeholder="Email")
                    new_role = st.selectbox("Role", ["Staff", "Admin"])
                    
                    if st.form_submit_button("Create User", use_container_width=True):
                        if new_name and new_email:
                            existing = supabase.table("UsersTable").select("*").eq("email", new_email).execute()
                            if existing.data:
                                st.error("Email already exists")
                            else:
                                temp_pass = generate_password()
                                supabase.table("UsersTable").insert({
                                    "full_name": new_name,
                                    "email": new_email,
                                    "password": temp_pass,
                                    "role": new_role
                                }).execute()
                                st.success(f"User created! Temp password: `{temp_pass}`")
                                st.rerun()
                        else:
                            st.error("Please fill all fields")
            
            with col2:
                st.markdown("**All Users**")
                users = supabase.table("UsersTable").select("*").execute().data or []
                if users:
                    for user in users:
                        with st.expander(f"{user['full_name']} ({user['role']})"):
                            st.write(f"**Email:** {user['email']}")
                            st.write(f"**Role:** {user['role']}")
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("Reset Password", key=f"reset_{user['id']}"):
                                    new_pass = generate_password()
                                    supabase.table("UsersTable").update({"password": new_pass}).eq("id", user['id']).execute()
                                    st.success(f"New password: `{new_pass}`")
                            with col_b:
                                if st.button("Delete User", key=f"del_{user['id']}", type="secondary"):
                                    supabase.table("UsersTable").delete().eq("id", user['id']).execute()
                                    st.success("User deleted!")
                                    st.rerun()
                else:
                    st.info("No users found")
        
        # ADMIN TAB 3: TASKS
        with admin_tabs[2]:
            st.markdown('<div class="section-header">TASK MANAGEMENT</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown("**Create New Task**")
                users = supabase.table("UsersTable").select("full_name").execute().data or []
                user_names = [u['full_name'] for u in users]
                
                with st.form("create_task", clear_on_submit=True):
                    task_title = st.text_input("", placeholder="Task Title")
                    task_assign = st.selectbox("Assign to", user_names if user_names else ["No users"])
                    task_deadline = st.date_input("Deadline")
                    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                    
                    if st.form_submit_button("Create Task", use_container_width=True):
                        if task_title and task_assign:
                            supabase.table("TasksTable").insert({
                                "title": task_title,
                                "assigned_to": task_assign,
                                "deadline": str(task_deadline),
                                "priority": task_priority,
                                "status": "Pending"
                            }).execute()
                            st.success("Task created!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Please fill all fields")
            
            with col2:
                st.markdown("**All Tasks**")
                tasks = supabase.table("TasksTable").select("*").order("deadline").execute().data or []
                if tasks:
                    for task in tasks:
                        with st.expander(f"{task['title']} - {task['status']}"):
                            st.write(f"**Assigned to:** {task.get('assigned_to', 'N/A')}")
                            st.write(f"**Deadline:** {task.get('deadline', 'N/A')}")
                            st.write(f"**Priority:** {task.get('priority', 'Medium')}")
                            st.write(f"**Status:** {task.get('status', 'Pending')}")
                            
                            # Files
                            files = get_task_files(task['id'])
                            if files:
                                st.markdown("**Files:**")
                                for file in files:
                                    col_f1, col_f2, col_f3 = st.columns([3, 1, 1])
                                    with col_f1:
                                        st.markdown(f"{get_file_icon(file['file_name'])} {file['file_name']}")
                                    with col_f2:
                                        st.markdown(create_download_link(file['file_data'], file['file_name'], file['file_type']), unsafe_allow_html=True)
                                    with col_f3:
                                        if st.button("Delete", key=f"del_file_{file['id']}", type="secondary"):
                                            supabase.table("TaskFilesTable").delete().eq("id", file['id']).execute()
                                            st.success("File deleted!")
                                            st.rerun()
                            
                            # File upload
                            with st.form(f"admin_upload_{task['id']}", clear_on_submit=True):
                                uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, key=f"upload_{task['id']}", label_visibility="collapsed")
                                if st.form_submit_button("Upload"):
                                    if uploaded_files:
                                        for file in uploaded_files:
                                            save_file_to_database(file, task['id'], curr_user['name'])
                                        st.success("Files uploaded!")
                                        st.rerun()
                            
                            if st.button("Delete Task", key=f"del_task_{task['id']}", type="secondary"):
                                supabase.table("TasksTable").delete().eq("id", task['id']).execute()
                                st.success("Task deleted!")
                                st.rerun()
                else:
                    st.info("No tasks found")
        
        # ADMIN TAB 4: CHANGE PASSWORD
        with admin_tabs[3]:
            st.markdown('<div class="section-header">CHANGE PASSWORD</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.form("admin_change_password"):
                    current_pass = st.text_input("", placeholder="Current Password", type="password", label_visibility="collapsed")
                    new_pass = st.text_input("", placeholder="New Password", type="password", label_visibility="collapsed")
                    confirm_pass = st.text_input("", placeholder="Confirm New Password", type="password", label_visibility="collapsed")
                    
                    if st.form_submit_button("Change Password", use_container_width=True):
                        if current_pass and new_pass and confirm_pass:
                            if new_pass != confirm_pass:
                                st.error("Passwords don't match")
                            elif len(new_pass) < 6:
                                st.error("Password must be at least 6 characters")
                            else:
                                user_data = supabase.table("UsersTable").select("*").eq("full_name", curr_user["name"]).execute()
                                if user_data.data and user_data.data[0]['password'] == current_pass:
                                    supabase.table("UsersTable").update({"password": new_pass}).eq("id", user_data.data[0]['id']).execute()
                                    st.success("Password changed successfully!")
                                else:
                                    st.error("Current password is incorrect")
                        else:
                            st.error("Please fill all fields")
    
    # ==========================================
    # STAFF DASHBOARD
    # ==========================================
    else:
        staff_tabs = st.tabs(["📋 My Tasks", "🔐 Change Password"])
        
        # STAFF TAB 1: MY TASKS
        with staff_tabs[0]:
            all_tasks = supabase.table("TasksTable").select("*").eq("assigned_to", curr_user["name"]).order("deadline").execute().data or []
            
            # KPIs
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                pending = len([t for t in all_tasks if t.get('status') == 'Pending'])
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{pending}</div>
                    <div class="kpi-label">PENDING</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                finished = len([t for t in all_tasks if t.get('status') == 'Finished'])
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{finished}</div>
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
                st.markdown('<div class="section-header">MY TASKS</div>', unsafe_allow_html=True)
                
                # Quick add
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
                                st.balloons()
                                st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Sort option for staff
                sort_by = st.selectbox("Sort by", ["Deadline", "Priority", "Status"], label_visibility="collapsed")
                
                # Apply sort
                if sort_by == "Priority":
                    priority_order = {"High": 1, "Medium": 2, "Low": 3}
                    all_tasks = sorted(all_tasks, key=lambda x: priority_order.get(x.get('priority', 'Medium'), 2))
                elif sort_by == "Status":
                    all_tasks = sorted(all_tasks, key=lambda x: x.get('status', ''))
                # Deadline is default (already sorted from query)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Task rows
                if all_tasks:
                    for task in all_tasks:
                        priority_class = f"priority-{task.get('priority', 'medium').lower()}"
                        
                        if st.button(f"{task['title']}", key=f"task_{task['id']}", use_container_width=True):
                            st.session_state.selected_task = task['id']
                            st.rerun()
                        
                        st.markdown(f"""
                        <div style='margin-top: -0.5rem; margin-bottom: 1rem; padding-left: 1rem; font-size: 0.8125rem; color: #718096;'>
                            <span class='priority-dot {priority_class}'></span>
                            {task.get('priority', 'Medium')} • Due: {task.get('deadline', 'N/A')} • {task.get('status', 'Pending')}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No tasks found")
            
            # RIGHT: Task Detail
            with col_detail:
                st.markdown('<div class="section-header">TASK DETAILS</div>', unsafe_allow_html=True)
                
                selected_id = st.session_state.get('selected_task')
                if selected_id and all_tasks:
                    task = next((t for t in all_tasks if t['id'] == selected_id), None)
                    if task:
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
                                            supabase.table("FollowupsTable").insert({
                                                "task_id": task['id'],
                                                "author_name": curr_user['name'],
                                                "content": update_text
                                            }).execute()
                                            st.success("Update added!")
                                            st.rerun()
                                with col_b:
                                    if st.form_submit_button("Mark Complete", use_container_width=True):
                                        supabase.table("TasksTable").update({"status": "Finished"}).eq("id", task['id']).execute()
                                        st.success("Task completed!")
                                        st.balloons()
                                        st.rerun()
                            
                            # File upload
                            st.markdown("<br>", unsafe_allow_html=True)
                            with st.form(f"staff_file_upload_{task['id']}", clear_on_submit=True):
                                uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, label_visibility="collapsed")
                                if st.form_submit_button("Upload", use_container_width=True):
                                    if uploaded_files:
                                        for file in uploaded_files:
                                            save_file_to_database(file, task['id'], curr_user['name'])
                                        st.success("Files uploaded!")
                                        st.rerun()
                                    else:
                                        st.warning("Please select files first")
                        
                        # Show files
                        files = get_task_files(task['id'])
                        if files:
                            st.markdown("<hr style='margin: 1.5rem 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
                            st.markdown("**Attached Files:**")
                            for file in files:
                                col_f1, col_f2, col_f3 = st.columns([3, 1, 1])
                                with col_f1:
                                    st.markdown(f"{get_file_icon(file['file_name'])} {file['file_name']} ({format_file_size(file['file_size'])})")
                                with col_f2:
                                    st.markdown(create_download_link(file['file_data'], file['file_name'], file['file_type']), unsafe_allow_html=True)
                                with col_f3:
                                    if st.button("Delete", key=f"del_file_staff_{file['id']}", type="secondary"):
                                        supabase.table("TaskFilesTable").delete().eq("id", file['id']).execute()
                                        st.success("File deleted!")
                                        st.rerun()
                    else:
                        st.info("Task not found")
                else:
                    st.info("Select a task from the list")
        
        # STAFF TAB 2: CHANGE PASSWORD
        with staff_tabs[1]:
            st.markdown('<div class="section-header">CHANGE PASSWORD</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with st.form("change_password"):
                    current_pass = st.text_input("", placeholder="Current Password", type="password", label_visibility="collapsed")
                    new_pass = st.text_input("", placeholder="New Password", type="password", label_visibility="collapsed")
                    confirm_pass = st.text_input("", placeholder="Confirm New Password", type="password", label_visibility="collapsed")
                    
                    if st.form_submit_button("Change Password", use_container_width=True):
                        if current_pass and new_pass and confirm_pass:
                            if new_pass != confirm_pass:
                                st.error("Passwords don't match")
                            elif len(new_pass) < 6:
                                st.error("Password must be at least 6 characters")
                            else:
                                user_data = supabase.table("UsersTable").select("*").eq("full_name", curr_user["name"]).execute()
                                if user_data.data and user_data.data[0]['password'] == current_pass:
                                    supabase.table("UsersTable").update({"password": new_pass}).eq("id", user_data.data[0]['id']).execute()
                                    st.success("Password changed successfully!")
                                else:
                                    st.error("Current password is incorrect")
                        else:
                            st.error("Please fill all fields")
