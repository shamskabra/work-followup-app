import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime
from PIL import Image

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Al Raed Security - Work Tracker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS FOR PROFESSIONAL LOOK
# ==========================================
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #D4AF37;
    }
    
    .company-name {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .company-tagline {
        color: #5d6d7e;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Card styling */
    .stContainer {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    /* Priority badges */
    .priority-high {
        background-color: #e74c3c;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .priority-medium {
        background-color: #f39c12;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .priority-low {
        background-color: #27ae60;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Status badges */
    .status-pending {
        background-color: #3498db;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    
    .status-finished {
        background-color: #27ae60;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        background-color: #3498db;
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        background-color: #2980b9;
    }
    
    /* Sidebar styling - LIGHT THEME */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 3px solid #D4AF37;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #2c3e50 !important;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .element-container,
    [data-testid="stSidebar"] label {
        color: #34495e !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background-color: #e74c3c;
        color: white;
        border: none;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #c0392b;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        color: #2c3e50;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: white;
        border-radius: 8px;
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #2c3e50 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #34495e !important;
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
# HEADER WITH LOGO
# ==========================================
def show_header():
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            logo = Image.open("logo_alraed_Security.png")
            st.image(logo, width=120)
        except:
            st.markdown("🛡️")
    
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1 class="company-name">Al Raed Security</h1>
            <p class="company-tagline">Work Management System</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# LOGIN SYSTEM
# ==========================================
if "user" not in st.session_state:
    show_header()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
            <h2 style='text-align: center; color: #6B5644; margin-bottom: 2rem;'>🔐 System Login</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown("#### Enter Your Credentials")
            user_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            user_password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit = st.form_submit_button("🚀 Enter System", use_container_width=True)
            
            if submit:
                if user_name and user_password:
                    res = supabase.table("UsersTable").select("*").eq("full_name", user_name).eq("password", user_password).execute()
                    
                    if res.data:
                        user_data = res.data[0]
                        st.session_state.user = {
                            "name": user_data["full_name"], 
                            "role": str(user_data["role"]).strip()
                        }
                        st.success(f"✅ Welcome back, {user_data['full_name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Name or Password")
                else:
                    st.warning("⚠️ Please enter both Name and Password")
    st.stop()

# ==========================================
# LOGGED IN VIEW
# ==========================================
else:
    show_header()
    
    curr_user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"### 👤 {curr_user['name']}")
        st.markdown(f"**Role:** {curr_user['role'].upper()}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            del st.session_state.user
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        # Get task stats
        try:
            if curr_user["role"].lower() == "boss":
                all_tasks = supabase.table("TasksTable").select("*").execute().data
                pending = len([t for t in all_tasks if t.get('status') == 'Pending'])
                finished = len([t for t in all_tasks if t.get('status') == 'Finished'])
            else:
                my_tasks = supabase.table("TasksTable").select("*").ilike("assigned_to", curr_user["name"]).execute().data
                pending = len([t for t in my_tasks if t.get('status') == 'Pending'])
                finished = len([t for t in my_tasks if t.get('status') == 'Finished'])
            
            st.metric("⏳ Pending", pending)
            st.metric("✅ Finished", finished)
        except:
            pass

    # ==========================================
    # BOSS VIEW
    # ==========================================
    if curr_user["role"].lower() == "boss":
        st.title("👨‍💼 Management Control Center")
        st.markdown("---")
        
        response = supabase.table("TasksTable").select("*").execute()
        all_tasks = response.data

        if all_tasks:
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_status = st.selectbox("📋 Filter by Status", ["All", "Pending", "Finished"])
            with col2:
                filter_priority = st.selectbox("🎯 Filter by Priority", ["All", "High", "Medium", "Low"])
            with col3:
                sort_by = st.selectbox("📊 Sort by", ["Deadline", "Priority", "Status"])
            
            df = pd.DataFrame(all_tasks)
            
            # Apply filters
            if filter_status != "All":
                df = df[df['status'] == filter_status]
            if filter_priority != "All":
                df = df[df['priority'] == filter_priority]
            
            st.markdown("---")
            
            for index, row in df.iterrows():
                p_val = row.get('priority', 'Medium')
                
                # Priority badge HTML
                if p_val == "High":
                    priority_badge = '<span class="priority-high">🔴 HIGH PRIORITY</span>'
                elif p_val == "Medium":
                    priority_badge = '<span class="priority-medium">🟡 MEDIUM</span>'
                else:
                    priority_badge = '<span class="priority-low">🟢 LOW</span>'
                
                # Status badge
                if row['status'] == "Finished":
                    status_badge = '<span class="status-finished">✅ FINISHED</span>'
                else:
                    status_badge = '<span class="status-pending">⏳ PENDING</span>'
                
                with st.container(border=True):
                    col_info, col_action = st.columns([3, 1])
                    
                    with col_info:
                        st.markdown(f"### {row['title']}")
                        st.markdown(f"{priority_badge} {status_badge}", unsafe_allow_html=True)
                        st.markdown(f"**👤 Assigned to:** `{row['assigned_to']}` | **📅 Deadline:** `{row['deadline']}`")
                        
                        # Latest update
                        f_res = supabase.table("FollowupsTable").select("content, author_name").eq("task_id", row['id']).order("id", desc=True).limit(1).execute()
                        if f_res.data:
                            st.markdown(f"**💬 Latest Update ({f_res.data[0]['author_name']}):** {f_res.data[0]['content']}")

                    with col_action:
                        try:
                            p_idx = ["Low", "Medium", "High"].index(p_val)
                        except:
                            p_idx = 1
                        new_prio = st.selectbox("Set Priority", ["Low", "Medium", "High"], index=p_idx, key=f"p_{row['id']}")
                        if st.button("💾 Update", key=f"b_{row['id']}", use_container_width=True):
                            supabase.table("TasksTable").update({"priority": new_prio}).eq("id", row['id']).execute()
                            st.success("Updated!")
                            st.rerun()
                    
                    with st.expander("💬 Add Comment / Instruction"):
                        msg = st.text_area("Your message:", key=f"m_{row['id']}", placeholder="Add notes, instructions, or feedback...")
                        if st.button("📤 Send Message", key=f"s_{row['id']}"):
                            if msg:
                                supabase.table("FollowupsTable").insert({
                                    "task_id": row['id'], 
                                    "author_name": f"BOSS: {curr_user['name']}", 
                                    "content": msg
                                }).execute()
                                st.success("✅ Message sent!")
                                st.rerun()
        else:
            st.info("📭 No tasks found in the system.")

    # ==========================================
    # STAFF VIEW
    # ==========================================
    else:
        st.title("📋 My Workspace")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["➕ Create New Task", "🔄 My Active Tasks"])

        with tab1:
            st.markdown("### 📝 Submit New Task Request")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                with st.form("new_work_form", clear_on_submit=True):
                    title = st.text_input("📌 Task/Project Title", placeholder="Enter a descriptive title...")
                    description = st.text_area("📄 Description (Optional)", placeholder="Add more details about this task...")
                    due = st.date_input("📅 Target Deadline")
                    prio = st.selectbox("🎯 Initial Priority", ["Low", "Medium", "High"], index=1)
                    
                    submit_btn = st.form_submit_button("🚀 Submit to Management", use_container_width=True)
                
                if submit_btn:
                    if title:
                        supabase.table("TasksTable").insert({
                            "title": title,
                            "deadline": str(due),
                            "priority": prio,
                            "status": "Pending",
                            "assigned_to": curr_user["name"]
                        }).execute()
                        st.success("✅ Task submitted successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Please provide a task title")
            
            with col2:
                st.markdown("""
                <div class="info-box">
                    <h4>💡 Tips</h4>
                    <ul>
                        <li>Be specific in your title</li>
                        <li>Set realistic deadlines</li>
                        <li>Choose appropriate priority</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### 📌 Tasks Assigned to Me")
            
            my_res = supabase.table("TasksTable").select("*").ilike("assigned_to", curr_user["name"]).execute()
            my_tasks = my_res.data
            
            if my_tasks:
                # Separate pending and finished
                pending_tasks = [t for t in my_tasks if t['status'] != 'Finished']
                finished_tasks = [t for t in my_tasks if t['status'] == 'Finished']
                
                st.markdown(f"**Active Tasks:** {len(pending_tasks)} | **Completed:** {len(finished_tasks)}")
                st.markdown("---")
                
                for t in my_tasks:
                    # Priority and status styling
                    if t['priority'] == "High":
                        priority_emoji = "🔴"
                        priority_color = "#ff4444"
                    elif t['priority'] == "Medium":
                        priority_emoji = "🟡"
                        priority_color = "#ffaa00"
                    else:
                        priority_emoji = "🟢"
                        priority_color = "#44bb44"
                    
                    status_icon = "✅" if t['status'] == "Finished" else "⏳"
                    
                    with st.expander(f"{status_icon} {priority_emoji} **{t['title']}** (Due: {t['deadline']})", expanded=(t['status'] != 'Finished')):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Priority:** {t['priority']}")
                            st.markdown(f"**Status:** {t['status']}")
                            st.markdown(f"**Deadline:** {t['deadline']}")
                        
                        with col2:
                            if t['status'] != "Finished":
                                if st.button("✅ Mark Complete", key=f"fin_{t['id']}", use_container_width=True):
                                    supabase.table("TasksTable").update({"status": "Finished"}).eq("id", t['id']).execute()
                                    st.success("Task completed!")
                                    st.balloons()
                                    st.rerun()
                        
                        st.markdown("---")
                        
                        # Conversation history
                        history = supabase.table("FollowupsTable").select("*").eq("task_id", t['id']).order("id", desc=True).execute()
                        if history.data:
                            st.markdown("**💬 Activity Log:**")
                            for log in history.data:
                                is_boss = "BOSS:" in log['author_name']
                                icon = "👨‍💼" if is_boss else "👤"
                                bg_color = "#fff3e0" if is_boss else "#e3f2fd"
                                st.markdown(f"""
                                <div style='background: {bg_color}; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;'>
                                    <strong>{icon} {log['author_name']}</strong><br>
                                    {log['content']}
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        # Progress update
                        if t['status'] != "Finished":
                            st.markdown("**📝 Log Progress Update:**")
                            note = st.text_area("What have you done?", key=f"note_{t['id']}", placeholder="Describe your progress...")
                            if st.button("📤 Submit Update", key=f"btn_{t['id']}", use_container_width=True):
                                if note:
                                    supabase.table("FollowupsTable").insert({
                                        "task_id": t['id'],
                                        "author_name": curr_user["name"],
                                        "content": note
                                    }).execute()
                                    st.success("✅ Progress logged!")
                                    st.rerun()
                                else:
                                    st.warning("Please write an update")
            else:
                st.info("📭 You have no active tasks. Use the 'Create' tab to start a new one.")
