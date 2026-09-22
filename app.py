import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. PAGE CONFIG & DARK PURPLE NEON GLASSMORPHISM THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Urbanwavve E-Commerce",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Dark Deep Purple Core Background */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1e1035 0%, #0d0814 100%) !important;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Glass Highlight Card (Glow Effect) */
    .glass-card-glow {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(126, 34, 206, 0.05) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.15);
    }

    /* Input Fields Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stNumberInput>div>div>input {
        border-radius: 14px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 10px 14px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.4) !important;
    }

    /* Base Glowing Buttons */
    .stButton>button {
        border-radius: 14px !important;
        background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 10px 22px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0px 4px 15px rgba(168, 85, 247, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 6px 20px rgba(168, 85, 247, 0.5) !important;
    }

    /* Auth Active/Inactive Toggles */
    .active-toggle button {
        background: linear-gradient(135deg, #7e22ce 0%, #3b0764 100%) !important;
        color: #c084fc !important;
        font-weight: 700 !important;
        border: 1px solid #a855f7 !important;
        box-shadow: inset 0px 2px 8px rgba(0, 0, 0, 0.5), 0px 0px 18px rgba(168, 85, 247, 0.5) !important;
    }
    .inactive-toggle button {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: none !important;
        opacity: 0.7 !important;
    }

    /* Form Slide-in Animation */
    @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .animated-form {
        animation: fadeInSlide 0.4s ease-out forwards;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 8, 20, 0.85) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 16px !important;
        border-radius: 16px !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. SESSION STATE & PERSISTENT DATA
# ---------------------------------------------------------
if 'registered_user' not in st.session_state:
    st.session_state.registered_user = {
        "email": "admin@urbanwavve.ge",
        "phone": "599000000",
        "business_name": "Urbanwavve",
        "business_type": "ონლაინ მაღაზია",
        "password": "password123",
        "logo": None
    }

if 'remember_me' not in st.session_state:
    st.session_state.remember_me = True  # ტაბის გათიშვისას ავტომატური შესვლა

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = st.session_state.remember_me

if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {"text": "🔔 სისტემაში წარმატებით შეხვედით", "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
    ]

if 'orders' not in st.session_state:
    # 10+ დღის წინანდელი შეკვეთა ავტო-შეხსენების შესამოწმებლად
    past_date = (datetime.now() - timedelta(days=11)).strftime("%Y-%m-%d")
    st.session_state.orders = [
        {
            "id": "ORD-101",
            "sell_price": 120.0,
            "cost_price": 60.0,
            "customer_name": "giorgi_meshveliani",
            "phone": "595112233",
            "address": "თბილისი, ჭავჭავაძის #12",
            "shipping_fee": 10.0,
            "shipping_paid": False,
            "product_info": "Oversized Blue Hoodie",
            "product_photo": None,
            "status": "გაფორმებული",
            "created_at": past_date
        }
    ]

# ავტომატური შეხსენების შემოწმება (10 დღეზე მეტი ხნის შეკვეთები)
def check_10_day_reminders():
    for o in st.session_state.orders:
        created = datetime.strptime(o["created_at"], "%Y-%m-%d")
        if (datetime.now() - created).days >= 10 and o["status"] != "ჩაბარებული":
            reminder_text = f"⏰ შეხსენება: შეკვეთა #{o['id']} ({o['customer_name']}) 10 დღეზე მეტია გაფორმებულია. გთხოვთ შეამოწმოთ სტატუსი!"
            if not any(n["text"] == reminder_text for n in st.session_state.notifications):
                st.session_state.notifications.append({"text": reminder_text, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})

check_10_day_reminders()


# ---------------------------------------------------------
# 3. AUTHENTICATION PAGE (LOGIN / REGISTER)
# ---------------------------------------------------------
def show_auth_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-weight: 800; color: #ffffff;'>⚡ Urbanwavve Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #c084fc; font-size: 15px; margin-bottom: 35px;'>მართეთ გაყიდვები და შეკვეთები ექსკლუზიურ გარემოში</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
            login_id = st.text_input("ნომერი ან ელ-ფოსტა", key="login_id")
            login_pass = st.text_input("პაროლი", type="password", key="login_pass")
            remember = st.checkbox("დაიმახსოვრე მონაცემები", value=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("სისტემაში შესვლა", key="submit_login", use_container_width=True):
                reg = st.session_state.registered_user
                if (login_id == reg["email"] or login_id == reg["phone"]) and login_pass == reg["password"]:
                    st.session_state.logged_in = True
                    st.session_state.remember_me = remember
                    st.session_state.notifications.append({"text": "🔑 სისტემაში წარმატებით შეხვედით", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.rerun()
                else:
                    st.error("❌ არასწორი ნომერი/ელ-ფოსტა ან პაროლი!")

        else:
            reg_email = st.text_input("ელ-ფოსტა", key="reg_email")
            reg_phone = st.text_input("საკონტაქტო ნომერი", key="reg_phone")
            reg_b_name = st.text_input("ბიზნესის დასახელება", key="reg_b_name")
            reg_b_type = st.selectbox("ბიზნესის სახეობა", ["ონლაინ მაღაზია", "ოჯახის მაღაზია", "შიდა გაყიდვები", "საბითუმო ვაჭრობა", "ინდივიდუალური წარმოება"])
            
            reg_pass = st.text_input("პაროლი", type="password", key="reg_pass")
            reg_confirm = st.text_input("გაიმეორეთ პაროლი", type="password", key="reg_confirm")
            reg_logo = st.file_uploader("ლოგოს ატვირთვა", type=['png', 'jpg', 'jpeg'])
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ანგარიშის შექმნა", key="submit_reg", use_container_width=True):
                if not (reg_email and reg_phone and reg_b_name and reg_pass and reg_confirm):
                    st.error("❌ გთხოვთ შეავსოთ ყველა ველი!")
                elif reg_pass != reg_confirm:
                    st.error("❌ პაროლები ერთმანეთს არ ემთხვევა!")
                else:
                    st.session_state.registered_user = {
                        "email": reg_email,
                        "phone": reg_phone,
                        "business_name": reg_b_name,
                        "business_type": reg_b_type,
                        "password": reg_pass,
                        "logo": reg_logo
                    }
                    st.session_state.notifications.append({"text": "🎉 ახალი ანგარიში წარმატებით დარეგისტრირდა!", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.success("✅ რეგისტრაცია წარმატებით დასრულდა! გადადით შესვლის გვერდზე.")
                    
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 4. MAIN DASHBOARD PAGE
# ---------------------------------------------------------
def show_dashboard():
    st.markdown("<h2>📊 ფინანსური დეშბორდი</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate Finance
    total_revenue = sum(o["sell_price"] for o in st.session_state.orders if o["status"] != "გაუქმებული")
    total_cost = sum(o["cost_price"] for o in st.session_state.orders if o["status"] != "გაუქმებული")
    total_profit = total_revenue - total_cost

    c1, c2, c3 = st.columns(3)
    c1.metric("შემოსავალი (Total Revenue)", f"{total_revenue:,.2f} ₾")
    c2.metric("გასავალი (Total Cost)", f"{total_cost:,.2f} ₾")
    c3.metric("წმინდა მოგება (Net Profit)", f"{total_profit:,.2f} ₾")

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)

    # Compact Graph Filter
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col_t, col_f = st.columns([3, 1])
    with col_t:
        st.subheader("📈 შემოსავლების დინამიკა")
    with col_f:
        time_frame = st.selectbox("პერიოდი", ["ბოლო 7 დღე", "ბოლო 1 თვე", "ბოლო 3 თვე", "1 წელი"])

    # Sample chart scaled by selection
    factor = 1 if time_frame == "ბოლო 7 დღე" else 3 if time_frame == "ბოლო 1 თვე" else 6 if time_frame == "ბოლო 3 თვე" else 12
    chart_data = pd.DataFrame({
        'პერიოდი': [f'T-{i}' for i in range(factor, 0, -1)],
        'შემოსავალი (₾)': [100 * i + (total_revenue/max(factor,1)) for i in range(1, factor + 1)]
    }).set_index('პერიოდი')

    st.line_chart(chart_data, color="#a855f7", height=220)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 5. ORDER CREATION PAGE
# ---------------------------------------------------------
def show_create_order_page():
    st.title("📝 შეკვეთის გაფორმება")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("create_order_form", clear_on_submit=True):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        sell_p = c1.number_input("ფასი რაც მომხმარებელმა გადაიხადა (₾)", min_value=0.0, step=5.0)
        cost_p = c2.number_input("ფასი რაც პროდუქტი გვიჯდება (₾)", min_value=0.0, step=5.0)
        
        cust_name = c1.text_input("შემკვეთის სახელი (ინსტაგრამ იუზერი)")
        cust_phone = c2.text_input("საკონტაქტო ნომერი")
        cust_address = c1.text_input("მისამართი")
        ship_fee = c2.number_input("ტრანსპორტირების თანხა (არ შედის ხარჯებში)", min_value=0.0, step=1.0)
        
        prod_info = st.text_area("რა შეიძინა (პროდუქციის დეტალები)")
        prod_photo = st.file_uploader("პროდუქტის ფოტო (სურვილისამებრ)", type=['png', 'jpg', 'jpeg'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("შეკვეთის გაფორმება"):
            if sell_p > 0 and cust_name and cust_phone:
                new_id = f"ORD-{len(st.session_state.orders) + 101}"
                new_order = {
                    "id": new_id,
                    "sell_price": sell_p,
                    "cost_price": cost_p,
                    "customer_name": cust_name,
                    "phone": cust_phone,
                    "address": cust_address,
                    "shipping_fee": ship_fee,
                    "shipping_paid": False,
                    "product_info": prod_info,
                    "product_photo": prod_photo,
                    "status": "გაფორმებული",
                    "created_at": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.orders.append(new_order)
                st.session_state.notifications.append({"text": f"📦 ახალი შეკვეთა #{new_id} გაფორმდა ({cust_name})", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success(f"✅ შეკვეთა #{new_id} წარმატებით გაფორმდა!")
            else:
                st.error("❌ გთხოვთ შეავსოთ აუცილებელი ველები (ფასი, სახელი, ნომერი)!")
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 6. ORDERS MANAGEMENT PAGE (3 STAGES)
# ---------------------------------------------------------
def show_orders_page():
    st.title("📦 შეკვეთების მართვა")
    st.markdown("<br>", unsafe_allow_html=True)

    # Counter Summary
    st_g = len([o for o in st.session_state.orders if o["status"] == "გაფორმებული"])
    st_c = len([o for o in st.session_state.orders if o["status"] == "ჩამოსულია"])
    st_f = len([o for o in st.session_state.orders if o["status"] == "ჩაბარებული"])

    col_a, col_b, col_c = st.columns(3)
    col_a.info(f"📥 გაფორმებული: **{st_g}** ამანათი")
    col_b.warning(f"🛬 ჩამოსულია: **{st_c}** ამანათი")
    col_c.success(f"✅ ჩაბარებული: **{st_f}** ამანათი")

    st.markdown("<br>", unsafe_allow_html=True)
    tabs = st.tabs(["📥 1. გაფორმებული", "🛬 2. ჩამოსულია", "✅ 3. ჩაბარებული"])

    # Tab 1: გაფორმებული
    with tabs[0]:
        orders_list = [o for o in st.session_state.orders if o["status"] == "გაფორმებული"]
        if not orders_list:
            st.info("გაფორმებული შეკვეთები არ არის.")
        for ord_item in orders_list:
            st.markdown(f"""
            <div class="glass-card">
                <h4><b>#{ord_item['id']}</b> — {ord_item['customer_name']} ({ord_item['phone']})</h4>
                <p><b>მისამართი:</b> {ord_item['address']} | <b>ნყიდი ფასი:</b> {ord_item['sell_price']} ₾ | <b>თვითღირებულება:</b> {ord_item['cost_price']} ₾</p>
                <p><b>ტრანსპორტირება:</b> {ord_item['shipping_fee']} ₾ | <b>პროდუქტი:</b> {ord_item['product_info']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"გადატანა 'ჩამოსულია'-ში ➡️", key=f"to_cam_{ord_item['id']}"):
                ord_item["status"] = "ჩამოსულია"
                st.session_state.notifications.append({"text": f"🛬 შეკვეთა #{ord_item['id']} გადავიდა სტატუსში: ჩამოსულია", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.rerun()

    # Tab 2: ჩამოსულია
    with tabs[1]:
        orders_list = [o for o in st.session_state.orders if o["status"] == "ჩამოსულია"]
        if not orders_list:
            st.info("ჩამოსული შეკვეთები არ არის.")
        for ord_item in orders_list:
            st.markdown(f"""
            <div class="glass-card">
                <h4><b>#{ord_item['id']}</b> — {ord_item['customer_name']}</h4>
                <p><b>გასახდელი ტრანსპორტირების თანხა:</b> <span style="color:#a855f7; font-weight:bold;">{ord_item['shipping_fee']} ₾</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Checkbox for shipping payment restriction
            is_paid = st.checkbox(f"მომხმარებელმა გადაიხადა ტრანსპორტირების თანხა ({ord_item['shipping_fee']} ₾)", value=ord_item["shipping_paid"], key=f"pay_{ord_item['id']}")
            ord_item["shipping_paid"] = is_paid

            if st.button(f"გადატანა 'ჩაბარებული'-ში ➡️", key=f"to_done_{ord_item['id']}"):
                if not ord_item["shipping_paid"]:
                    st.error("❌ პროდუქტი ვერ გადავა ჩაბარებულ ველში ტრანსპორტირების თანხის გადახდის აღნიშვნის გარეშე!")
                else:
                    ord_item["status"] = "ჩაბარებული"
                    st.session_state.notifications.append({"text": f"✅ შეკვეთა #{ord_item['id']} წარმატებით ჩაბარდა!", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.rerun()

    # Tab 3: ჩაბარებული
    with tabs[2]:
        orders_list = [o for o in st.session_state.orders if o["status"] == "ჩაბარებული"]
        if not orders_list:
            st.info("ჩაბარებული შეკვეთები არ არის.")
        for ord_item in orders_list:
            st.markdown(f"""
            <div class="glass-card-glow">
                <h4><b>#{ord_item['id']}</b> — {ord_item['customer_name']} (დასრულებული)</h4>
                <p><b>სრული შემოსავალი:</b> {ord_item['sell_price']} ₾ | <b>ტრანსპორტირება:</b> {ord_item['shipping_fee']} ₾ (გადახდილია ✅)</p>
            </div>
            """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 7. NOTIFICATIONS PAGE
# ---------------------------------------------------------
def show_notifications_page():
    st.title("🔔 ნოტიფიკაციები და შეხსენებები")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    for notif in reversed(st.session_state.notifications):
        st.markdown(f"• **{notif['text']}** <br><small style='color:#94a3b8;'>{notif['date']}</small><hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 8. PROFILE SETTINGS PAGE
# ---------------------------------------------------------
def show_profile_page():
    st.title("👤 პროფილის პარამეტრები")
    st.markdown("<br>", unsafe_allow_html=True)

    reg = st.session_state.registered_user

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("მონაცემების განახლება")
    
    new_b_name = st.text_input("ბიზნესის დასახელება", value=reg["business_name"])
    new_email = st.text_input("ელ-ფოსტა", value=reg["email"])
    new_phone = st.text_input("საკონტაქტო ნომერი", value=reg["phone"])
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.subheader("🔒 პაროლის შეცვლა")
    curr_pass = st.text_input("მიმდინარე პაროლი", type="password")
    new_pass = st.text_input("ახალი პაროლი", type="password")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ცვლილებების შენახვა"):
        if curr_pass and curr_pass != reg["password"]:
            st.error("❌ მიმდინარე პაროლი არასწორია!")
        else:
            # Warning modal/confirmation using session state
            st.warning("⚠️ ყურადღება: მონაცემების შეცვლის შემდეგ ძველ მონაცემებს ვეღარ დააბრუნებთ! დარწმუნებული ხართ?")
            if st.button("⚠️ დიახ, ვადასტურებ შეცვლას", key="confirm_change"):
                reg["business_name"] = new_b_name
                reg["email"] = new_email
                reg["phone"] = new_phone
                if new_pass:
                    reg["password"] = new_pass
                st.session_state.notifications.append({"text": "👤 პროფილის მონაცემები/პაროლი განახლდა", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                st.success("✅ მონაცემები წარმატებით განახლდა!")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# 9. MAIN ROUTER & NAVIGATION
# ---------------------------------------------------------
if not st.session_state.logged_in:
    show_auth_page()
else:
    with st.sidebar:
        st.markdown("<h2 style='color: #a855f7; font-weight: 800;'>🔮 Urbanwavve</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#94a3b8;'>{st.session_state.registered_user['business_name']}</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        page = st.radio(
            "მენიუ",
            ["📊 დეშბორდი", "📝 შეკვეთის გაფორმება", "📦 შეკვეთების მართვა", "🔔 ნოტიფიკაციები", "👤 პროფილი"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 გასვლა", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.remember_me = False
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
