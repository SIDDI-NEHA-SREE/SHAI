import os
import sys
# Resolve sys.path for Streamlit Community Cloud deployments
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from utils.ui_helpers import load_global_css, gradient_header
from utils.auth import login_user, register_organization, register_employee, require_role

# Configure page settings
st.set_page_config(
    page_title="ServiceHubAI - Login Portal",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load custom stylesheets
load_global_css()

# Configuration check
from utils.supabase_client import get_env_var
required_keys = ["SUPABASE_URL", "SUPABASE_ANON_KEY", "SUPABASE_SERVICE_ROLE_KEY", "GEMINI_API_KEY"]
missing = [k for k in required_keys if not get_env_var(k)]

if missing:
    gradient_header("ServiceHubAI", "Enterprise AI-Powered Service Desk Platform")
    st.error("### ⚙️ Setup Required")
    st.info("To start using the platform, please configure these settings in Streamlit Secrets or your local environment:")
    for k in missing:
        st.code(f"{k}=your-value")
    st.markdown("For instructions, please check the [README.md](file:///d:/3YR/demo/ServiceHubAI/README.md) file.")
    st.stop()

# Header layout
gradient_header("ServiceHubAI", "Enterprise AI-Powered Service Desk Platform")

# Session routing check (if user is already logged in, redirect them directly to their dashboard)
if "user" in st.session_state and st.session_state["user"]:
    user = st.session_state["user"]
    role = user["role"]
    
    # Active Session Sidebar Controls
    with st.sidebar:
        st.markdown(f"### Logged in:")
        st.caption(f"{user['email']}")
        st.caption(f"Role: {role.upper()}")
        if st.button("Logout Session", use_container_width=True):
            from utils.auth import logout_user
            logout_user()
            
    try:
        if role in ["superadmin", "orgadmin"]:
            st.switch_page("pages/Admin.py")
        elif role == "manager":
            st.switch_page("pages/Manager.py")
        elif role == "agent":
            st.switch_page("pages/Agent.py")
        elif role == "employee":
            st.switch_page("pages/Employee.py")
    except Exception as e:
        st.error(f"Error redirecting to dashboard: {e}")

# Authentication Navigation Tabs
tab_login, tab_reg_org, tab_reg_emp, tab_forgot = st.tabs([
    "🔑 User Login",
    "🏢 Register Organization",
    "👨‍💻 Register Employee",
    "❓ Forgot Password"
])

# =========================================================================
# TAB 1: LOGIN PORTAL
# =========================================================================
with tab_login:
    st.markdown("### Access your Workspace")
    
    portal_type = st.radio(
        "Select Portal System",
        ["Organization Portal", "Super Admin Console"],
        horizontal=True,
        key="login_portal_type"
    )
    
    org_code = ""
    if portal_type == "Organization Portal":
        org_code = st.text_input("Organization Code", placeholder="e.g. ACME", help="Your company registration code").upper().strip()
        
    email = st.text_input("Email Address", placeholder="name@company.com").strip()
    password = st.text_input("Password", type="password", placeholder="••••••••")
    remember_me = st.checkbox("Remember me on this device", value=True)
    
    if st.button("Log In", use_container_width=True):
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            with st.spinner("Authenticating credentials..."):
                if portal_type == "Super Admin Console":
                    success, msg = login_user(email, password, org_code=None)
                else:
                    if not org_code:
                        st.error("Organization code is required.")
                        st.stop()
                    success, msg = login_user(email, password, org_code=org_code)
                
                if success:
                    st.success(msg)
                    # Get user profile and perform switch page
                    user = st.session_state["user"]
                    role = user["role"]
                    if role in ["superadmin", "orgadmin"]:
                        st.switch_page("pages/Admin.py")
                    elif role == "manager":
                        st.switch_page("pages/Manager.py")
                    elif role == "agent":
                        st.switch_page("pages/Agent.py")
                    elif role == "employee":
                        st.switch_page("pages/Employee.py")
                else:
                    st.error(msg)

# =========================================================================
# TAB 2: REGISTER NEW TENANT ORGANIZATION
# =========================================================================
with tab_reg_org:
    st.markdown("### Spin up a new Organization Workspace")
    
    org_name = st.text_input("Organization / Company Name", placeholder="Acme Corporation")
    new_org_code = st.text_input("Organization Short Code", placeholder="e.g. ACME", max_chars=10).upper().strip()
    
    st.markdown("---")
    st.markdown("##### Administrative Account Information")
    
    col1, col2 = st.columns(2)
    with col1:
        admin_first = st.text_input("First Name", key="org_admin_first")
        admin_email = st.text_input("Work Email Address", placeholder="admin@company.com")
    with col2:
        admin_last = st.text_input("Last Name", key="org_admin_last")
        admin_pass = st.text_input("Choose Password", type="password", placeholder="Minimum 6 characters")
        
    if st.button("Register Organization Workspace", use_container_width=True):
        if not org_name or not new_org_code or not admin_email or not admin_pass:
            st.error("Please fill in all mandatory fields.")
        elif len(admin_pass) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            with st.spinner("Provisioning organization database and accounts..."):
                success, msg = register_organization(
                    org_name=org_name,
                    org_code=new_org_code,
                    admin_email=admin_email,
                    admin_password=admin_pass,
                    first_name=admin_first,
                    last_name=admin_last
                )
                if success:
                    st.success(msg)
                    st.balloons()
                else:
                    st.error(msg)

# =========================================================================
# TAB 3: REGISTER AN EMPLOYEE
# =========================================================================
with tab_reg_emp:
    st.markdown("### Join your Organization Portal")
    
    emp_org_code = st.text_input("Company Organization Code", placeholder="e.g. ACME", key="emp_org_code").upper().strip()
    emp_email = st.text_input("Your Work Email", placeholder="employee@company.com", key="emp_email").strip()
    emp_pass = st.text_input("Choose Password", type="password", placeholder="Minimum 6 characters", key="emp_pass")
    
    col_ef, col_el = st.columns(2)
    with col_ef:
        emp_first = st.text_input("First Name", key="emp_first")
    with col_el:
        emp_last = st.text_input("Last Name", key="emp_last")
        
    if st.button("Register Account", use_container_width=True, key="emp_reg_btn"):
        if not emp_org_code or not emp_email or not emp_pass:
            st.error("Please fill in all required registration fields.")
        elif len(emp_pass) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            with st.spinner("Creating profile..."):
                success, msg = register_employee(
                    org_code=emp_org_code,
                    email=emp_email,
                    password=emp_pass,
                    first_name=emp_first,
                    last_name=emp_last
                )
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

# =========================================================================
# TAB 4: PASSWORD RECOVERY (FORGOT PASSWORD)
# =========================================================================
with tab_forgot:
    st.markdown("### Reset your Password")
    st.write("Enter your registered email address below. We'll send you instructions to reset your password.")
    
    forgot_email = st.text_input("Registered Email Address", key="forgot_email").strip()
    
    if st.button("Send Reset Link", use_container_width=True):
        if not forgot_email:
            st.error("Please enter your email address.")
        else:
            from utils.supabase_client import get_supabase
            try:
                supabase = get_supabase()
                supabase.auth.reset_password_for_email(forgot_email)
                st.success("If the email is registered in our system, you will receive a password reset link shortly.")
            except Exception as e:
                st.error(f"Error requesting password reset: {e}")
