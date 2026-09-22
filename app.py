import streamlit as st

# Custom CSS for Modern UI & Rounded Tabs
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }

    /* Modern Rounded Tabs (Instagram style) */
    div[data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #161B22;
        padding: 8px;
        border-radius: 30px;
        border: 1px solid #30363D;
    }

    div[data-baseweb="tab"] {
        height: 40px;
        white-space: pre;
        border-radius: 20px;
        color: #8B949E;
        font-weight: 600;
        padding: 0px 20px;
        border: none !important;
    }

    div[aria-selected="true"] {
        background-color: #238636 !important; /* ან Instagram Gradient / Accent Color */
        color: #FFFFFF !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Inputs & Buttons */
    .stTextInput>div>div>input {
        border-radius: 12px;
        background-color: #161B22;
        color: white;
        border: 1px solid #30363D;
    }
    
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Profile Section Code Template
def show_profile_page():
    st.title("👤 პროფილის მართვა")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("პროფილის ფოტო")
        uploaded_file = st.file_uploader("აირჩიეთ ფოტო", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file, width=150)
            
    with col2:
        st.subheader("პირადი ინფორმაცია")
        name = st.text_input("სახელი და გვარი", value="Urbanwavve")
        phone = st.text_input("საკონტაქტო ნომერი", value="+995 5XX XX XX XX")
        
        st.subheader("პაროლის შეცვლა")
        old_pass = st.text_input("მიმდინარე პაროლი", type="password")
        new_pass = st.text_input("ახალი პაროლი", type="password")
        
        if st.button("მონაცემების განახლება"):
            st.success("მონაცემები წარმატებით განახლდა!")

    st.markdown("---")
    st.subheader("📦 შეკვეთების მართვა და ანულირება")
    # აქ დაემატება შეკვეთების გაუქმების ფუნქციონალი
