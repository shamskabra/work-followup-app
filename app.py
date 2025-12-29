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
    page_title="Al Raed Security - Work Tracker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ENTERPRISE-GRADE CSS
# ==========================================
st.markdown("""
<style>
    /* Enterprise typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, system-ui, sans-serif;
    }
    
    /* Clean professional background */
    .stApp {
        background: #f7fafc;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; max-width: 1200px;}
    
    /* ===== PROFESSIONAL TABS (Dashboard) ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: white;
        border-radius: 8px;
        padding: 0.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #4a5568;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        font-size: 0.9375rem;
        border-radius: 6px;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f7fafc;
        color: #2d3748;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #9f7928;
        color: white;
        font-weight: 600;
    }
    
    /* ===== ENTERPRISE FORM INPUTS ===== */
    .stTextInput > div > div > input {
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9375rem !important;
        background: white !important;
        color: #2d3748 !important;
        transition: all 0.15s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #9f7928 !important;
        box-shadow: 0 0 0 1px #9f7928 !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a0aec0 !important;
        font-weight: 400 !important;
    }
    
    /* Remove labels - we use placeholders */
    .stTextInput > label {
        display: none !important;
    }
    
    /* ===== ENTERPRISE BUTTON ===== */
    .stButton > button {
        background: #9f7928 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.9375rem !important;
        font-weight: 600 !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
        letter-spacing: 0.3px !important;
    }
    
    .stButton > button:hover {
        background: #8a6a24 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    .stButton > button:active {
        background: #7a5d20 !important;
    }
    
    /* ===== PROFESSIONAL BADGES ===== */
    .priority-high, .priority-medium, .priority-low,
    .status-pending, .status-finished {
        padding: 0.35rem 0.75rem;
        border-radius: 4px;
        font-weight: 500;
        font-size: 0.8125rem;
        display: inline-block;
        letter-spacing: 0.2px;
    }
    
    .priority-high { background: #fed7d7; color: #9b2c2c; border: 1px solid #fc8181; }
    .priority-medium { background: #feebc8; color: #9c4221; border: 1px solid #f6ad55; }
    .priority-low { background: #c6f6d5; color: #22543d; border: 1px solid #68d391; }
    .status-pending { background: #bee3f8; color: #2c5282; border: 1px solid #4299e1; }
    .status-finished { background: #c6f6d5; color: #22543d; border: 1px solid #68d391; }
    
    /* ===== HEADER CARD (Dashboard) ===== */
    .main-header {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1);
        border-left: 3px solid #9f7928;
    }
    
    .company-name {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.3px;
    }
    
    .company-tagline {
        color: #718096;
        font-size: 0.875rem;
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }
    
    /* ===== ELEGANT SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] * {
        color: #2d3748 !important;
    }
    
    [data-testid="stSidebar"] h3 {
        font-weight: 600 !important;
        color: #1a202c !important;
        font-size: 1.1rem !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #4a5568 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: #e53e3e !important;
        color: white !important;
        border-radius: 6px !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #c53030 !important;
    }
    
    /* Sidebar metrics with proper contrast */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #9f7928 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #4a5568 !important;
    }
    
    /* ===== CONTAINERS ===== */
    .stContainer, div[data-testid="stContainer"] {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    /* ===== METRICS ===== */
    [data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 6px;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stMetricValue"] {
        color: #9f7928 !important;
        font-size: 1.875rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #718096 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }
    
    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-weight: 500;
        color: #2d3748;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #cbd5e0;
    }
    
    /* ===== ALERTS ===== */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 6px !important;
        border-left-width: 3px !important;
        font-size: 0.9375rem !important;
    }
    
    /* ===== GENERAL TEXT ===== */
    h1 { color: #2d3748; font-weight: 600; letter-spacing: -0.3px; }
    h2, h3 { color: #2d3748; font-weight: 600; }
    p { color: #4a5568; line-height: 1.6; }
    
    /* ===== SELECT BOXES ===== */
    .stSelectbox > div > div > select {
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        padding: 0.75rem 1rem !important;
        background: white !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #9f7928 !important;
        box-shadow: 0 0 0 1px #9f7928 !important;
    }
    
    /* ===== TEXT AREA ===== */
    .stTextArea > div > div > textarea {
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9375rem !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #9f7928 !important;
        box-shadow: 0 0 0 1px #9f7928 !important;
    }
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        border: 1px dashed #cbd5e0;
        border-radius: 6px;
        padding: 1.5rem;
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
    col1, col2 = st.columns([1, 8])
    with col1:
        try:
            logo = Image.open("logo_alraed_Security.png")
            st.image(logo, width=60)  # Smaller logo
        except:
            st.markdown("🛡️")
    
    with col2:
        st.markdown("""
        <div style='padding: 0.5rem 0;'>
            <h1 style='color: #2d3748; font-size: 1.5rem; font-weight: 600; margin: 0; letter-spacing: -0.3px;'>
                Al Raed Security
            </h1>
            <p style='color: #718096; font-size: 0.875rem; margin: 0.2rem 0 0 0; font-weight: 400;'>
                Work Management System
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

# ==========================================
# LOGIN / REGISTRATION SYSTEM
# ==========================================
if "user" not in st.session_state:
    # Add special class for login tabs
    st.markdown("""
    <style>
        /* Override for login page tabs only */
        body:not(.logged-in) .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: transparent !important;
            border: none !important;
            border-bottom: 1px solid #e2e8f0 !important;
            justify-content: center;
            border-radius: 0 !important;
            padding: 0 !important;
        }
        
        body:not(.logged-in) .stTabs [data-baseweb="tab"] {
            background: transparent !important;
            color: #718096;
            font-weight: 500;
            padding: 0.875rem 2rem;
            border-bottom: 2px solid transparent;
            border-radius: 0 !important;
        }
        
        body:not(.logged-in) .stTabs [data-baseweb="tab"]:hover {
            background: transparent !important;
            color: #2d3748;
            border-bottom-color: #cbd5e0;
        }
        
        body:not(.logged-in) .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: transparent !important;
            color: #2d3748;
            font-weight: 600;
            border-bottom-color: #9f7928;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Compact enterprise header
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <div style='margin-bottom: 1rem;'>
            <img src='data:image/png;base64,{}' width='60' style='opacity: 0.9;'/>
        </div>
        <h1 style='color: #2d3748; font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0 0.2rem 0; letter-spacing: -0.3px;'>
            Al Raed Security
        </h1>
        <p style='color: #718096; font-size: 0.875rem; margin: 0; font-weight: 400;'>
            Work Management System
        </p>
    </div>
    """.format(base64.b64encode(open("logo_alraed_Security.png", "rb").read()).decode() if os.path.exists("logo_alraed_Security.png") else ""), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enterprise tabs
    login_tab, register_tab = st.tabs(["Login", "Request Access"])
    
    # ==========================================
    # LOGIN TAB - ENTERPRISE DESIGN
    # ==========================================
    with login_tab:
        col1, col2, col3 = st.columns([1, 2.5, 1])
        
        with col2:
            # Professional login card - no header, just form
            st.markdown("""
            <div style='
                background: white;
                padding: 2rem 2.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
                margin-top: 0.5rem;
            '></div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: -1rem;'></div>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                user_username = st.text_input("", placeholder="Username or Email", label_visibility="collapsed")
                user_password = st.text_input("", type="password", placeholder="Password", label_visibility="collapsed")
                
                col_check, col_forgot = st.columns([1, 1])
                with col_check:
                    remember = st.checkbox("Remember me", value=False)
                with col_forgot:
                    st.markdown("<p style='text-align: right; margin-top: 0.5rem;'><a href='#' style='color: #9f7928; text-decoration: none; font-size: 0.875rem; font-weight: 500;'>Forgot Password?</a></p>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Sign In", use_container_width=True)
                
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
                                    st.session_state.user = {
                                        "name": user_data["full_name"], 
                                        "role": str(user_data["role"]).strip()
                                    }
                                    st.success(f"Welcome, {user_data['full_name']}")
                                    st.rerun()
                            else:
                                st.error("Invalid credentials")
                        except Exception as e:
                            st.error("Authentication failed")
                    else:
                        st.warning("Please enter both fields")
    
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
                reg_username = st.text_input("🔑 Username *", placeholder="Choose a short username (e.g., mshams, john.doe)", 
                                             help="This will be used for login. Keep it short and simple.")
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
                    if reg_name and reg_username:
                        try:
                            # Check if username already exists
                            existing_user = supabase.table("UsersTable").select("*").eq("username", reg_username).execute()
                            existing_name = supabase.table("UsersTable").select("*").eq("full_name", reg_name).execute()
                            
                            if existing_user.data:
                                st.error(f"❌ Username '{reg_username}' is already taken. Please choose a different one.")
                            elif existing_name.data:
                                st.error(f"❌ The name '{reg_name}' is already registered. Please use a different name or contact admin.")
                            else:
                                # Generate temporary password
                                temp_password = generate_temp_password()
                                
                                # Insert into UsersTable with pending status
                                new_user = {
                                    "full_name": reg_name,
                                    "username": reg_username,
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
                            error_msg = str(e)
                            if "username" in error_msg.lower() and "does not exist" in error_msg.lower():
                                st.error("❌ Database Error: The 'username' column doesn't exist yet!")
                                st.warning("⚠️ Admin needs to add the 'username' column to UsersTable in Supabase first.")
                                st.info("""
                                **Setup Required:**
                                1. Go to Supabase → Table Editor → UsersTable
                                2. Click "+ Add Column"
                                3. Name: `username`, Type: `text`
                                4. Check "Is Unique" and Uncheck "Is Nullable"
                                5. Save and try again
                                """)
                            else:
                                st.error(f"❌ Registration failed: {error_msg}")
                    else:
                        st.error("❌ Please provide both your full name and username")
    
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
        
        # Password Change in Sidebar for all users
        with st.expander("🔒 Change Password"):
            with st.form("sidebar_password_form"):
                curr_pass = st.text_input("Current Password", type="password", key="sidebar_curr_pass")
                new_pass = st.text_input("New Password", type="password", key="sidebar_new_pass")
                conf_pass = st.text_input("Confirm Password", type="password", key="sidebar_conf_pass")
                
                if st.form_submit_button("Change", use_container_width=True):
                    if not (curr_pass and new_pass and conf_pass):
                        st.error("Fill all fields")
                    elif new_pass != conf_pass:
                        st.error("Passwords don't match")
                    elif len(new_pass) < 6:
                        st.error("Min 6 characters")
                    else:
                        try:
                            user_data = supabase.table("UsersTable").select("*").eq("full_name", curr_user["name"]).execute()
                            if user_data.data and user_data.data[0]['password'] == curr_pass:
                                supabase.table("UsersTable").update({"password": new_pass}).eq("id", user_data.data[0]['id']).execute()
                                st.success("Password changed!")
                            else:
                                st.error("Wrong password")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
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
                                    st.markdown(f"**🔑 Username:** `{user.get('username', 'N/A')}`")
                                    st.markdown(f"**📧 Email:** {user.get('email', 'N/A')}")
                                    st.markdown(f"**📱 Phone:** {user.get('phone', 'N/A')}")
                                    st.markdown(f"**🏢 Department:** {user.get('department', 'N/A')}")
                                    st.markdown(f"**💼 Position:** {user.get('position', 'N/A')}")
                                    if user.get('notes'):
                                        st.markdown(f"**📝 Notes:** {user.get('notes')}")
                                    st.caption(f"Requested: {user.get('requested_at', 'N/A')}")
                                
                                with col2:
                                    # Check if this user was just approved
                                    just_approved_key = f"approved_{user['id']}"
                                    
                                    if st.button("✅ Approve", key=f"approve_{user['id']}", use_container_width=True):
                                        supabase.table("UsersTable").update({"status": "active"}).eq("id", user['id']).execute()
                                        # Store approval info in session state
                                        st.session_state[just_approved_key] = {
                                            "name": user['full_name'],
                                            "username": user.get('username', 'N/A'),
                                            "password": user['password']
                                        }
                                        st.rerun()
                                    
                                    if st.button("❌ Reject", key=f"reject_{user['id']}", use_container_width=True):
                                        supabase.table("UsersTable").update({"status": "rejected"}).eq("id", user['id']).execute()
                                        st.warning(f"❌ {user['full_name']} rejected")
                                        st.rerun()
                        
                        # Show recently approved users with passwords
                        st.markdown("---")
                        if any(key.startswith("approved_") for key in st.session_state.keys()):
                            st.markdown("### 🔑 Recently Approved Users")
                            for key in list(st.session_state.keys()):
                                if key.startswith("approved_"):
                                    info = st.session_state[key]
                                    with st.container(border=True):
                                        st.success(f"✅ **{info['name']}** was approved!")
                                        st.code(f"Name: {info['name']}\nUsername: {info['username']}\nPassword: {info['password']}", language="text")
                                        st.warning("⚠️ Copy these credentials now! Share them with the user securely.")
                                        if st.button("✔️ Done - Clear This", key=f"clear_{key}"):
                                            del st.session_state[key]
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
                                    st.markdown(f"**🔑 Username:** `{user.get('username', 'N/A')}`")
                                    st.markdown(f"**📧 Email:** {user.get('email', 'N/A')}")
                                    st.markdown(f"**📱 Phone:** {user.get('phone', 'N/A')}")
                                    st.markdown(f"**🏢 Department:** {user.get('department', 'N/A')}")
                                    st.markdown(f"**💼 Position:** {user.get('position', 'N/A')}")
                                    st.markdown(f"**👔 Role:** {user.get('role', 'staff')}")
                                    
                                    # Show password button
                                    show_pass_key = f"show_pass_{user['id']}"
                                    if show_pass_key not in st.session_state:
                                        st.session_state[show_pass_key] = False
                                    
                                    if st.button("👁️ Show Password", key=f"showpw_{user['id']}"):
                                        st.session_state[show_pass_key] = not st.session_state[show_pass_key]
                                    
                                    if st.session_state[show_pass_key]:
                                        st.code(f"Name: {user['full_name']}\nUsername: {user.get('username', 'N/A')}\nPassword: {user['password']}", language="text")
                                        st.caption("⚠️ Keep this confidential")
                                
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
    # STAFF VIEW
    # ==========================================
    else:
        st.title("📋 My Workspace")
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["➕ Create New Task", "🔄 My Active Tasks", "🔒 Change Password"])

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
        
        # ==========================================
        # PASSWORD CHANGE TAB
        # ==========================================
        with tab3:
            st.markdown("### 🔒 Change Your Password")
            st.info("💡 Choose a strong password to keep your account secure.")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                with st.form("change_password_form", clear_on_submit=True):
                    st.markdown("#### Enter New Password")
                    
                    current_password = st.text_input("🔑 Current Password", type="password", 
                                                    placeholder="Enter your current password")
                    new_password = st.text_input("🆕 New Password", type="password", 
                                                 placeholder="Enter new password")
                    confirm_password = st.text_input("✅ Confirm New Password", type="password", 
                                                     placeholder="Re-enter new password")
                    
                    change_btn = st.form_submit_button("🔄 Change Password", use_container_width=True)
                    
                    if change_btn:
                        if not (current_password and new_password and confirm_password):
                            st.error("❌ Please fill in all fields")
                        elif new_password != confirm_password:
                            st.error("❌ New passwords don't match!")
                        elif len(new_password) < 6:
                            st.warning("⚠️ Password should be at least 6 characters long")
                        elif current_password == new_password:
                            st.warning("⚠️ New password must be different from current password")
                        else:
                            # Verify current password
                            try:
                                # Get current user's data
                                user_data = supabase.table("UsersTable").select("*").eq("full_name", curr_user["name"]).execute()
                                
                                if user_data.data:
                                    stored_password = user_data.data[0]['password']
                                    user_id = user_data.data[0]['id']
                                    
                                    if stored_password == current_password:
                                        # Update password
                                        supabase.table("UsersTable").update({"password": new_password}).eq("id", user_id).execute()
                                        st.success("✅ Password changed successfully!")
                                        st.info("🔐 Please remember your new password. You'll need it for your next login.")
                                        st.balloons()
                                    else:
                                        st.error("❌ Current password is incorrect")
                                else:
                                    st.error("❌ User not found")
                            except Exception as e:
                                st.error(f"❌ Error changing password: {str(e)}")
                
                st.markdown("---")
                st.markdown("""
                <div style='background: #fff3e0; padding: 1rem; border-radius: 8px; border-left: 4px solid #ff9800;'>
                    <h4 style='margin: 0 0 0.5rem 0; color: #e65100;'>🔐 Password Tips:</h4>
                    <ul style='margin: 0; padding-left: 1.5rem;'>
                        <li>Use at least 6 characters</li>
                        <li>Mix letters, numbers, and symbols</li>
                        <li>Don't use common words or personal info</li>
                        <li>Don't share your password with anyone</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
