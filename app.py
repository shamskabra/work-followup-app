import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime
from PIL import Image
import base64
import secrets
import string

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
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #2c3e50 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #34495e !important;
    }
    
    /* Pending badge */
    .badge-pending {
        background: #ffeaa7;
        color: #d63031;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.75rem;
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
    """Generate a random temporary password"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_file_icon(file_type):
    """Return appropriate emoji for file type"""
    icons = {
        'pdf': '📄',
        'doc': '📝', 'docx': '📝',
        'xls': '📊', 'xlsx': '📊',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️', 'webp': '🖼️',
        'zip': '📦', 'rar': '📦',
        'txt': '📃',
        'default': '📎'
    }
    extension = file_type.lower().replace('.', '')
    return icons.get(extension, icons['default'])

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def save_file_to_database(file, task_id, uploaded_by):
    """Save file to database as base64"""
    try:
        file_bytes = file.read()
        file_name = file.name
        file_size = len(file_bytes)
        file_type = file.type
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')
        
        file_record = {
            "task_id": task_id,
            "file_name": file_name,
            "file_type": file_type,
            "file_size": file_size,
            "file_data": file_base64,
            "uploaded_by": uploaded_by,
            "uploaded_at": datetime.now().isoformat()
        }
        
        result = supabase.table("TaskFilesTable").insert(file_record).execute()
        return True, "File uploaded successfully!"
    except Exception as e:
        return False, f"Upload failed: {str(e)}"

def get_task_files(task_id):
    """Get all files for a task"""
    try:
        response = supabase.table("TaskFilesTable").select("*").eq("task_id", task_id).order("uploaded_at", desc=False).execute()
        return response.data if response.data else []
    except:
        return []

def create_download_link(file_data, file_name, file_type):
    """Create a download link for base64 file data"""
    try:
        b64 = file_data
        href = f'<a href="data:{file_type};base64,{b64}" download="{file_name}" style="text-decoration: none; background-color: #3498db; color: white; padding: 0.3rem 0.8rem; border-radius: 5px; font-size: 0.85rem;">📥 Download</a>'
        return href
    except:
        return '<span style="color: red;">Download Error</span>'

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
# LOGIN / REGISTRATION SYSTEM
# ==========================================
if "user" not in st.session_state:
    show_header()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create tabs for Login and Registration
    login_tab, register_tab = st.tabs(["🔐 Login", "📝 Request Access"])
    
    # ==========================================
    # LOGIN TAB
    # ==========================================
    with login_tab:
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
                            
                            # Check if account is active
                            if user_data.get("status") == "pending":
                                st.warning("⏳ Your account is pending approval. Please wait for admin to activate your account.")
                            elif user_data.get("status") == "rejected":
                                st.error("❌ Your account request was rejected. Please contact administration.")
                            else:
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
    
    # ==========================================
    # REGISTRATION TAB
    # ==========================================
    with register_tab:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
                <h2 style='text-align: center; color: #6B5644; margin-bottom: 2rem;'>📝 Request Access</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("📋 Fill in the form below. Your request will be reviewed by management.")
            
            with st.form("registration_form", clear_on_submit=True):
                st.markdown("#### Your Information")
                
                reg_name = st.text_input("👤 Full Name *", placeholder="Enter your full name")
                reg_email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
                reg_phone = st.text_input("📱 Phone Number", placeholder="+965 XXXX XXXX")
                reg_department = st.selectbox("🏢 Department", 
                    ["Security Operations", "Administration", "Technical", "HR", "Finance", "Other"])
                reg_position = st.text_input("💼 Position/Role", placeholder="e.g. Security Guard, Manager")
                reg_notes = st.text_area("📝 Additional Notes (Optional)", 
                    placeholder="Any additional information you'd like to share...")
                
                col_x, col_y, col_z = st.columns([1, 2, 1])
                with col_y:
                    register_btn = st.form_submit_button("📤 Submit Request", use_container_width=True)
                
                if register_btn:
                    if reg_name:
                        # Check if name already exists
                        existing = supabase.table("UsersTable").select("*").eq("full_name", reg_name).execute()
                        
                        if existing.data:
                            st.error("❌ This name is already registered. Please use a different name or contact admin.")
                        else:
                            # Generate temporary password
                            temp_password = generate_temp_password()
                            
                            # Insert into UsersTable with pending status
                            try:
                                new_user = {
                                    "full_name": reg_name,
                                    "password": temp_password,
                                    "role": "staff",  # Default role
                                    "status": "pending",  # Pending approval
                                    "email": reg_email,
                                    "phone": reg_phone,
                                    "department": reg_department,
                                    "position": reg_position,
                                    "notes": reg_notes,
                                    "requested_at": datetime.now().isoformat()
                                }
                                
                                result = supabase.table("UsersTable").insert(new_user).execute()
                                
                                st.success("✅ Request submitted successfully!")
                                st.info("""
                                📋 **What's Next?**
                                1. Your request has been sent to management
                                2. You will be notified once approved
                                3. You'll receive your login credentials from admin
                                4. Please wait for approval before attempting to login
                                """)
                                st.balloons()
                            except Exception as e:
                                st.error(f"❌ Registration failed: {str(e)}")
                    else:
                        st.error("❌ Please provide at least your full name")
    
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
                
                # Get pending user requests
                pending_users = supabase.table("UsersTable").select("*").eq("status", "pending").execute().data
                if pending_users:
                    st.markdown("---")
                    st.warning(f"⏳ {len(pending_users)} pending user request(s)")
            else:
                my_tasks = supabase.table("TasksTable").select("*").ilike("assigned_to", curr_user["name"]).execute().data
                pending = len([t for t in my_tasks if t.get('status') == 'Pending'])
                finished = len([t for t in my_tasks if t.get('status') == 'Finished'])
            
            st.metric("⏳ Pending Tasks", pending)
            st.metric("✅ Finished Tasks", finished)
        except:
            pass

    # ==========================================
    # BOSS VIEW WITH USER MANAGEMENT
    # ==========================================
    if curr_user["role"].lower() == "boss":
        st.title("👨‍💼 Management Control Center")
        
        # Main tabs
        main_tabs = st.tabs(["📋 Tasks Management", "👥 User Management"])
        
        # ==========================================
        # TASKS TAB (existing functionality)
        # ==========================================
        with main_tabs[0]:
            st.markdown("---")
            
            response = supabase.table("TasksTable").select("*").execute()
            all_tasks = response.data

            if all_tasks:
                # Get unique staff members
                df = pd.DataFrame(all_tasks)
                staff_list = ["All"] + sorted(df['assigned_to'].unique().tolist())
                
                # Filter options
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    filter_staff = st.selectbox("👤 Filter by Staff", staff_list)
                with col2:
                    filter_status = st.selectbox("📋 Filter by Status", ["All", "Pending", "Finished"])
                with col3:
                    filter_priority = st.selectbox("🎯 Filter by Priority", ["All", "High", "Medium", "Low"])
                with col4:
                    sort_by = st.selectbox("📊 Sort by", ["Deadline", "Priority", "Status"])
                
                # Apply filters
                if filter_staff != "All":
                    df = df[df['assigned_to'] == filter_staff]
                if filter_status != "All":
                    df = df[df['status'] == filter_status]
                if filter_priority != "All":
                    df = df[df['priority'] == filter_priority]
                
                # Apply sorting
                if sort_by == "Deadline":
                    df = df.sort_values('deadline')
                elif sort_by == "Priority":
                    priority_order = {"High": 1, "Medium": 2, "Low": 3}
                    df['priority_num'] = df['priority'].map(priority_order)
                    df = df.sort_values('priority_num')
                    df = df.drop('priority_num', axis=1)
                elif sort_by == "Status":
                    df = df.sort_values('status')
                
                st.markdown(f"**Showing {len(df)} task(s)**")
                st.markdown("---")
                
                if len(df) == 0:
                    st.info("📭 No tasks match the selected filters.")
                else:
                    for index, row in df.iterrows():
                        p_val = row.get('priority', 'Medium')
                        
                        if p_val == "High":
                            priority_badge = '<span class="priority-high">🔴 HIGH PRIORITY</span>'
                        elif p_val == "Medium":
                            priority_badge = '<span class="priority-medium">🟡 MEDIUM</span>'
                        else:
                            priority_badge = '<span class="priority-low">🟢 LOW</span>'
                        
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
                                
                                f_res = supabase.table("FollowupsTable").select("content, author_name").eq("task_id", row['id']).order("id", desc=True).limit(1).execute()
                                if f_res.data:
                                    st.markdown(f"**💬 Latest Update ({f_res.data[0]['author_name']}):** {f_res.data[0]['content']}")
                                
                                task_files = get_task_files(row['id'])
                                if task_files:
                                    st.markdown(f"**📎 Attachments ({len(task_files)}):**")
                                    for file in task_files:
                                        icon = get_file_icon(file['file_name'].split('.')[-1])
                                        col_file, col_dl = st.columns([3, 1])
                                        with col_file:
                                            st.markdown(f"{icon} **{file['file_name']}** ({format_file_size(file['file_size'])}) - by {file['uploaded_by']}")
                                        with col_dl:
                                            download_link = create_download_link(file['file_data'], file['file_name'], file['file_type'])
                                            st.markdown(download_link, unsafe_allow_html=True)

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
                            
                            with st.expander("💬 Add Comment / Upload Files"):
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
                                
                                st.markdown("---")
                                st.markdown("**📎 Upload Files**")
                                uploaded_files = st.file_uploader(
                                    "Choose files", 
                                    accept_multiple_files=True,
                                    key=f"boss_upload_{row['id']}",
                                    help="Upload PDFs, images, documents, etc."
                                )
                                
                                if uploaded_files:
                                    if st.button("⬆️ Upload Files", key=f"upload_boss_{row['id']}"):
                                        for uploaded_file in uploaded_files:
                                            success, message = save_file_to_database(uploaded_file, row['id'], curr_user['name'])
                                            if success:
                                                st.success(f"✅ {uploaded_file.name} uploaded!")
                                            else:
                                                st.error(f"❌ {message}")
                                        st.rerun()
            else:
                st.info("📭 No tasks found in the system.")
        
        # ==========================================
        # USER MANAGEMENT TAB
        # ==========================================
        with main_tabs[1]:
            st.markdown("---")
            st.subheader("👥 User Management")
            
            # Get all users
            all_users = supabase.table("UsersTable").select("*").execute().data
            
            if all_users:
                # Separate by status
                pending_users = [u for u in all_users if u.get('status') == 'pending']
                active_users = [u for u in all_users if u.get('status') != 'pending' and u.get('status') != 'rejected']
                rejected_users = [u for u in all_users if u.get('status') == 'rejected']
                
                user_tabs = st.tabs([f"⏳ Pending ({len(pending_users)})", 
                                    f"✅ Active ({len(active_users)})", 
                                    f"❌ Rejected ({len(rejected_users)})"])
                
                # Pending Users Tab
                with user_tabs[0]:
                    if pending_users:
                        st.info(f"📋 {len(pending_users)} user(s) waiting for approval")
                        
                        for user in pending_users:
                            with st.container(border=True):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.markdown(f"### 👤 {user['full_name']}")
                                    st.markdown(f"**📧 Email:** {user.get('email', 'N/A')}")
                                    st.markdown(f"**📱 Phone:** {user.get('phone', 'N/A')}")
                                    st.markdown(f"**🏢 Department:** {user.get('department', 'N/A')}")
                                    st.markdown(f"**💼 Position:** {user.get('position', 'N/A')}")
                                    if user.get('notes'):
                                        st.markdown(f"**📝 Notes:** {user.get('notes')}")
                                    st.caption(f"Requested: {user.get('requested_at', 'N/A')}")
                                
                                with col2:
                                    if st.button("✅ Approve", key=f"approve_{user['id']}", use_container_width=True):
                                        supabase.table("UsersTable").update({"status": "active"}).eq("id", user['id']).execute()
                                        st.success(f"✅ {user['full_name']} approved!")
                                        st.info(f"🔑 Temporary Password: `{user['password']}`\n\nShare this with the user securely.")
                                        st.rerun()
                                    
                                    if st.button("❌ Reject", key=f"reject_{user['id']}", use_container_width=True):
                                        supabase.table("UsersTable").update({"status": "rejected"}).eq("id", user['id']).execute()
                                        st.warning(f"❌ {user['full_name']} rejected")
                                        st.rerun()
                    else:
                        st.info("✅ No pending requests")
                
                # Active Users Tab
                with user_tabs[1]:
                    if active_users:
                        st.success(f"✅ {len(active_users)} active user(s)")
                        
                        for user in active_users:
                            with st.expander(f"👤 {user['full_name']} - {user.get('role', 'staff').upper()}"):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown(f"**📧 Email:** {user.get('email', 'N/A')}")
                                    st.markdown(f"**📱 Phone:** {user.get('phone', 'N/A')}")
                                    st.markdown(f"**🏢 Department:** {user.get('department', 'N/A')}")
                                    st.markdown(f"**💼 Position:** {user.get('position', 'N/A')}")
                                    st.markdown(f"**👔 Role:** {user.get('role', 'staff')}")
                                
                                with col2:
                                    new_role = st.selectbox("Change Role", ["staff", "boss"], 
                                                          index=0 if user.get('role') == 'staff' else 1,
                                                          key=f"role_{user['id']}")
                                    if st.button("💾 Update Role", key=f"upd_{user['id']}", use_container_width=True):
                                        supabase.table("UsersTable").update({"role": new_role}).eq("id", user['id']).execute()
                                        st.success("Updated!")
                                        st.rerun()
                                    
                                    if st.button("🔄 Reset Password", key=f"reset_{user['id']}", use_container_width=True):
                                        new_pass = generate_temp_password()
                                        supabase.table("UsersTable").update({"password": new_pass}).eq("id", user['id']).execute()
                                        st.success(f"🔑 New Password: `{new_pass}`")
                    else:
                        st.info("No active users found")
                
                # Rejected Users Tab
                with user_tabs[2]:
                    if rejected_users:
                        st.warning(f"❌ {len(rejected_users)} rejected user(s)")
                        
                        for user in rejected_users:
                            with st.expander(f"👤 {user['full_name']}"):
                                st.markdown(f"**📧 Email:** {user.get('email', 'N/A')}")
                                st.markdown(f"**🏢 Department:** {user.get('department', 'N/A')}")
                                
                                if st.button("♻️ Reconsider & Approve", key=f"reapprove_{user['id']}"):
                                    supabase.table("UsersTable").update({"status": "active"}).eq("id", user['id']).execute()
                                    st.success(f"✅ {user['full_name']} approved!")
                                    st.rerun()
                    else:
                        st.info("No rejected users")
            else:
                st.info("No users in the system")

    # ==========================================
    # STAFF VIEW (unchanged from previous version)
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
                        result = supabase.table("TasksTable").insert({
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
                        <li>Upload files after creation</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### 📌 Tasks Assigned to Me")
            
            my_res = supabase.table("TasksTable").select("*").ilike("assigned_to", curr_user["name"]).execute()
            my_tasks = my_res.data
            
            if my_tasks:
                pending_tasks = [t for t in my_tasks if t['status'] != 'Finished']
                finished_tasks = [t for t in my_tasks if t['status'] == 'Finished']
                
                st.markdown(f"**Active Tasks:** {len(pending_tasks)} | **Completed:** {len(finished_tasks)}")
                st.markdown("---")
                
                for t in my_tasks:
                    if t['priority'] == "High":
                        priority_emoji = "🔴"
                    elif t['priority'] == "Medium":
                        priority_emoji = "🟡"
                    else:
                        priority_emoji = "🟢"
                    
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
                        
                        task_files = get_task_files(t['id'])
                        if task_files:
                            st.markdown(f"**📎 Attached Files ({len(task_files)}):**")
                            for file in task_files:
                                icon = get_file_icon(file['file_name'].split('.')[-1])
                                col_file, col_dl = st.columns([3, 1])
                                with col_file:
                                    st.markdown(f"{icon} **{file['file_name']}**")
                                    st.caption(f"{format_file_size(file['file_size'])} - Uploaded by {file['uploaded_by']}")
                                with col_dl:
                                    download_link = create_download_link(file['file_data'], file['file_name'], file['file_type'])
                                    st.markdown(download_link, unsafe_allow_html=True)
                            st.markdown("---")
                        
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
                            
                            st.markdown("---")
                            st.markdown("**📎 Upload Project Files**")
                            st.caption("Upload invoices, quotations, pictures, samples, etc.")
                            
                            uploaded_files = st.file_uploader(
                                "Choose files to upload", 
                                accept_multiple_files=True,
                                key=f"staff_upload_{t['id']}",
                                help="Supported: PDF, Images, Excel, Word, etc."
                            )
                            
                            if uploaded_files:
                                st.info(f"📋 {len(uploaded_files)} file(s) selected")
                                if st.button("⬆️ Upload Files", key=f"upload_staff_{t['id']}", use_container_width=True):
                                    for uploaded_file in uploaded_files:
                                        success, message = save_file_to_database(uploaded_file, t['id'], curr_user['name'])
                                        if success:
                                            st.success(f"✅ {uploaded_file.name} uploaded!")
                                        else:
                                            st.error(f"❌ {message}")
                                    st.rerun()
            else:
                st.info("📭 You have no active tasks. Use the 'Create' tab to start a new one.")
