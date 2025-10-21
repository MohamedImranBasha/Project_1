import streamlit as st
import pandas as pd
import numpy as np
import hashlib
from datetime import datetime
import mysql.connector
from mysql.connector import Error


# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'client_queries_mgmt'
}

# Database Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

# Password Hashing
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Database Setup
def setup_database():
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # queries table    
        cursor.execute("""CREATE TABLE IF NOT EXISTS queries (
                          query_id INT AUTO_INCREMENT PRIMARY KEY,
                          client_name TEXT NOT NULL,
                          email_id VARCHAR(255),
                          mobile_number VARCHAR(20),
                          query_heading TEXT,
                          query_text TEXT NOT NULL,
                          status VARCHAR(50) NOT NULL,
                          priority VARCHAR(50) NOT NULL,
                          submitted_on DATE NOT NULL,
                          submitted_time TIME NOT NULL,
                          resolved_on DATE,
                          resolved_time TIME,
                          assigned_to TEXT)""")

        # users table
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                          user_id INT AUTO_INCREMENT PRIMARY KEY,
                          username VARCHAR(50) UNIQUE NOT NULL,
                          password VARCHAR(255) NOT NULL,
                          role VARCHAR(20) NOT NULL DEFAULT 'client')""")

        # Insert default users
        default_users = {
            "support_admin": ("support123", "support"),
            "client_user": ("client123", "client")
        }
        for username, (password, role) in default_users.items():
            hashed_pw = hash_password(password)
            try:
                cursor.execute("""
                     INSERT INTO users (username, password, role)
                     VALUES (%s, %s, %s)
                """, (username, hashed_pw, role))
            except Error:
                pass
                
        # Load queries from CSV only if the table is empty
        try:
            csv_url = "https://drive.google.com/uc?id=1KNDcf56n6gUf_zla4uLJqELVFb_c8mDi&export=download"
            df_csv = pd.read_csv(csv_url)
            df_csv = df_csv.replace({np.nan: None})
            
            cursor.execute("SELECT COUNT(*) FROM queries")
            result = cursor.fetchone()[0]
                    
            if result == 0:
                insert_query_stmt = """
                    INSERT INTO queries (client_name, email_id, mobile_number, query_heading, query_text, status, priority,
                                          submitted_on, submitted_time, resolved_on, resolved_time, assigned_to)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                for _, row in df_csv.iterrows():
                    data = (
                        row['client_name'], row['email_id'], row['mobile_number'], 
                        row['query_heading'], row['query_text'], row['status'], 
                        row['priority'], row['submitted_on'], row['submitted_time'], 
                        row['resolved_on'], row['resolved_time'], row['assigned_to']
                    )
                    try:
                        cursor.execute(insert_query_stmt, data)
                    except mysql.connector.Error as err:
                        st.warning(f"Error importing row: {err}")
                conn.commit()
        except Exception as e:
            st.warning(f"Could not load CSV: {e}")
        
        conn.commit()
        cursor.close()
        
    except Error as e:
        st.error(f"Database setup error: {e}")
    finally:
        if conn.is_connected():
            conn.close()

# Query Functions
def get_queries_from_db():
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        query = "SELECT * FROM queries ORDER BY query_id DESC"
        df = pd.read_sql(query, conn)
        
        if not df.empty:
            df['submitted_on'] = pd.to_datetime(df['submitted_on'], errors='coerce').dt.date
            df['resolved_on'] = pd.to_datetime(df['resolved_on'], errors='coerce').dt.date
        return df
    except Error as e:
        st.error(f"Error fetching queries: {e}")
        return pd.DataFrame()
    finally:
        if conn.is_connected():
            conn.close()
    
def add_new_query(client_name, email_id, mobile_number, query_heading, query_text, priority, uploaded_file=None):
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        now = datetime.now()
        submitted_on = now.date()
        submitted_time = now.time()
        status = "Open"
        
        cursor.execute('''
            INSERT INTO queries (client_name, email_id, mobile_number, query_heading, query_text, status, priority, submitted_on, submitted_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
            client_name, 
            email_id if email_id else None, 
            mobile_number if mobile_number else None, 
            query_heading if query_heading else None, 
            query_text, 
            status, 
            priority, 
            submitted_on, 
            submitted_time
        ))
        
        conn.commit()
        cursor.close()
        return True, "Query submitted successfully!"
    except Error as e:
        return False, f"Error submitting query: {e}"
    finally:
        if conn.is_connected():
            conn.close()

def update_query_status(query_id, new_status, assigned_to):
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        now = datetime.now()
        resolved_on = now.date() if new_status == "Resolved" else None 
        resolved_time = now.time() if new_status == "Resolved" else None
        
        cursor.execute('''UPDATE queries
                          SET status = %s, resolved_on = %s, resolved_time = %s, assigned_to = %s
                          WHERE query_id = %s''', (
            new_status, 
            resolved_on, 
            resolved_time, 
            assigned_to if assigned_to else None, 
            query_id
        ))
        
        conn.commit()
        cursor.close()
        return True, "Query updated successfully!"
    except Error as e:
        return False, f"Error updating query: {e}"
    finally:
        if conn.is_connected():
            conn.close()

# User Authentication
def register_user(username, password, role="client"):
    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed"
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            return False, "Username already exists!"
        
        hashed_pw = hash_password(password)
        cursor.execute('''INSERT INTO users (username, password, role) VALUES (%s, %s, %s)''', (
            username, 
            hashed_pw, 
            role
        ))
        
        conn.commit()
        cursor.close()
        return True, "Registration successful! Please log in."
    except Error as e:
        return False, f"Registration error: {e}"
    finally:
        if conn.is_connected():
            conn.close()
    
def authenticate_user(username, password, role):
    conn = get_db_connection()
    if not conn:
        return False, None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s AND role = %s", (username, role))
        result = cursor.fetchone()
        cursor.close()
        
        if result and result[0] == hash_password(password):
            return True, role
        return False, None
    except Error as e:
        st.error(f"Authentication error: {e}")
        return False, None
    finally:
        if conn.is_connected():
            conn.close()

# Streamlit Configuration
st.set_page_config(
    page_title="Client Query Management System", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📋"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None

# Login & Register UI
def login_and_register_ui():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #1F2937;'>🔐 Client Query Management System</h1>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<h5 style='color: black; text-align: center;'>Organizing, Tracking, and Closing Support Queries📝</h5>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""<style>
        div.stForm{
            background-color:#F9FAFB;
            padding:40px;
            border-radius:12px;
            box-shadow:0 12px 30px rgba(0,0,0,0.5);
        }  
        .stTextInput>div>div>input, .stSelectbox>div>div>div{
            background-color: white;
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
        }
        .stButton>button{
            background-color: #3B82F6;
            color: white;
            border-radius: 8px;
            padding: 12px 24px;
            width: 100%;
        }
        </style>""", unsafe_allow_html=True)
        
        choice = st.radio("Choose an option:", ["Login", "Register"], horizontal=True, label_visibility="collapsed")


        if choice == "Login":
            with st.form("login_form"):
                st.markdown("<h3 style='color: black; text-align: center;'>Welcome Back! 👋</h3>", unsafe_allow_html=True)
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                role = st.selectbox("Role", ["client", "support"])
                submitted = st.form_submit_button("🚀 Log In")
                
                if submitted:
                    if not username or not password:
                        st.error("Please enter both username and password.")
                    else:
                        success, user_role = authenticate_user(username, password, role)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_role = user_role
                            st.session_state.username = username
                            st.success(f"Welcome {username}! Role: {user_role}")
                            st.rerun()
                        else:
                            st.error("Invalid credentials.")
        else:
            with st.form("register_form"):
                st.markdown("<h3 style='color: black; text-align: center;'>Register 📝</h3>", unsafe_allow_html=True)
                new_username = st.text_input("Username", placeholder="Choose a username", key="reg_user")
                new_password = st.text_input("Password", type="password", placeholder="Create a password (min 6 chars)", key="reg_pass")
                confirm_pw = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_conf")
                submitted = st.form_submit_button("✨ Register")
                
                if submitted:
                    if not new_username or not new_password or not confirm_pw:
                        st.error("⚠️ Please fill in all fields")
                    elif new_password != confirm_pw:
                        st.error("❌ Passwords do not match!")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        success, msg = register_user(new_username, new_password)
                        if success:
                            st.success(f"✅ {msg}")
                            st.balloons()
                        else:
                            st.error(f"❌ {msg}")

def logout_button():
    if st.sidebar.button("🚪 Log Out", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.username = None
        st.success("Logged out successfully!")
        st.rerun()

# Main Application
def main():
    if not st.session_state.logged_in:
        login_and_register_ui()
    else:
        st.write(f"Welcome, **{st.session_state.username}** ({st.session_state.user_role})")
        logout_button()
        
        if st.session_state.user_role == "client":
            client_dashboard()
        elif st.session_state.user_role == "support":
            support_dashboard()

def client_dashboard():
    st.markdown("""
     <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
         <h1 style='color: white; text-align: center; margin: 0;'>📋 Client Submission Dashboard</h1>
     </div>
     """, unsafe_allow_html=True)
    
    # Submit Query Section
    st.subheader("Submit a New Query")
    with st.form("new_query_form"):
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Your Name*")
            email_id = st.text_input("Email")
        with col2:
            mobile_number = st.text_input("Mobile Number")
            priority = st.selectbox("Priority*", ["Low", "Medium", "High"])
        
        query_heading = st.text_input("Query Heading*")
        query_text = st.text_area("Query Details*", height=150)
        
        submitted = st.form_submit_button("🚀 Submit Query", use_container_width=True)
        
        if submitted:
            if client_name and query_text:
                success, msg = add_new_query(client_name, email_id, mobile_number, query_heading, query_text, priority)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Please fill in required fields (Name and Query Details)")
    
    st.markdown("---")
    
    # View Queries Section
    st.subheader("Your Queries")
    df = get_queries_from_db()
    if not df.empty:
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.info("No queries found.")

def support_dashboard():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>🛠️ Support Team Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # All Queries Section
    st.subheader("All Queries")
    df = get_queries_from_db()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No queries found.")
    
    st.markdown("---")
    
    # Update Status Section
    st.subheader("Update Query Status")
    col1, col2 = st.columns(2)
    with col1:
        query_id = st.number_input("Query ID*", min_value=1, step=1)
        new_status = st.selectbox("New Status*", ["Open", "In Progress", "Resolved"])
    with col2:
        assigned_to = st.text_input("Assigned To")
    
    if st.button("💾 Update Query", use_container_width=True, type="primary"):
        if query_id:
            success, msg = update_query_status(query_id, new_status, assigned_to)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        else:
            st.error("Please enter a valid Query ID")

# Run the application
if __name__ == "__main__":
    try:
        setup_database()
    except Exception as e:
        st.error(f"Database setup error: {e}")
        st.stop()
    main()