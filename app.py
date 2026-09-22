import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS (Modern UI)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Urbanwavve Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Dark Theme Core Background */
    .stApp {
        background-color: #0b0e14;
        color: #e6e8eb;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Input Field Labels - Bright & Bold */
    .stMarkdown label, label, div[data-testid="stWidgetLabel"] p {
        color: #f1f5f9 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }

    /* Modern Rounded Input Fields */
    .stTextInput>div>div>input {
        border-radius: 14px !important;
        background-color: #121721 !important;
        color: #ffffff !important;
        border: 1px solid #2a3447 !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3) !important;
    }

    /* All Buttons Styling (Rounded & Blue Gradient) */
    .stButton>button {
        border-radius: 14px !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.25) !important;
    }
    .stButton>button:hover {
        opacity: 0.95 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0px 6px 16px rgba(37, 99, 235, 0.4) !important;
    }

    /* Inactive Toggle Button Style */
    .inactive-btn button {
        background: #121721 !important;
        color: #94a3b8 !important;
        border: 1px solid #2a3447 !important;
        box-shadow: none !important;
    }
    .inactive-btn button:hover {
        background: #1a2233 !important;
        color: #ffffff !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #121721 !important;
        border-right: 1px solid #1e2638 !important;
    }

    /* Metrics Cards */
    div[data-testid="stMetric"] {
        background-color: #121721 !important;
        border: 1px solid #2a3447 !important;
        padding: 16px !important;
        border-radius: 16px !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. STATE INITIALIZATION
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'  # 'login' or 'register'

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "username": "ebro12",
        "full_name": "Urbanwavve Admin",
        "phone": "+995 599 00 00 00",
        "profile_pic": None
    }

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {"id": "ORD-101", "customer": "გიორგი გ.", "amount": "120.00 ₾", "status": "აქტიური"},
        {"id": "ORD-102", "customer": "ნიკა ქ.", "amount": "85.00 ₾", "status": "აქტიური"},
        {"id": "ORD-103", "customer": "ანა მ.", "amount": "124.00 ₾", "status": "გაუქმებული"},
    ]


# ---------------------------------------------------------
# 3. AUTHENTICATION PAGE (Login / Register Custom Toggles)
# ---------------------------------------------------------
def show_auth_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-weight: 800; color: #ffffff;'>✨ Business & Order Manager</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px; margin-bottom: 25px;'>მართეთ თქვენი გაყიდვები, შეკვეთები და ფინანსები მარტივად</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.3, 1])
    
    with col2:
        # --- TOP BUTTON TOGGLES ---
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.session_state.auth_mode == 'login':
                if st.button("🔑 შესვლა", key="nav_login", use_container_width=True):
                    pass
            else:
                st.markdown('<div class="inactive-btn">', unsafe_allow_html=True)
                if st.button("🔑 შესვლა", key="nav_login_inact", use_container_width=True):
                    st.session_state.auth_mode = 'login'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
        with btn_col2:
            if st.session_state.auth_mode == 'register':
                if st.button("📝 რეგისტრაცია", key="nav_reg", use_container_width=True):
                    pass
            else:
                st.markdown('<div class="inactive-btn">', unsafe_allow_html=True)
                if st.button("📝 რეგისტრაცია", key="nav_reg_inact", use_container_width=True):
                    st.session_state.auth_mode = 'register'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # --- FORM BODY ---
        if st.session_state.auth_mode == 'login':
            username = st.text_input("მომხმარებლის სახელი ან ელ-ფოსტა", key="login_user")
            password = st.text_input("პაროლი", type="password", key="login_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("სისტემაში შესვლა", key="submit_login", use_container_width=True):
                if username and password:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ გთხოვთ შეავსოთ ყველა ველი!")

        else:
            reg_user = st.text_input("მომხმარებლის სახელი", key="reg_user")
            reg_email = st.text_input("ელ-ფოსტა", key="reg_email")
            reg_phone = st.text_input("ტელეფონის ნომერი", key="reg_phone", placeholder="+995 5XX XX XX XX")
            reg_pass = st.text_input("პაროლი", type="password", key="reg_pass")
            reg_confirm_pass = st.text_input("გაიმეორეთ პაროლი", type="password", key="reg_confirm_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ანგარიშის შექმნა", key="submit_reg", use_container_width=True):
                if not (reg_user and reg_email and reg_phone and reg_pass and reg_confirm_pass):
                    st.error("❌ გთხოვთ შეავსოთ ყველა ველი!")
                elif reg_pass != reg_confirm_pass:
                    st.error("❌ პაროლები ერთმანეთს არ ემთხვევა!")
                else:
                    st.session_state.user_data["username"] = reg_user
                    st.session_state.user_data["phone"] = reg_phone
                    st.success("✅ რეგისტრაცია წარმატებით დასრულდა! გადადით შესვლის გვერდზე.")


# ---------------------------------------------------------
# 4. DASHBOARD PAGE
# ---------------------------------------------------------
def show_dashboard():
    st.title("📊 ფინანსური დეშბორდი")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("სულ შეკვეთა", len(st.session_state.orders))
    c2.metric("შემოსავალი", "329.00 ₾")
    c3.metric("ხარჯი", "163.00 ₾")
    c4.metric("წმინდა მოგება", "166.00 ₾")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📈 შეკვეთების გადანაწილება ეტაპების მიხედვით")
    
    chart_data = pd.DataFrame(
        {"რაოდენობა": [3, 5, 2, 8]},
        index=["მიღებული", "მუშავდება", "გაგზავნილი", "დასრულებული"]
    )
    st.bar_chart(chart_data, color="#3b82f6")


# ---------------------------------------------------------
# 5. PROFILE & ORDER MANAGEMENT PAGE
# ---------------------------------------------------------
def show_profile_page():
    st.title("👤 პროფილის და მონაცემების მართვა")
    
    tab1, tab2 = st.tabs(["⚙️ პირადი პროფილები", "📦 შეკვეთების ანულირება"])
    
    with tab1:
        st.subheader("პროფილის პარამეტრები")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.session_state.user_data["profile_pic"]:
                st.image(st.session_state.user_data["profile_pic"], width=160)
            else:
                st.info("📷 ფოტო არ არის არჩეული")
            uploaded_file = st.file_uploader("ფოტოს შეცვლა", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                st.session_state.user_data["profile_pic"] = uploaded_file
                st.success("ფოტო განახლდა!")
                
        with col2:
            new_name = st.text_input("სახელი და გვარი", value=st.session_state.user_data["full_name"])
            new_phone = st.text_input("საკონტაქტო ნომერი", value=st.session_state.user_data["phone"])
            
            st.markdown("<hr style='border-color: #2a3447;'>", unsafe_allow_html=True)
            st.subheader("🔒 პაროლის შეცვლა")
            curr_pass = st.text_input("მიმდინარე პაროლი", type="password")
            new_pass = st.text_input("ახალი პაროლი", type="password")
            confirm_pass = st.text_input("დაადასტურეთ ახალი პაროლი", type="password")
            
            if st.button("ცვლილებების შენახვა"):
                if new_pass and new_pass != confirm_pass:
                    st.error("❌ ახალი პაროლები ერთმანეთს არ ემთხვევა!")
                else:
                    st.session_state.user_data["full_name"] = new_name
                    st.session_state.user_data["phone"] = new_phone
                    st.success("მონაცემები წარმატებით შენახულია!")

    with tab2:
        st.subheader("შეკვეთების სტატუსები და გაუქმება")
        df = pd.DataFrame(st.session_state.orders)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        active_orders = [o["id"] for o in st.session_state.orders if o["status"] == "აქტიური"]
        if active_orders:
            order_to_cancel = st.selectbox("აირჩიეთ შეკვეთა გაუქმებისთვის/ანულირებისთვის:", active_orders)
            if st.button("❌ შეკვეთის ანულირება"):
                for order in st.session_state.orders:
                    if order["id"] == order_to_cancel:
                        order["status"] = "გაუქმებული"
                st.success(f"შეკვეთა {order_to_cancel} წარმატებით გაუქმდა!")
                st.rerun()
        else:
            st.info("აქტიური შეკვეთები არ არის.")


# ---------------------------------------------------------
# 6. MAIN ROUTER & SIDEBAR MENU
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_auth_page()
else:
    with st.sidebar:
        st.markdown("<h3 style='margin-bottom: 20px; color: #ffffff;'>🌐 Urbanwavve</h3>", unsafe_allow_html=True)
        
        page = st.radio(
            "მენიუ",
            ["📊 დეშბორდი", "📦 შეკვეთები", "👤 პროფილის მართვა"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("🚪 გასვლა", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if page == "📊 დეშბორდი":
        show_dashboard()
    elif page == "📦 შეკვეთები":
        st.title("📦 შეკვეთები")
        st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)
    elif page == "👤 პროფილის მართვა":
        show_profile_page()
