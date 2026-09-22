import streamlit as st
import sqlite3
import pandas as pd
import hashlib
from datetime import datetime
from PIL import Image
import io

# --- გვერდის კონფიგურაცია ---
st.set_page_config(
    page_title="Business & Order Manager",
    page_icon="🛍️",
    layout="wide"
)

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
            image BLOB
        )
    ''')
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

def add_order(username, item_name, cost_price, sale_price, profit, customer_name, order_date, image_bytes):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        INSERT INTO orders (username, item_name, cost_price, sale_price, profit, customer_name, order_date, status, image)
        VALUES (?,?,?,?,?,?,?,'გაფორმებული',?)
    ''', (username, item_name, cost_price, sale_price, profit, customer_name, order_date, image_bytes))
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

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'business_name' not in st.session_state:
    st.session_state['business_name'] = ""

# ==========================================
# 1. პირველივე გვერდი: ავტორიზაცია / რეგისტრაცია
# ==========================================
if not st.session_state['logged_in']:
    st.title("🛍️ ბიზნესისა და შეკვეთების მართვა")
    st.write("მართეთ თქვენი გაყიდვები, შეკვეთები და ფინანსები მარტივად.")

    tab1, tab2 = st.tabs(["🔑 ავტორიზაცია (შესვლა)", "📝 რეგისტრაცია"])

    with tab1:
        st.subheader("სისტემაში შესვლა")
        with st.form("login_form"):
            login_input = st.text_input("მომხმარებლის სახელი ან ელ-ფოსტა (Gmail)")
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
            new_email = st.text_input("📧 ელ-ფოსტა (Gmail)")
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
    # ზედა პანელი: პროფილის ინფო და გამოსვლის (Logout) ღილაკი
    col_head1, col_head2 = st.columns([4, 1])
    with col_head1:
        st.subheader(f"🏢 {st.session_state['business_name']}")
        st.caption(f"👤 ავტორიზებული მომხმარებელი: `{st.session_state['username']}`")
    with col_head2:
        if st.button("🚪 გამოსვლა (Logout)", key="top_logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.session_state['business_name'] = ""
            st.rerun()

    st.markdown("---")

    # ნოტიფიკაციები (10+ დღის შეკვეთები)
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
                    notifications.append(f"⚠️ **შეხსენება:** შეკვეთა #{row['id']} ({row['item_name']}) გაფორმდა {days_passed} დღის წინ. გადაამოწმეთ სტატუსი!")

    # მენიუ მარცხნივ
    menu = ["📊 დეშბორდი & ფინანსები", "➕ ახალი შეკვეთა", "📦 შეკვეთების მართვა", f"🔔 ნოტიფიკაციები ({len(notifications)})"]
    choice = st.sidebar.radio("მენიუ", menu)

    # 📊 1. დეშბორდი & ფინანსები
    if choice == "📊 დეშბორდი & ფინანსები":
        st.title(f"📊 ფინანსური მიმოხილვა")
        
        if not df_all.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("სულ შეკვეთა", len(df_all))
            c2.metric("💰 ჯამური შემოსავალი", f"{df_all['sale_price'].sum():.2f} ₾")
            c3.metric("📉 ჯამური ხარჯი", f"{df_all['cost_price'].sum():.2f} ₾")
            c4.metric("✨ წმინდა მოგება", f"{df_all['profit'].sum():.2f} ₾")

            st.markdown("---")
            st.subheader("📈 შეკვეთების გადანაწილება ეტაპების მიხედვით")
            st.bar_chart(df_all['status'].value_counts())
        else:
            st.info("შეკვეთები ჯერ არ არის დაფიქსირებული.")

    # ➕ 2. ახალი შეკვეთის დამატება
    elif choice == "➕ ახალი შეკვეთა":
        st.title("➕ ახალი შეკვეთის გაფორმება")

        with st.form("new_order_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                item_name = st.text_input("📦 პროდუქტის დასახელება")
                customer_name = st.text_input("👤 მყიდველის სახელი და გვარი")
                uploaded_file = st.file_uploader("🖼️ დაამატეთ პროდუქტის ფოტო", type=['png', 'jpg', 'jpeg'])

            with col2:
                sale_price = st.number_input("💰 გასაყიდი ფასი (₾)", min_value=0.0, step=1.0)
                cost_price = st.number_input("📉 თვითღირებულება (₾)", min_value=0.0, step=1.0)
                profit = sale_price - cost_price
                st.info(f"💡 მოსალოდნელი მოგება: **{profit:.2f} ₾**")

            submitted = st.form_submit_button("შეკვეთის ჩანიშვნა", type="primary")

            if submitted:
                if not item_name or not customer_name:
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
                        current_now,
                        image_bytes
                    )
                    st.success(f"შეკვეთა წარმატებით ჩაინიშნა! თარიღი: {current_now}")

    # 📦 3. შეკვეთების 3-ეტაპიანი მართვა
    elif choice == "📦 შეკვეთების მართვა":
        st.title("📦 შეკვეთების ეტაპები")

        tab_gaph, tab_chamo, tab_chab = st.tabs(["📝 1. გაფორმებული", "✈️ 2. ჩამოსული", "✅ 3. ჩაბარებული"])

        def render_orders(status_filter, btn_text=None, next_status=None):
            df_filtered = df_all[df_all['status'] == status_filter]
            if df_filtered.empty:
                st.info("ამ სექციაში შეკვეთები არ არის.")
                return

            for _, row in df_filtered.iterrows():
                with st.expander(f"📦 #{row['id']} - {row['item_name']} | მყიდველი: {row['customer_name']}"):
                    c1, c2 = st.columns([1, 2])
                    
                    with c1:
                        if row['image']:
                            image = Image.open(io.BytesIO(row['image']))
                            st.image(image, width=200)
                        else:
                            st.caption("🖼️ ფოტო არ არის")

                    with c2:
                        st.write(f"**თარიღი:** {row['order_date']}")
                        st.write(f"**გასაყიდი ფასი:** {row['sale_price']:.2f} ₾")
                        st.write(f"**თვითღირებულება:** {row['cost_price']:.2f} ₾")
                        st.write(f"**მოგება:** {row['profit']:.2f} ₾")

                        if btn_text and next_status:
                            if st.button(btn_text, key=f"btn_{row['id']}"):
                                update_order_status(row['id'], next_status)
                                st.success(f"სტატუსი შეიცვალა: {next_status}")
                                st.rerun()

        with tab_gaph:
            st.subheader("📝 გაფორმებული შეკვეთები")
            render_orders("გაფორმებული", "✈️ ჩამოსულია", "ჩამოსული")

        with tab_chamo:
            st.subheader("✈️ ჩამოსული შეკვეთები")
            render_orders("ჩამოსული", "✅ ჩაბარებულია", "ჩაბარებული")

        with tab_chab:
            st.subheader("✅ ჩაბარებული შეკვეთები")
            render_orders("ჩაბარებული")

    # 🔔 4. ნოტიფიკაციები
    elif choice.startswith("🔔 ნოტიფიკაციები"):
        st.title("🔔 შეხსენებები და შეტყობინებები")
        if notifications:
            for note in notifications:
                st.warning(note)
        else:
            st.success("🎉 ყველა შეკვეთა კონტროლზეა, შეხსენებები არ არის!")
