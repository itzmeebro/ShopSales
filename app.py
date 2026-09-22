import streamlit as st
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime, timedelta
from PIL import Image
import io

# --- გვერდის კონფიგურაცია ---
st.set_page_config(
    page_title="Business & Order Manager",
    page_icon="🛍️",
    layout="wide"
)

# --- SOFT DARK EYES-FRIENDLY THEME & ACCESSIBLE CONTRAST (CSS) ---
st.markdown("""
    <style>
    /* რბილი, თვალისათვის კომფორტული მუქი ფონი */
    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    
    /* SideBar */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* ტექსტის მკაფიო კონტრასტი */
    p, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #f8fafc !important;
    }

    .stCaption {
        color: #94a3b8 !important;
    }
    
    /* ბარათების / კონტეინერების რბილი სტილი */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        transition: all 0.2s ease;
    }
    
    [data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"]:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }

    /* მშვიდი იისფერი/ლურჯი ღილაკები */
    .stButton > button {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #6366f1 !important;
        transform: translateY(-1px);
    }

    /* Input ველები */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
        border: 1px solid #475569 !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
    }

    /* Tabs სტილი */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        background-color: #1e293b;
        color: #94a3b8 !important;
        border: 1px solid #334155;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4f46e5 !important;
        color: #ffffff !important;
        font-weight: 600;
        border: none !important;
    }

    /* Metric ბარათები */
    [data-testid="stMetricValue"] {
        color: #818cf8 !important;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }

    .stAlert {
        border-radius: 8px !important;
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- პაროლის ჰეშირება ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- ბაზის ინიციალიზაცია ---
def init_db():
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            password TEXT,
            business_name TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            item_name TEXT,
            cost_price REAL,
            sale_price REAL,
            profit REAL,
            customer_name TEXT,
            order_date TEXT,
            status TEXT,
            image BLOB,
            shipping_cost REAL DEFAULT 0,
            shipping_paid INTEGER DEFAULT 0,
            address TEXT DEFAULT '',
            phone TEXT DEFAULT ''
        )
    ''')
    
    c.execute("PRAGMA table_info(orders)")
    columns = [col[1] for col in c.fetchall()]
    if 'shipping_cost' not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN shipping_cost REAL DEFAULT 0")
    if 'shipping_paid' not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN shipping_paid INTEGER DEFAULT 0")
    if 'address' not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN address TEXT DEFAULT ''")
    if 'phone' not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN phone TEXT DEFAULT ''")
        
    conn.commit()
    conn.close()

init_db()

# --- ბაზასთან მუშაობის ფუნქციები ---
def add_user(username, email, password, business_name):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users(username, email, password, business_name) VALUES (?,?,?,?)', 
                  (username.strip(), email.strip(), make_hashes(password), business_name.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username_or_email, password):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    input_val = username_or_email.strip()
    c.execute('SELECT username, business_name FROM users WHERE (username = ? OR email = ?) AND password = ?', 
              (input_val, input_val, make_hashes(password)))
    data = c.fetchone()
    conn.close()
    return data

def add_order(username, item_name, cost_price, sale_price, profit, customer_name, phone, address, order_date, image_bytes, shipping_cost):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        INSERT INTO orders (username, item_name, cost_price, sale_price, profit, customer_name, phone, address, order_date, status, image, shipping_cost, shipping_paid)
        VALUES (?,?,?,?,?,?,?,?,?,'გაფორმებული',?,?, 0)
    ''', (username, item_name, cost_price, sale_price, profit, customer_name, phone, address, order_date, image_bytes, shipping_cost))
    conn.commit()
    conn.close()

def get_user_orders(username):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM orders WHERE username = ?", conn, params=(username,))
    conn.close()
    return df

def update_order_status(order_id, new_status):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

def update_shipping_payment(order_id, paid_status):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE orders SET shipping_paid = ? WHERE id = ?", (paid_status, order_id))
    conn.commit()
    conn.close()

def delete_all_user_orders(username):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE username = ?", (username,))
    conn.commit()
    conn.close()

# --- MODAL DIALOG წაშლის დადასტურებისთვის ---
@st.dialog("🚨 შეკვეთების სრული წაშლა")
def confirm_delete_dialog(username):
    st.write("⚠️ **ყურადღება!** ნამდვილად გსურთ ყველა შეკვეთის წაშლა?")
    st.write("ეს მოქმედება **სამუდამოა** და წაშლილი მონაცემების აღდგენა შეუძლებელი იქნება.")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if st.button("❌ გაუქმება", use_container_width=True):
            st.rerun()
    with col_d2:
        if st.button("🗑️ დიახ, წაშლა", type="primary", use_container_width=True):
            delete_all_user_orders(username)
            st.toast("🧹 ყველა შეკვეთა წარმატებით წაიშალა!", icon="✅")
            st.rerun()

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'business_name' not in st.session_state:
    st.session_state['business_name'] = ""

# ==========================================
# 1. ავტორიზაცია / რეგისტრაცია
# ==========================================
if not st.session_state['logged_in']:
    st.title("✨ Business & Order Hub")
    st.caption("მართეთ თქვენი გაყიდვები, შეკვეთები და ფინანსები მოსახერხებელ პანელში.")

    tab1, tab2 = st.tabs(["🔑 შესვლა", "📝 რეგისტრაცია"])

    with tab1:
        st.subheader("სისტემაში შესვლა")
        with st.form("login_form"):
            login_input = st.text_input("მომხმარებლის სახელი ან ელ-ფოსტა")
            login_pass = st.text_input("პაროლი", type='password')
            login_submit = st.form_submit_button("შესვლა", type="primary")

            if login_submit:
                if not login_input or not login_pass:
                    st.warning("გთხოვთ შეავსოთ შესასვლელი ველები.")
                else:
                    user_data = login_user(login_input, login_pass)
                    if user_data:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = user_data[0]
                        st.session_state['business_name'] = user_data[1]
                        st.success(f"მოგესალმებით, {user_data[1]}!")
                        st.rerun()
                    else:
                        st.error("არასწორი მომხმარებლის სახელი/ელ-ფოსტა ან პაროლი.")

    with tab2:
        st.subheader("ახალი ბიზნეს ანგარიშის შექმნა")
        with st.form("register_form"):
            new_business = st.text_input("🏢 მაღაზიის / ბიზნესის სახელწოდება")
            new_email = st.text_input("📧 ელ-ფოსტა")
            new_user = st.text_input("👤 მომხმარებლის სახელი")
            new_pass = st.text_input("🔒 პაროლი", type='password')
            confirm_pass = st.text_input("🔒 დაადასტურეთ პაროლი", type='password')
            
            reg_submit = st.form_submit_button("რეგისტრაცია", type="primary")

            if reg_submit:
                if not new_business.strip() or not new_email.strip() or not new_user.strip() or not new_pass:
                    st.warning("გთხოვთ შეავსოთ ყველა ველი.")
                elif new_pass != confirm_pass:
                    st.error("პაროლები არ ემთხვევა ერთმანეთს.")
                else:
                    if add_user(new_user, new_email, new_pass, new_business):
                        st.success("🎉 რეგისტრაცია წარმატებით დასრულდა! გადადით შესვლის ჩანართზე.")
                    else:
                        st.error("ასეთი მომხმარებელი ან ელ-ფოსტა უკვე არსებობს.")

# ==========================================
# 2. ავტორიზებული მომხმარებლის პანელი
# ==========================================
else:
    col_head1, col_head2 = st.columns([4, 1])
    with col_head1:
        st.title(f"🏢 {st.session_state['business_name']}")
        st.caption(f"👤 მომხმარებელი: `{st.session_state['username']}`")
    with col_head2:
        st.write("")
        if st.button("🚪 გამოსვლა", key="top_logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.session_state['business_name'] = ""
            st.rerun()

    st.markdown("---")

    df_all = get_user_orders(st.session_state['username'])
    notifications = []
    
    if not df_all.empty:
        today = datetime.now().date()
        for idx, row in df_all.iterrows():
            if row['status'] == 'გაფორმებული':
                try:
                    order_dt = datetime.strptime(row['order_date'], "%Y-%m-%d %H:%M:%S").date()
                except:
                    order_dt = datetime.strptime(row['order_date'].split()[0], "%Y-%m-%d").date()
                
                days_passed = (today - order_dt).days
                if days_passed >= 10:
                    notifications.append(f"⚠️ **შეხსენება:** შეკვეთა #{row['id']} ({row['item_name']}) გაფორმდა {days_passed} დღის წინ.")

    menu = ["📊 დეშბორდი & ფინანსები", "➕ ახალი შეკვეთა", "📦 შეკვეთების მართვა", f"🔔 ნოტიფიკაციები ({len(notifications)})"]
    choice = st.sidebar.radio("მენიუ", menu)

    # 📊 1. დეშბორდი
    if choice == "📊 დეშბორდი & ფინანსები":
        st.subheader("📊 ფინანსური დეშბორდი")

        if not df_all.empty:
            df_all['dt'] = pd.to_datetime(df_all['order_date'])
            now = datetime.now()

            # პერიოდის არჩევა დეშბორდის თავზე
            col_p1, col_p2 = st.columns([2, 3])
            with col_p1:
                period = st.selectbox(
                    "📅 აირჩიეთ პერიოდი ფინანსების დასათვლელად:",
                    ["შეწმნიდან დღემდე", "ბოლო 1 კვირა", "ბოლო 1 თვე", "ბოლო 3 თვე", "ბოლო 1 წელი"]
                )

            if period == "ბოლო 1 კვირა":
                df_filtered = df_all[df_all['dt'] >= (now - timedelta(days=7))]
            elif period == "ბოლო 1 თვე":
                df_filtered = df_all[df_all['dt'] >= (now - timedelta(days=30))]
            elif period == "ბოლო 3 თვე":
                df_filtered = df_all[df_all['dt'] >= (now - timedelta(days=90))]
            elif period == "ბოლო 1 წელი":
                df_filtered = df_all[df_all['dt'] >= (now - timedelta(days=365))]
            else:
                df_filtered = df_all

            # ფინანსური მეტრიკები
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📦 სულ შეკვეთა", len(df_filtered))
            c2.metric("💰 შემოსავალი", f"{df_filtered['sale_price'].sum():.2f} ₾")
            c3.metric("📉 ხარჯი", f"{df_filtered['cost_price'].sum():.2f} ₾")
            
            total_profit = df_filtered['profit'].sum()
            c4.metric("✨ წმინდა მოგება", f"{total_profit:.2f} ₾")

            # შეკვეთების გადანაწილების გრაფიკი
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📈 შეკვეთების გადანაწილება ეტაპების მიხედვით")
            if not df_filtered.empty:
                st.bar_chart(df_filtered['status'].value_counts())
            else:
                st.info("არჩეულ პერიოდში შეკვეთები არ მოიძებნა.")

        else:
            st.info("შეკვეთები ჯერ არ არის დაფიქსირებული.")

        st.markdown("<br><hr>", unsafe_allow_html=True)
        
        # --- RESET / გასუფთავების სექცია ---
        st.subheader("⚙️ მონაცემების მართვა")
        col_reset1, col_reset2 = st.columns([3, 1])
        with col_reset1:
            st.caption("ყველა შეკვეთის ბაზიდან წაშლა და დეშბორდის განულება.")
        with col_reset2:
            if st.button("🗑️ შეკვეთების გასუფთავება", type="primary", use_container_width=True):
                confirm_delete_dialog(st.session_state['username'])

    # ➕ 2. ახალი შეკვეთა
    elif choice == "➕ ახალი შეკვეთა":
        st.subheader("➕ ახალი შეკვეთის გაფორმება")

        col1, col2 = st.columns(2)
        
        with col1:
            item_name = st.text_input("📦 პროდუქტის დასახელება")
            customer_name = st.text_input("👤 მყიდველის სახელი და გვარი")
            customer_phone = st.text_input("📞 საკონტაქტო ნომერი")
            customer_address = st.text_area("📍 ჩაბარების მისამართი", height=100)
            uploaded_file = st.file_uploader("🖼️ პროდუქტის ფოტო", type=['png', 'jpg', 'jpeg'])

        with col2:
            sale_price = st.number_input("💰 გასაყიდი ფასი (₾)", min_value=0.0, step=1.0, value=0.0)
            cost_price = st.number_input("📉 თვითღირებულება (₾)", min_value=0.0, step=1.0, value=0.0)
            shipping_cost = st.number_input("✈️ წონა / ტრანსპორტირება (₾)", min_value=0.0, step=0.5, value=0.0)
            
            profit = sale_price - cost_price
            
            if profit > 0:
                st.success(f"💡 მოსალოდნელი მოგება: **+{profit:.2f} ₾**")
            elif profit < 0:
                st.error(f"⚠️ ყურადღება: ზარალი **{profit:.2f} ₾**")
            else:
                st.info("💡 მოსალოდნელი მოგება: **0.00 ₾**")

        st.markdown("---")
        submitted = st.button("✨ შეკვეთის ჩანიშვნა", type="primary")

        if submitted:
            if not item_name.strip() or not customer_name.strip():
                st.warning("გთხოვთ მიუთითოთ პროდუქტი და მყიდველის სახელი/გვარი.")
            else:
                image_bytes = None
                if uploaded_file is not None:
                    image_bytes = uploaded_file.read()

                current_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                add_order(
                    st.session_state['username'],
                    item_name,
                    cost_price,
                    sale_price,
                    profit,
                    customer_name,
                    customer_phone,
                    customer_address,
                    current_now,
                    image_bytes,
                    shipping_cost
                )
                st.success(f"🎉 შეკვეთა წარმატებით ჩაინიშნა! თარიღი: {current_now}")

    # 📦 3. შეკვეთების მართვა
    elif choice == "📦 შეკვეთების მართვა":
        st.subheader("📦 შეკვეთების მართვა & სტატუსები")

        df_gaph = df_all[df_all['status'] == 'გაფორმებული']
        df_chamo = df_all[df_all['status'] == 'ჩამოსული']
        df_chab = df_all[df_all['status'] == 'ჩაბარებული']

        count_gaph = len(df_gaph)
        count_chamo = len(df_chamo)
        count_chab = len(df_chab)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("📝 გაფორმებული", f"{count_gaph}")
        with m2:
            st.metric("✈️ ჩამოსული", f"{count_chamo}")
        with m3:
            st.metric("✅ ჩაბარებული", f"{count_chab}")

        st.markdown("<br>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([
            f"📝 გაფორმებული ({count_gaph})", 
            f"✈️ ჩამოსული ({count_chamo})", 
            f"✅ ჩაბარებული ({count_chab})"
        ])

        with tab1:
            if df_gaph.empty:
                st.info("💡 ამ სექციაში შეკვეთები არ არის.")
            else:
                for _, row in df_gaph.iterrows():
                    with st.container():
                        st.markdown(f"### 📦 #{row['id']} - **{row['item_name']}**")
                        col_img, col_info, col_action = st.columns([1.2, 2.5, 1.3])

                        with col_img:
                            if row['image']:
                                image = Image.open(io.BytesIO(row['image']))
                                st.image(image, use_container_width=True)
                            else:
                                st.info("🖼️ ფოტო არ არის")

                        with col_info:
                            st.markdown(f"👤 **მყიდველი:** `{row['customer_name']}`")
                            st.markdown(f"📞 **ტელეფონი:** `{row.get('phone', 'არ არის')}`")
                            st.markdown(f"📍 **მისამართი:** `{row.get('address', 'არ არის')}`")
                            st.markdown(f"📅 **თარიღი:** {row['order_date']}")
                            st.markdown(f"✈️ **ტრანსპორტირება:** `{row.get('shipping_cost', 0):.2f} ₾`")
                            
                        with col_action:
                            st.markdown("##### 💵 ფინანსები")
                            st.write(f"💰 გასაყიდი: **{row['sale_price']:.2f} ₾**")
                            st.write(f"📉 თვითღირ.: **{row['cost_price']:.2f} ₾**")
                            profit_val = row['profit']
                            if profit_val >= 0:
                                st.markdown(f"✨ მოგება: :green[**+{profit_val:.2f} ₾**]")
                            else:
                                st.markdown(f"⚠️ მოგება: :red[**{profit_val:.2f} ₾**]")

                            st.markdown("---")
                            if st.button("✈️ გადაყვანა: ჩამოსული", key=f"btn_move_{row['id']}", type="primary", use_container_width=True):
                                update_order_status(row['id'], "ჩამოსული")
                                st.rerun()

                    st.markdown("<br>", unsafe_allow_html=True)

        with tab2:
            if df_chamo.empty:
                st.info("💡 ამ სექციაში შეკვეთები არ არის.")
            else:
                for _, row in df_chamo.iterrows():
                    with st.container():
                        st.markdown(f"### 📦 #{row['id']} - **{row['item_name']}**")
                        col_img, col_info, col_action = st.columns([1.2, 2.5, 1.3])

                        with col_img:
                            if row['image']:
                                image = Image.open(io.BytesIO(row['image']))
                                st.image(image, use_container_width=True)
                            else:
                                st.info("🖼️ ფოტო არ არის")

                        with col_info:
                            st.markdown(f"👤 **მყიდველი:** `{row['customer_name']}`")
                            st.markdown(f"📞 **ტელეფონი:** `{row.get('phone', 'არ არის')}`")
                            st.markdown(f"📍 **მისამართი:** `{row.get('address', 'არ არის')}`")
                            st.markdown(f"📅 **თარიღი:** {row['order_date']}")
                            
                            ship_cost = row.get('shipping_cost', 0)
                            is_paid = bool(row.get('shipping_paid', 0))
                            st.markdown(f"✈️ **ტრანსპორტირება:** `{ship_cost:.2f} ₾`")
                            
                            paid_check = st.checkbox("☑️ ტრანსპორტირება გადახდილია", value=is_paid, key=f"ship_check_{row['id']}")
                            if paid_check != is_paid:
                                update_shipping_payment(row['id'], 1 if paid_check else 0)
                                st.rerun()

                        with col_action:
                            st.markdown("##### 💵 ფინანსები")
                            st.write(f"💰 გასაყიდი: **{row['sale_price']:.2f} ₾**")
                            st.write(f"📉 თვითღირ.: **{row['cost_price']:.2f} ₾**")
                            profit_val = row['profit']
                            if profit_val >= 0:
                                st.markdown(f"✨ მოგება: :green[**+{profit_val:.2f} ₾**]")
                            else:
                                st.markdown(f"⚠️ მოგება: :red[**{profit_val:.2f} ₾**]")

                            st.markdown("---")
                            if paid_check:
                                if st.button("✅ გადაყვანა: ჩაბარებული", key=f"btn_move_{row['id']}", type="primary", use_container_width=True):
                                    update_order_status(row['id'], "ჩაბარებული")
                                    st.rerun()
                            else:
                                st.warning("🔒 ჯერ მონიშნეთ ტრანსპორტირების გადახდა")

                    st.markdown("<br>", unsafe_allow_html=True)

        with tab3:
            if df_chab.empty:
                st.info("💡 ამ სექციაში შეკვეთები არ არის.")
            else:
                for _, row in df_chab.iterrows():
                    with st.container():
                        st.markdown(f"### 📦 #{row['id']} - **{row['item_name']}**")
                        col_img, col_info, col_action = st.columns([1.2, 2.5, 1.3])

                        with col_img:
                            if row['image']:
                                image = Image.open(io.BytesIO(row['image']))
                                st.image(image, use_container_width=True)
                            else:
                                st.info("🖼️ ფოტო არ არის")

                        with col_info:
                            st.markdown(f"👤 **მყიდველი:** `{row['customer_name']}`")
                            st.markdown(f"📞 **ტელეფონი:** `{row.get('phone', 'არ არის')}`")
                            st.markdown(f"📍 **მისამართი:** `{row.get('address', 'არ არის')}`")
                            st.markdown(f"📅 **თარიღი:** {row['order_date']}")
                            st.markdown(f"✈️ **ტრანსპორტირება:** `{row.get('shipping_cost', 0):.2f} ₾` (✅ გადახდილია)")

                        with col_action:
                            st.markdown("##### 💵 ფინანსები")
                            st.write(f"💰 გასაყიდი: **{row['sale_price']:.2f} ₾**")
                            st.write(f"📉 თვითღირ.: **{row['cost_price']:.2f} ₾**")
                            profit_val = row['profit']
                            if profit_val >= 0:
                                st.markdown(f"✨ მოგება: :green[**+{profit_val:.2f} ₾**]")
                            else:
                                st.markdown(f"⚠️ მოგება: :red[**{profit_val:.2f} ₾**]")

                    st.markdown("<br>", unsafe_allow_html=True)

    # 🔔 4. ნოტიფიკაციები
    elif choice.startswith("🔔 ნოტიფიკაციები"):
        st.subheader("🔔 შეხსენებები და შეტყობინებები")
        if notifications:
            for note in notifications:
                st.warning(note)
        else:
            st.success("🎉 ყველა შეკვეთა კონტროლზეა, შეხსენებები არ არის!")
