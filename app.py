import streamlit as st
from supabase import create_client
import pandas as pd
from datetime import datetime

# ==========================================
# 1. DATABASE CONNECTION
# ==========================================
URL = st.secrets["URL"]
KEY = st.secrets["KEY"]

supabase = create_client(URL, KEY)

# Page Setup
st.set_page_config(page_title="Work Followup Pro", layout="wide")

# ==========================================
# 2. LOGIN SYSTEM
# ==========================================
if "user" not in st.session_state:
    st.title("🏢 Organization Work Tracker")
    st.subheader("Please Login")
    
    with st.form("login_form"):
        user_name = st.text_input("Your Full Name")
        user_password = st.text_input("Password", type="password") 
        submit = st.form_submit_button("Enter System")
        
        if submit:
            if user_name and user_password:
                # Fetch user from Supabase
                res = supabase.table("UsersTable").select("*").eq("full_name", user_name).eq("password", user_password).execute()
                
                if res.data:
                    user_data = res.data[0]
                    # Save exact role and name to session
                    st.session_state.user = {
                        "name": user_data["full_name"], 
                        "role": str(user_data["role"]).strip()
                    }
                    st.success(f"Welcome back, {user_data['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid Name or Password.")
            else:
                st.warning("Please enter both Name and Password.")
    st.stop() 

else:
    curr_user = st.session_state.user
    st.sidebar.title(f"👤 {curr_user['name']}")
    st.sidebar.info(f"Role: {curr_user['role']}")
    
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.rerun()

    # ==========================================
    # 3. BOSS VIEW
    # ==========================================
    if curr_user["role"].lower() == "boss":
        st.title("👨‍💼 Management Control Center")
        
        response = supabase.table("TasksTable").select("*").execute()
        all_tasks = response.data

        if all_tasks:
            df = pd.DataFrame(all_tasks)
            for index, row in df.iterrows():
                p_val = row.get('priority', 'Medium')
                prio_color = "🔴" if p_val == "High" else "🟡" if p_val == "Medium" else "🟢"
                
                with st.container(border=True):
                    col_info, col_action = st.columns([3, 1])
                    with col_info:
                        st.subheader(f"{prio_color} {row['title']}")
                        st.markdown(f"**Assigned to:** `{row['assigned_to']}` | **Deadline:** `{row['deadline']}`")
                        st.write(f"**Status:** {row['status']}")
                        
                        f_res = supabase.table("FollowupsTable").select("content").eq("task_id", row['id']).order("id", desc=True).limit(1).execute()
                        if f_res.data:
                            st.info(f"**Latest Update:** {f_res.data[0]['content']}")

                    with col_action:
                        try:
                            p_idx = ["Low", "Medium", "High"].index(p_val)
                        except:
                            p_idx = 1
                        new_prio = st.selectbox("Priority", ["Low", "Medium", "High"], index=p_idx, key=f"p_{row['id']}")
                        if st.button("Update", key=f"b_{row['id']}"):
                            supabase.table("TasksTable").update({"priority": new_prio}).eq("id", row['id']).execute()
                            st.rerun()
                    
                    with st.expander("💬 Add Comment"):
                        msg = st.text_area("Note:", key=f"m_{row['id']}")
                        if st.button("Send", key=f"s_{row['id']}"):
                            supabase.table("FollowupsTable").insert({
                                "task_id": row['id'], "author_name": f"BOSS: {curr_user['name']}", "content": msg
                            }).execute()
                            st.success("Note added!")
        else:
            st.info("No tasks found in the database.")

    # ==========================================
    # 4. STAFF VIEW (FIXED VERSION)
    # ==========================================
    else:
        st.title("📋 My Workspace")
        
        tab1, tab2 = st.tabs(["➕ Create New Work", "🔄 Update Progress"])

        with tab1:
            st.subheader("Submit New Task")
            with st.form("new_work_form", clear_on_submit=True):
                title = st.text_input("Task/Project Title")
                due = st.date_input("Deadline")
                prio = st.selectbox("Initial Priority", ["Low", "Medium", "High"])
                submit_btn = st.form_submit_button("Submit to Boss")
            
            # Handle submission OUTSIDE the form
            if submit_btn:
                if title:
                    supabase.table("TasksTable").insert({
                        "title": title,
                        "deadline": str(due),
                        "priority": prio,
                        "status": "Pending",
                        "assigned_to": curr_user["name"]
                    }).execute()
                    st.success("Project submitted successfully!")
                    st.rerun()
                else:
                    st.error("Please provide a title.")

        with tab2:
            st.subheader("Tasks Assigned to Me")
            # Using ilike for case-insensitive matching
            my_res = supabase.table("TasksTable").select("*").ilike("assigned_to", curr_user["name"]).execute()
            my_tasks = my_res.data
            
            if my_tasks:
                for t in my_tasks:
                    status_icon = "✅" if t['status'] == "Finished" else "⏳"
                    with st.expander(f"{status_icon} {t['title']} (Due: {t['deadline']})"):
                        st.write(f"**Current Priority:** {t['priority']}")
                        st.write(f"**Status:** {t['status']}")
                        
                        # Show conversation history
                        history = supabase.table("FollowupsTable").select("*").eq("task_id", t['id']).order("id", desc=True).execute()
                        if history.data:
                            st.caption("--- Recent Activity ---")
                            for log in history.data:
                                st.write(f"**{log['author_name']}:** {log['content']}")
                        
                        st.divider()
                        
                        # Log Progress
                        note = st.text_area("Update your progress...", key=f"note_{t['id']}")
                        if st.button("Log Progress", key=f"btn_{t['id']}"):
                            if note:
                                supabase.table("FollowupsTable").insert({
                                    "task_id": t['id'],
                                    "author_name": curr_user["name"],
                                    "content": note
                                }).execute()
                                st.success("Progress logged!")
                                st.rerun()
                        
                        # Mark as Finished
                        if t['status'] != "Finished":
                            if st.button("Mark as Finished", key=f"fin_{t['id']}"):
                                supabase.table("TasksTable").update({"status": "Finished"}).eq("id", t['id']).execute()
                                st.balloons()
                                st.rerun()
            else:
                st.info("You have no active tasks. Use the 'Create' tab to start.")
