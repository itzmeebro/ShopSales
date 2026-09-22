import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM CSS (Custom UI + Dynamic Tabs)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Urbanwavve Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0b0e14;
        color: #e6e8eb;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Labels */
    .stMarkdown label, label, div[data-testid="stWidgetLabel"] p {
        color: #f1f5f9 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }

    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div {
        border-radius: 12px !important;
        background-color: #121721 !important;
        color: #ffffff !important;
        border: 1px solid #2a3447 !important;
    }

    /* Base Buttons */
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        opacity: 0.95 !important;
        transform: translateY(-1px) !important;
    }

    /* Auth Active/Inactive Toggles */
    .active-toggle button {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important;
        color: #60a5fa !important;
        font-weight: 800 !important;
        border: 2px solid #2563eb !important;
        box-shadow: 0px 0px 14px rgba(37, 99, 235, 0.4) !important;
    }
    .inactive-toggle button {
        background: #121721 !important;
        color: #64748b !important;
        border: 1px solid #1e2638 !important;
        opacity: 0.65 !important;
    }

    /* Animated Auth Form */
    @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .animated-form {
        animation: fadeInSlide 0.4s ease-out forwards;
    }

    /* Sidebar & Cards */
    section[data-testid="stSidebar"] {
        background-color: #121721 !important;
        border-right: 1px solid #1e2638 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #121721 !important;
        border: 1px solid #2a3447 !important;
        padding: 16px !important;
        border-radius: 16px !important;
    }
    
    /* Order Cards */
    .order-card {
        background-color: #121721;
        border: 1px solid #2a3447;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. STATE INITIALIZATION
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        "🔔 სისტემაში წარმატებით შეხვედით",
        "📦 ახალი შეკვეთა #ORD-104 დაემატა"
    ]

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "username": "ebro12",
        "full_name": "Urbanwavve Admin",
        "phone": "+995 599 00 00 00",
        "profile_pic": None
    }

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {"id": "ORD-101", "customer": "გიორგი გ.", "item": "ჰუდი - Oversized Blue", "amount": 120.0, "status": "მიღებული", "date": "2026-09-22"},
        {"id": "ORD-102", "customer": "ნიკა ქ.", "item": "პერანგი - Poplin White", "amount": 85.0, "status": "მუშავდება", "date": "2026-09-22"},
        {"id": "ORD-103", "customer": "ანა მ.", "item": "შარვალი - Urban Black", "amount": 124.0, "status": "გაგზავნილი", "date": "2026-09-21"},
        {"id": "ORD-104", "customer": "ლუკა ს.", "item": "მაისური - Wavve Print", "amount": 65.0, "status": "დასრულებული", "date": "2026-09-20"},
    ]


# ---------------------------------------------------------
# 3. AUTHENTICATION PAGE
# ---------------------------------------------------------
def show_auth_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-weight: 800; color: #ffffff;'>✨ Business & Order Manager</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px; margin-bottom: 30px;'>მართეთ თქვენი გაყიდვები, შეკვეთები და ფინანსები მარტივად</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        btn_col1, btn_col2 = st.columns(2, gap="small")
        
        with btn_col1:
            if st.session_state.auth_mode == 'login':
                st.markdown('<div class="active-toggle">', unsafe_allow_html=True)
                st.button("🔑 შესვლა", key="nav_login_act", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="inactive-toggle">', unsafe_allow_html=True)
                if st.button("🔑 შესვლა", key="nav_login_inact", use_container_width=True):
                    st.session_state.auth_mode = 'login'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
        with btn_col2:
            if st.session_state.auth_mode == 'register':
                st.markdown('<div class="active-toggle">', unsafe_allow_html=True)
                st.button("📝 რეგისტრაცია", key="nav_reg_act", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="inactive-toggle">', unsafe_allow_html=True)
                if st.button("📝 რეგისტრაცია", key="nav_reg_inact", use_container_width=True):
                    st.session_state.auth_mode = 'register'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="animated-form">', unsafe_allow_html=True)
        
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
                    
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 4. DASHBOARD PAGE (NO GRAPH)
# ---------------------------------------------------------
def show_dashboard():
    st.title("📊 ფინანსური დეშბორდი")
    
    total_orders = len(st.session_state.orders)
    total_income = sum(o["amount"] for o in st.session_state.orders if o["status"] != "გაუქმებული")
    expenses = total_income * 0.4  # სავარაუდო ხარჯი
    net_profit = total_income - expenses

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("სულ შეკვეთა", total_orders)
    c2.metric("შემოსავალი", f"{total_income:.2f} ₾")
    c3.metric("ხარჯი", f"{expenses:.2f} ₾")
    c4.metric("წმინდა მოგება", f"{net_profit:.2f} ₾")
    
    st.markdown("<br><hr style='border-color: #2a3447;'><br>", unsafe_allow_html=True)
    
    st.subheader("🔔 ბოლო აქტივობები & ნოტიფიკაციები")
    for notif in reversed(st.session_state.notifications[-5:]):
        st.info(notif)


# ---------------------------------------------------------
# 5. ORDER MANAGEMENT PAGE (KANBAN + NEW ORDER + NOTIFICATIONS)
# ---------------------------------------------------------
def show_orders_page():
    st.title("📦 შეკვეთების მართვა ეტაპების მიხედვით")
    
    # top row: New Order Modal & Notifications Toggle
    col_add, col_notif = st.columns([2, 1])
    
    with col_add:
        with st.expander("➕ ახალი შეკვეთის დამატება", expanded=False):
            with st.form("add_order_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                cust_name = c1.text_input("მომხმარებლის სახელი")
                item_desc = c2.text_input("პროდუქციის დასახელება")
                item_price = c1.number_input("თანხა (₾)", min_value=0.0, step=5.0)
                init_status = c2.selectbox("საწყისი სტატუსი", ["მიღებული", "მუშავდება"])
                
                if st.form_submit_button("შეკვეთის დამატება"):
                    if cust_name and item_desc and item_price > 0:
                        new_id = f"ORD-10{len(st.session_state.orders) + 1}"
                        st.session_state.orders.append({
                            "id": new_id,
                            "customer": cust_name,
                            "item": item_desc,
                            "amount": item_price,
                            "status": init_status,
                            "date": datetime.now().strftime("%Y-%m-%d")
                        })
                        st.session_state.notifications.append(f"📦 შეიქმნა ახალი შეკვეთა {new_id} - {cust_name}")
                        st.success(f"შეკვეთა {new_id} დაემატა!")
                        st.rerun()
                    else:
                        st.error("გთხოვთ შეავსოთ ყველა ველი!")

    with col_notif:
        with st.expander("🔔 ნოტიფიკაციები", expanded=False):
            for n in reversed(st.session_state.notifications):
                st.caption(n)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for Workflow Stages
    statuses = ["მიღებული", "მუშავდება", "გაგზავნილი", "დასრულებული", "გაუქმებული"]
    tabs = st.tabs([f"📥 {s}" if s=="მიღებული" else f"⚙️ {s}" if s=="მუშავდება" else f"🚚 {s}" if s=="გაგზავნილი" else f"✅ {s}" if s=="დასრულებული" else f"❌ {s}" for s in statuses])

    for idx, status in enumerate(statuses):
        with tabs[idx]:
            filtered_orders = [o for o in st.session_state.orders if o["status"] == status]
            if not filtered_orders:
                st.info(f"ამ ეტაპზე შეკვეთები არ არის ('{status}').")
            else:
                for ord_item in filtered_orders:
                    with st.container():
                        st.markdown(f"""
                        <div class="order-card">
                            <h4><b>{ord_item['id']}</b> — {ord_item['customer']}</h4>
                            <p><b>პროდუქტი:</b> {ord_item['item']} | <b>თანხა:</b> {ord_item['amount']} ₾</p>
                            <p><small style='color: #94a3b8;'>თარიღი: {ord_item['date']}</small></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Dynamic Status Change Buttons
                        c_prev, c_next, c_cancel = st.columns([1, 1, 1])
                        
                        if idx > 0 and status != "გაუქმებული":
                            if c_prev.button(f"⬅️ გადაყვანა {statuses[idx-1]}-ში", key=f"prev_{ord_item['id']}"):
                                ord_item["status"] = statuses[idx-1]
                                st.session_state.notifications.append(f"🔄 {ord_item['id']} გადავიდა ეტაპზე: {statuses[idx-1]}")
                                st.rerun()
                                
                        if idx < 3 and status != "გაუქმებული":
                            if c_next.button(f"გადაყვანა {statuses[idx+1]}-ში ➡️", key=f"next_{ord_item['id']}"):
                                ord_item["status"] = statuses[idx+1]
                                st.session_state.notifications.append(f"🔄 {ord_item['id']} გადავიდა ეტაპზე: {statuses[idx+1]}")
                                st.rerun()
                                
                        if status != "გაუქმებული" and status != "დასრულებული":
                            if c_cancel.button(f"❌ გაუქმება", key=f"canc_{ord_item['id']}"):
                                ord_item["status"] = "გაუქმებული"
                                st.session_state.notifications.append(f"❌ შეკვეთა {ord_item['id']} გაუქმდა")
                                st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 6. PROFILE PAGE
# ---------------------------------------------------------
def show_profile_page():
    st.title("👤 პროფილის და პარამეტრების მართვა")
    
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


# ---------------------------------------------------------
# 7. MAIN ROUTER
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_auth_page()
else:
    with st.sidebar:
        st.markdown("<h3 style='margin-bottom: 20px; color: #ffffff;'>🌐 Urbanwavve</h3>", unsafe_allow_html=True)
        
        page = st.radio(
            "მენიუ",
            ["📊 დეშბორდი", "📦 შეკვეთების მართვა", "👤 პროფილის მართვა"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("🚪 გასვლა", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    if page == "📊 დეშბორდი":
        show_dashboard()
    elif page == "📦 შეკვეთების მართვა":
        show_orders_page()
    elif page == "👤 პროფილის მართვა":
        show_profile_page()
