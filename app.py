import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS (Modern / Instagram Style)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Urbanwavve Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0b0e14;
        color: #e6e8eb;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Sidebar Styling (Instagram / Modern Nav) */
    section[data-testid="stSidebar"] {
        background-color: #121721 !important;
        border-right: 1px solid #1e2638;
    }
    section[data-testid="stSidebar"] .stButton>button {
        background-color: transparent;
        color: #a0aec0;
        border: none;
        text-align: left;
        padding: 12px 16px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #1e2638;
        color: #ffffff;
    }

    /* Modern Rounded Tabs (Login / Register & Navigation) */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #121721;
        padding: 6px;
        border-radius: 30px;
        border: 1px solid #1e2638;
    }
    div[data-baseweb="tab"] {
        height: 42px;
        border-radius: 22px;
        color: #a0aec0;
        font-weight: 600;
        padding: 0px 24px;
        border: none !important;
        background-color: transparent;
        transition: all 0.3s ease;
    }
    div[aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        box-shadow: 0px 4px 15px rgba(37, 99, 235, 0.4);
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 14px !important;
        background-color: #121721 !important;
        color: #ffffff !important;
        border: 1px solid #1e2638 !important;
        padding: 12px 16px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* Primary Buttons */
    .stButton>button {
        border-radius: 14px;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #121721;
        border: 1px solid #1e2638;
        padding: 16px;
        border-radius: 16px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. STATE INITIALIZATION
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
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
# 3. AUTHENTICATION PAGE (Login / Register)
# ---------------------------------------------------------
def show_auth_page():
    st.markdown("<h2 style='text-align: center; font-weight: 700;'>✨ Business & Order Manager</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0aec0;'>მართეთ თქვენი გაყიდვები, შეკვეთები და ფინანსები მარტივად</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        auth_tab = st.tabs(["🔑 შესვლა", "📝 რეგისტრაცია"])
        
        with auth_tab[0]:
            st.write(" ")
            username = st.text_input("მომხმარებლის სახელი ან ელ-ფოსტა", key="login_user")
            password = st.text_input("პაროლი", type="password", key="login_pass")
            if st.button("სისტემაში შესვლა", use_container_width=True):
                st.session_state.logged_in = True
                st.rerun()
                
        with auth_tab[1]:
            st.write(" ")
            reg_user = st.text_input("ახალი მომხმარებელი", key="reg_user")
            reg_email = st.text_input("ელ-ფოსტა", key="reg_email")
            reg_pass = st.text_input("ახალი პაროლი", type="password", key="reg_pass")
            if st.button("ანგარიშის შექმნა", use_container_width=True):
                st.success("რეგისტრაცია წარმატებით დასრულდა!")


# ---------------------------------------------------------
# 4. DASHBOARD PAGE
# ---------------------------------------------------------
def show_dashboard():
    st.title("📊 ფინანსური დეშბორდი")
    
    # Quick Info Bar
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("სულ შეკვეთა", len(st.session_state.orders))
    c2.metric("შემოსავალი", "329.00 ₾")
    c3.metric("ხარჯი", "163.00 ₾")
    c4.metric("წმინდა მოგება", "166.00 ₾")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📈 შეკვეთების გადანაწილება ეტაპების მიხედვით")
    
    # Built-in Streamlit Chart (No Plotly needed)
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
            
            st.markdown("<hr style='border-color: #1e2638;'>", unsafe_allow_html=True)
            st.subheader("🔒 პაროლის შეცვლა")
            curr_pass = st.text_input("მიმდინარე პაროლი", type="password")
            new_pass = st.text_input("ახალი პაროლი", type="password")
            confirm_pass = st.text_input("დაადასტურეთ ახალი პაროლი", type="password")
            
            if st.button("ცვლილებების შენახვა"):
                st.session_state.user_data["full_name"] = new_name
                st.session_state.user_data["phone"] = new_phone
                st.success("მონაცემები წარმატებით შენახულია!")

    with tab2:
        st.subheader("შეკვეთების სტატუსები და გაუქმება")
        df = pd.DataFrame(st.session_state.orders)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        order_to_cancel = st.selectbox(
            "აირჩიეთ შეკვეთა გაუქმებისთვის/ანულირებისთვის:",
            [o["id"] for o in st.session_state.orders if o["status"] == "აქტიური"]
        )
        if st.button("❌ შეკვეთის ანულირება"):
            for order in st.session_state.orders:
                if order["id"] == order_to_cancel:
                    order["status"] = "გაუქმებული"
            st.success(f"შეკვეთა {order_to_cancel} წარმატებით გაუქმდა!")
            st.rerun()


# ---------------------------------------------------------
# 6. MAIN ROUTER & SIDEBAR MENU
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_auth_page()
else:
    # Sidebar Navigation (Instagram/Modern Style)
    with st.sidebar:
        st.markdown("<h3 style='margin-bottom: 20px;'>🌐 Urbanwavve</h3>", unsafe_allow_html=True)
        
        page = st.radio(
            "მენიუ",
            ["📊 დეშბორდი", "📦 შეკვეთები", "👤 პროფილის მართვა"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("🚪 გასვლა", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    # Route Page Views
    if page == "📊 დეშბორდი":
        show_dashboard()
    elif page == "📦 შეკვეთები":
        st.title("📦 შეკვეთები")
        st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)
    elif page == "👤 პროფილის მართვა":
        show_profile_page()
