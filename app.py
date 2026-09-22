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
            image BLOB,
            shipping_cost REAL DEFAULT 0,
            shipping_paid INTEGER DEFAULT 0
        )
    ''')
    
    # სვეტების შემოწმება/დამატება ძველი ბაზისთვის
    c.execute("PRAGMA table_info(orders)")
    columns = [col[1] for col in c.fetchall()]
    if 'shipping_cost' not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN shipping_cost REAL DEFAULT 0")
    if 'shipping_paid' not in columns:
        c.execute("ALTER TABLE orders ADD COLUMN shipping_paid INTEGER DEFAULT 0")
        
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

def add_order(username, item_name, cost_price, sale_price, profit, customer_name, order_date, image_bytes, shipping_cost):
    conn = sqlite3.connect('store_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        INSERT INTO orders (username, item_name, cost_price, sale_price, profit, customer_name, order_date, status, image, shipping_cost, shipping_paid)
        VALUES (?,?,?,?,?,?,?,'გაფორმებული',?,?, 0)
    ''', (username, item_name, cost_price, sale_price, profit, customer_name, order_date, image_bytes, shipping_cost))
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

    menu = ["📊 დეშბორდი & ფინანსები", "➕ ახალი შეკვეთა", "📦 შეკვეთების მართვა", f"🔔 ნოტიფიკაციები ({len(notifications)})"]
    choice = st.sidebar.radio("მენიუ", menu)

    # 📊 1. დეშბორდი
    if choice == "📊 დეშბორდი & ფინანსები":
        st.title("📊 ფინანსური მიმოხილვა")
        
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

    # ➕ 2. ახალი შეკვეთა
    elif choice == "➕ ახალი შეკვეთა":
        st.title("➕ ახალი შეკვეთის გაფორმება")

        col1, col2 = st.columns(2)
        
        with col1:
            item_name = st.text_input("📦 პროდუქტის დასახელება")
            customer_name = st.text_input("👤 მყიდველის სახელი და გვარი")
            uploaded_file = st.file_uploader("🖼️ დაამატეთ პროდუქტის ფოტო", type=['png', 'jpg', 'jpeg'])

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
                st.info(f"💡 მოსალოდნელი მოგება: **0.00 ₾**")

        st.markdown("---")
        submitted = st.button("შეკვეთის ჩანიშვნა", type="primary")

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
                    current_now,
                    image_bytes,
                    shipping_cost
                )
                st.success(f"🎉 შეკვეთა წარმატებით ჩაინიშნა! თარიღი: {current_now}")

    # 📦 3. შეკვეთების მართვა
    elif choice == "📦 შეკვეთების მართვა":
        st.title("📦 შეკვეთების მართვა & სტატუსები")
        st.write("ადევნეთ თვალი შეკვეთებს ეტაპების მიხედვით.")

        df_gaph = df_all[df_all['status'] == 'გაფორმებული']
        df_chamo = df_all[df_all['status'] == 'ჩამოსული']
        df_chab = df_all[df_all['status'] == 'ჩაბარებული']

        count_gaph = len(df_gaph)
        count_chamo = len(df_chamo)
        count_chab = len(df_chab)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("📝 გაფორმებული", f"{count_gaph} შეკვეთა")
        with m2:
            st.metric("✈️ ჩამოსული", f"{count_chamo} შეკვეთა")
        with m3:
            st.metric("✅ ჩაბარებული", f"{count_chab} შეკვეთა")

        st.markdown("---")

        tab1, tab2, tab3 = st.tabs([
            f"📝 1. გაფორმებული ({count_gaph})", 
            f"✈️ 2. ჩამოსული ({count_chamo})", 
            f"✅ 3. ჩაბარებული ({count_chab})"
        ])

        with tab1:
            st.subheader("📝 გაფორმებული შეკვეთები")
            if df_gaph.empty:
                st.info("💡 ამ სექციაში შეკვეთები არ არის.")
            else:
                for _, row in df_gaph.iterrows():
                    with st.container():
                        st.markdown(f"#### 📦 #{row['id']} - **{row['item_name']}**")
                        col_img, col_info, col_action = st.columns([1.2, 2.5, 1.3])

                        with col_img:
                            if row['image']:
                                image = Image.open(io.BytesIO(row['image']))
                                st.image(image, use_container_width=True)
                            else:
                                st.info("🖼️ ფოტო არ არის")

                        with col_info:
                            st.markdown(f"👤 **მყიდველი:** `{row['customer_name']}`")
                            st.markdown(f"📅 **თარიღი:** {row['order_date']}")
                            st.markdown(f"🏷️ **სტატუსი:** :orange[{row['status']}]")
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

                    st.markdown("---")

        with tab2:
            st.subheader("✈️ ჩამოსული შეკვეთები")
            if df_chamo.empty:
                st.info("💡 ამ სექციაში შეკვეთები არ არის.")
            else:
                for _, row in df_chamo.iterrows():
                    with st.container():
                        st.markdown(f"#### 📦 #{row['id']} - **{row['item_name']}**")
                        col_img, col_info, col_action = st.columns([1.2, 2.5, 1.3])

                        with col_img:
                            if row['image']:
                                image = Image.open(io.BytesIO(row['image']))
                                st.image(image, use_container_width=True)
                            else:
                                st.info("🖼️ ფოტო არ არის")

                        with col_info:
                            st.markdown(f"👤 **მყიდველი:** `{row['customer_name']}`")
                            st.markdown(f"📅 **თარიღი:** {row['order_date']}")
                            st.markdown(f"🏷️ **სტატუსი:** :blue[{row['status']}]")
                            
                            ship_cost = row.get('shipping_cost', 0)
                            is_paid = bool(row.get('shipping_paid', 0))
                            st.markdown(f"✈️ **ტრანსპორტირება:** `{ship_cost:.2f} ₾`")
                            
                            # ჩექბოქსი გადახდის აღსანიშნავად
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
                            # გადაყვანის შეზღუდვა
                            if paid_check:
                                if st.button("✅ გადაყვანა: ჩაბარებული", key=f"btn_move_{row['id']}", type="primary", use_container_width=True):
                                    update_order_status(row['id'], "ჩაბარებული")
                                    st.rerun()
                            else:
                                st.warning("🔒 გადასაყვანად ჯერ მონიშნეთ ტრანსპორტირების გადახდა")

                    st.markdown("---")

        with tab3:
            st.subheader("✅ ჩაბარებული შეკვეთები")
            if df_chab.empty:
                st.info("💡 ამ სექციაში შეკვეთები არ არის.")
            else:
                for _, row in df_chab.iterrows():
                    with st.container():
                        st.markdown(f"#### 📦 #{row['id']} - **{row['item_name']}**")
                        col_img, col_info, col_action = st.columns([1.2, 2.5, 1.3])

                        with col_img:
                            if row['image']:
                                image = Image.open(io.BytesIO(row['image']))
                                st.image(image, use_container_width=True)
                            else:
                                st.info("🖼️ ფოტო არ არის")

                        with col_info:
                            st.markdown(f"👤 **მყიდველი:** `{row['customer_name']}`")
                            st.markdown(f"📅 **თარიღი:** {row['order_date']}")
                            st.markdown(f"🏷️ **სტატუსი:** :green[{row['status']}]")
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

                    st.markdown("---")

    # 🔔 4. ნოტიფიკაციები
    elif choice.startswith("🔔 ნოტიფიკაციები"):
        st.title("🔔 შეხსენებები და შეტყობინებები")
        if notifications:
            for note in notifications:
                st.warning(note)
        else:
            st.success("🎉 ყველა შეკვეთა კონტროლზეა, შეხსენებები არ არის!")
