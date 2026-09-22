import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. PAGE CONFIG & DEEP DARK NEON THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Urbanwavve Manager",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* მთლიანი აპლიკაციის ფონი და ძირითადი ტექსტი */
    .stApp {
        background: #0B0414 !important;
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* ყველა სათაურისა და ტექსტის თეთრად იძულება */
    h1, h2, h3, h4, h5, h6, span, label, div, p {
        color: #FFFFFF !important;
    }

    /* კარლასების დიზაინი (Glassmorphism) */
    .glass-card {
        background: #150A24 !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .glass-card-glow {
        background: #1B0E30 !important;
        border: 2px solid #A855F7 !important;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.25);
    }

    /* შეყვანის ველები (Inputs & Selects) */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background-color: #0F071D !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(168, 85, 247, 0.5) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #C084FC !important;
        box-shadow: 0 0 10px rgba(192, 132, 252, 0.4) !important;
    }

    /* ფოტოს ასატვირთი ველის სრული გადაფარვა და სტილიზაცია */
    div[data-testid="stFileUploader"] {
        background-color: #150A24 !important;
        border: 2px dashed #A855F7 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    div[data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }
    div[data-testid="stFileUploader"] span, div[data-testid="stFileUploader"] small {
        color: #E9D5FF !important;
    }
    div[data-testid="stFileUploader"] button {
        background: #A855F7 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    /* მთავარი ღილაკების სტილი */
    .stButton>button {
        width: 100%;
        border-radius: 10px !important;
        background: linear-gradient(135deg, #A855F7 0%, #7E22CE 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 10px 20px !important;
        box-shadow: 0px 4px 15px rgba(168, 85, 247, 0.3) !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    /* საიდბარის ფონი */
    section[data-testid="stSidebar"] {
        background-color: #08030F !important;
        border-right: 1px solid rgba(168, 85, 247, 0.2) !important;
    }

    /* ტაბების სტილი */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #150A24;
        border-radius: 8px;
        color: #E9D5FF !important;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: #A855F7 !important;
        color: #FFFFFF !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. SQLITE DATABASE SETUP
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            customer_name TEXT,
            price REAL,
            cost REAL,
            address TEXT,
            phone TEXT,
            shipping_fee REAL,
            product_name TEXT,
            status TEXT,
            shipping_paid INTEGER,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    return sqlite3.connect("database.db")


# ---------------------------------------------------------
# 3. SESSION STATE
# ---------------------------------------------------------
if 'registered_user' not in st.session_state:
    st.session_state.registered_user = {
        "email": "admin@urbanwavve.ge",
        "phone": "599000000",
        "business_name": "Urbanwavve",
        "business_type": "ონლაინ მაღაზია",
        "password": "password123"
    }

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True

if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'


def add_notification(text):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notifications (text, created_at) VALUES (?, ?)", 
              (text, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def load_orders():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM orders ORDER BY rowid DESC", conn)
    conn.close()
    return df


# ---------------------------------------------------------
# 4. AUTHENTICATION PAGE
# ---------------------------------------------------------
def show_auth_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-weight: 800;'>⚡ Urbanwavve Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #C084FC; font-size: 16px; margin-bottom: 35px;'>მართეთ გაყიდვები და შეკვეთები</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        if b1.button("🔑 შესვლა", key="btn_login_tab"):
            st.session_state.auth_mode = 'login'
            st.rerun()
        if b2.button("📝 რეგისტრაცია", key="btn_reg_tab"):
            st.session_state.auth_mode = 'register'
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.auth_mode == 'login':
            login_id = st.text_input("ნომერი ან ელ-ფოსტა", key="login_id")
            login_pass = st.text_input("პაროლი", type="password", key="login_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("სისტემაში შესვლა", key="btn_login_submit"):
                reg = st.session_state.registered_user
                if (login_id == reg["email"] or login_id == reg["phone"]) and login_pass == reg["password"]:
                    st.session_state.logged_in = True
                    add_notification("🔑 სისტემაში წარმატებით შეხვედით")
                    st.rerun()
                else:
                    st.error("❌ არასწორი ნომერი/ელ-ფოსტა ან პაროლი!")
        else:
            reg_email = st.text_input("ელ-ფოსტა", key="reg_email")
            reg_phone = st.text_input("საკონტაქტო ნომერი", key="reg_phone")
            reg_b_name = st.text_input("ბიზნესის დასახელება", key="reg_b_name")
            reg_b_type = st.selectbox("ბიზნესის სახეობა", ["ონლაინ მაღაზია", "ოჯახის მაღაზია", "შიდა გაყიდვები", "საბითუმო ვაჭრობა"])
            reg_pass = st.text_input("პაროლი", type="password", key="reg_pass")
            reg_confirm = st.text_input("გაიმეორეთ პაროლი", type="password", key="reg_confirm")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ანგარიშის შექმნა", key="btn_reg_submit"):
                if reg_pass != reg_confirm:
                    st.error("❌ პაროლები არ ემთხვევა!")
                else:
                    st.session_state.registered_user = {
                        "email": reg_email, "phone": reg_phone,
                        "business_name": reg_b_name, "business_type": reg_b_type,
                        "password": reg_pass
                    }
                    add_notification("🎉 ახალი ანგარიში დარეგისტრირდა")
                    st.success("✅ წარმატებით დარეგისტრირდით!")
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 5. DASHBOARD PAGE
# ---------------------------------------------------------
def show_dashboard():
    st.markdown("<h2>📊 ფინანსური დეშბორდი</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    orders_df = load_orders()
    
    if not orders_df.empty:
        total_revenue = orders_df[orders_df['status'] != 'გაუქმებული']['price'].sum()
        total_cost = orders_df[orders_df['status'] != 'გაუქმებული']['cost'].sum()
        total_profit = total_revenue - total_cost
    else:
        total_revenue, total_cost, total_profit = 0.0, 0.0, 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("შემოსავალი", f"{total_revenue:,.2f} ₾")
    c2.metric("გასავალი", f"{total_cost:,.2f} ₾")
    c3.metric("წმინდა მოგება", f"{total_profit:,.2f} ₾")

    st.markdown("<br><hr style='border-color: rgba(168,85,247,0.2);'><br>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_t, col_f = st.columns([3, 1])
    with col_t:
        st.subheader("📈 შემოსავლების დინამიკა")
    with col_f:
        time_frame = st.selectbox("პერიოდი", ["ბოლო 7 დღე", "ბოლო 1 თვე", "ბოლო 3 თვე", "1 წელი"])

    chart_data = pd.DataFrame({
        'დღეები': [f'დღე {i}' for i in range(1, 8)],
        'შემოსავალი (₾)': [total_revenue / 7 * i for i in range(1, 8)]
    }).set_index('დღეები')

    st.line_chart(chart_data, color="#A855F7", height=220)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 6. CREATE ORDER PAGE
# ---------------------------------------------------------
def show_create_order_page():
    st.markdown("<h2>📝 შეკვეთის გაფორმება</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("სახელი", key="ord_name")
        price = st.number_input("ფასი", min_value=0.0, step=5.0, key="ord_price")
        cost = st.number_input("ღირებულება", min_value=0.0, step=5.0, key="ord_cost")
        product_name = st.text_input("პროდუქტი", key="ord_prod")

    with col2:
        shipping_fee = st.number_input("ტრანსპორტირება", min_value=0.0, step=1.0, key="ord_ship")
        address = st.text_input("მისამართი", key="ord_addr")
        phone = st.text_input("ნომერი", key="ord_phone")
        photo = st.file_uploader("ფოტო", type=['png', 'jpg', 'jpeg'], key="ord_photo")

    calculated_profit = price - cost
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-card-glow" style="text-align: center;">
        <h3 style="margin:0; color: #E9D5FF;">💡 მოსალოდნელი წმინდა მოგება რეალურ დროში:</h3>
        <h1 style="margin:10px 0 0 0; color: {'#4ADE80' if calculated_profit >= 0 else '#F87171'}; font-size: 38px;">
            {calculated_profit:,.2f} ₾
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 შეკვეთის ჩანიშვნა და შენახვა", key="btn_save_order"):
        if price > 0 and name and phone:
            conn = get_db_connection()
            c = conn.cursor()
            order_id = f"ORD-{int(datetime.now().timestamp()) % 100000}"
            created_at = datetime.now().strftime("%Y-%m-%d")
            
            c.execute('''
                INSERT INTO orders (id, customer_name, price, cost, address, phone, shipping_fee, product_name, status, shipping_paid, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (order_id, name, price, cost, address, phone, shipping_fee, product_name, "გაფორმებული", 0, created_at))
            
            conn.commit()
            conn.close()
            
            add_notification(f"📦 ახალი შეკვეთა #{order_id} გაფორმდა ({name})")
            st.success(f"✅ შეკვეთა #{order_id} წარმატებით შენახულია ბაზაში!")
        else:
            st.error("❌ გთხოვთ შეავსოთ აუცილებელი ველები: სახელი, ფასი და ნომერი!")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 7. ORDERS MANAGEMENT PAGE
# ---------------------------------------------------------
def show_orders_page():
    st.markdown("<h2>📦 შეკვეთების მართვა</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    orders_df = load_orders()

    st_g = len(orders_df[orders_df['status'] == 'გაფორმებული']) if not orders_df.empty else 0
    st_c = len(orders_df[orders_df['status'] == 'ჩამოსულია']) if not orders_df.empty else 0
    st_f = len(orders_df[orders_df['status'] == 'ჩაბარებული']) if not orders_df.empty else 0

    col_a, col_b, col_c = st.columns(3)
    col_a.info(f"📥 გაფორმებული: **{st_g}**")
    col_b.warning(f"🛬 ჩამოსულია: **{st_c}**")
    col_c.success(f"✅ ჩაბარებული: **{st_f}**")

    st.markdown("<br>", unsafe_allow_html=True)
    tabs = st.tabs(["📥 1. გაფორმებული", "🛬 2. ჩამოსულია", "✅ 3. ჩაბარებული"])

    conn = get_db_connection()
    c = conn.cursor()

    with tabs[0]:
        g_orders = orders_df[orders_df['status'] == 'გაფორმებული'] if not orders_df.empty else pd.DataFrame()
        if g_orders.empty:
            st.info("გაფორმებული შეკვეთები არ არის.")
        else:
            for _, row in g_orders.iterrows():
                st.markdown(f"""
                <div class="glass-card">
                    <h3><b>#{row['id']}</b> — {row['customer_name']} ({row['phone']})</h3>
                    <p><b>მისამართი:</b> {row['address']} | <b>ფასი:</b> {row['price']} ₾ | <b>ღირებულება:</b> {row['cost']} ₾</p>
                    <p><b>ტრანსპორტირება:</b> {row['shipping_fee']} ₾ | <b>პროდუქტი:</b> {row['product_name']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                b_col1, b_col2 = st.columns([3, 1])
                if b_col1.button(f"გადატანა 'ჩამოსულია'-ში ➡️", key=f"to_c_{row['id']}"):
                    c.execute("UPDATE orders SET status = 'ჩამოსულია' WHERE id = ?", (row['id'],))
                    conn.commit()
                    add_notification(f"🛬 შეკვეთა #{row['id']} ჩამოვიდა")
                    st.rerun()
                if b_col2.button(f"🗑️ წაშლა", key=f"del_{row['id']}"):
                    c.execute("DELETE FROM orders WHERE id = ?", (row['id'],))
                    conn.commit()
                    st.rerun()

    with tabs[1]:
        c_orders = orders_df[orders_df['status'] == 'ჩამოსულია'] if not orders_df.empty else pd.DataFrame()
        if c_orders.empty:
            st.info("ჩამოსული შეკვეთები არ არის.")
        else:
            for _, row in c_orders.iterrows():
                st.markdown(f"""
                <div class="glass-card">
                    <h3><b>#{row['id']}</b> — {row['customer_name']}</h3>
                    <p><b>გასახდელი ტრანსპორტირების თანხა:</b> <span style="color:#A855F7; font-weight:bold; font-size:18px;">{row['shipping_fee']} ₾</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                is_paid = st.checkbox(f"ტრანსპორტირების თანხა გადახდილია ({row['shipping_fee']} ₾)", value=bool(row['shipping_paid']), key=f"pay_{row['id']}")
                if is_paid != bool(row['shipping_paid']):
                    c.execute("UPDATE orders SET shipping_paid = ? WHERE id = ?", (1 if is_paid else 0, row['id']))
                    conn.commit()

                b_col1, b_col2 = st.columns([3, 1])
                if b_col1.button(f"გადატანა 'ჩაბარებული'-ში ➡️", key=f"to_f_{row['id']}"):
                    if not is_paid:
                        st.error("❌ ვერ გადაიტანთ ჩაბარებულში, სანამ ტრანსპორტირების თანხა არ აღინიშნება გადახდილად!")
                    else:
                        c.execute("UPDATE orders SET status = 'ჩაბარებული' WHERE id = ?", (row['id'],))
                        conn.commit()
                        add_notification(f"✅ შეკვეთა #{row['id']} ჩაბარდა")
                        st.rerun()
                if b_col2.button(f"🗑️ წაშლა", key=f"del_c_{row['id']}"):
                    c.execute("DELETE FROM orders WHERE id = ?", (row['id'],))
                    conn.commit()
                    st.rerun()

    with tabs[2]:
        f_orders = orders_df[orders_df['status'] == 'ჩაბარებული'] if not orders_df.empty else pd.DataFrame()
        if f_orders.empty:
            st.info("ჩაბარებული შეკვეთები არ არის.")
        else:
            for _, row in f_orders.iterrows():
                st.markdown(f"""
                <div class="glass-card-glow">
                    <h3><b>#{row['id']}</b> — {row['customer_name']} (დასრულებული ✅)</h3>
                    <p><b>სრული შემოსავალი:</b> {row['price']} ₾ | <b>მოგება:</b> {row['price'] - row['cost']} ₾</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🗑️ შეკვეთის წაშლა ბაზიდან", key=f"del_f_{row['id']}"):
                    c.execute("DELETE FROM orders WHERE id = ?", (row['id'],))
                    conn.commit()
                    st.rerun()

    conn.close()


# ---------------------------------------------------------
# 8. NOTIFICATIONS & PROFILE PAGES
# ---------------------------------------------------------
def show_notifications_page():
    st.markdown("<h2>🔔 ნოტიფიკაციები</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    conn = get_db_connection()
    notifs = pd.read_sql_query("SELECT * FROM notifications ORDER BY id DESC", conn)
    conn.close()

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if notifs.empty:
        st.write("ნოტიფიკაციები არ არის.")
    else:
        for _, n in notifs.iterrows():
            st.markdown(f"• **{n['text']}** <br><small style='color:#C084FC;'>{n['created_at']}</small><hr style='border-color: rgba(168,85,247,0.1);'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_profile_page():
    st.markdown("<h2>👤 პროფილის პარამეტრები</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    reg = st.session_state.registered_user

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    new_b_name = st.text_input("ბიზნესის დასახელება", value=reg["business_name"], key="prof_b_name")
    new_email = st.text_input("ელ-ფოსტა", value=reg["email"], key="prof_email")
    new_phone = st.text_input("საკონტაქტო ნომერი", value=reg["phone"], key="prof_phone")
    
    st.markdown("<hr style='border-color: rgba(168,85,247,0.2);'>", unsafe_allow_html=True)
    curr_pass = st.text_input("მიმდინარე პაროლი", type="password", key="prof_curr_pass")
    new_pass = st.text_input("ახალი პაროლი", type="password", key="prof_new_pass")

    if st.button("💾 ცვლილებების შენახვა", key="btn_save_profile"):
        if curr_pass and curr_pass != reg["password"]:
            st.error("❌ მიმდინარე პაროლი არასწორია!")
        else:
            reg["business_name"] = new_b_name
            reg["email"] = new_email
            reg["phone"] = new_phone
            if new_pass:
                reg["password"] = new_pass
            add_notification("👤 პროფილის მონაცემები განახლდა")
            st.success("✅ მონაცემები წარმატებით განახლდა!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="glass-card" style="border: 1px solid rgba(239, 68, 68, 0.4) !important;">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #F87171 !important;'>⚠️ საშიში ზონა (მონაცემების განულება)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #E9D5FF;'>ყველა შეკვეთისა და ნოტიფიკაციის სამუდამოდ წაშლა ბაზიდან.</p>", unsafe_allow_html=True)
    
    if st.button("🗑️ ყველა შეკვეთის და მონაცემის განულება", key="btn_clear_all"):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM orders")
        c.execute("DELETE FROM notifications")
        conn.commit()
        conn.close()
        add_notification("⚠️ სისტემის ყველა მონაცემი განულდა")
        st.success("✅ ბაზა წარმატებით განულდა!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 9. MAIN ROUTER & NAVIGATION
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_auth_page()
else:
    with st.sidebar:
        st.markdown("<h2 style='color: #C084FC; font-weight: 800;'>🔮 Urbanwavve</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#E9D5FF;'>{st.session_state.registered_user['business_name']}</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(168,85,247,0.2);'>", unsafe_allow_html=True)
        
        page = st.radio(
            "მენიუ",
            ["📊 დეშბორდი", "📝 შეკვეთის გაფორმება", "📦 შეკვეთების მართვა", "🔔 ნოტიფიკაციები", "👤 პროფილი"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 გასვლა", key="btn_logout"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "📊 დეშბორდი":
        show_dashboard()
    elif page == "📝 შეკვეთის გაფორმება":
        show_create_order_page()
    elif page == "📦 შეკვეთების მართვა":
        show_orders_page()
    elif page == "🔔 ნოტიფიკაციები":
        show_notifications_page()
    elif page == "👤 პროფილი":
        show_profile_page()
