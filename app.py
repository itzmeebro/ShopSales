# 📦 3. შეკვეთების მართვა (განახლებული ლამაზი დიზაინი)
    elif choice == "📦 შეkვეთების მართვა":
        st.title("📦 შეკვეთების მართვა & სტატუსები")
        st.write("ადევნეთ თვალი შეკვეთებს ეტაპების მიხედვით.")

        # რაოდენობების დათვლა
        df_gaph = df_all[df_all['status'] == 'გაფორმებული']
        df_chamo = df_all[df_all['status'] == 'ჩამოსული']
        df_chab = df_all[df_all['status'] == 'ჩაბარებული']

        count_gaph = len(df_gaph)
        count_chamo = len(df_chamo)
        count_chab = len(df_chab)

        # 📊 ზედა ვიზუალური ბარათები (Metrics Summary)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("📝 გაფორმებული", f"{count_gaph} შეკვეთა", help="მუშავდება / გზაშია")
        with m2:
            st.metric("✈️ ჩამოსული", f"{count_chamo} შეკვეთა", help="მზადაა ჩასაბარებლად")
        with m3:
            st.metric("✅ ჩაბარებული", f"{count_chab} შეკვეთა", help="დასრულებული შეკვეთები")

        st.markdown("---")

        # 📑 3-ეტაპიანი ტაბები რაოდენობების მითითებით
        tab1, tab2, tab3 = st.tabs([
            f"📝 1. გაფორმებული ({count_gaph})", 
            f"✈️ 2. ჩამოსული ({count_chamo})", 
            f"✅ 3. ჩაბარებული ({count_chab})"
        ])

        # დამხმარე ფუნქცია შეკვეთების ლამაზად გამოსატანად
        def render_pretty_orders(df_subset, status_badge_color, btn_label=None, next_status=None):
            if df_subset.empty:
                st.info("💡 ამ სექციაში შეკვეთები არ არის.")
                return

            for _, row in df_subset.iterrows():
                # თითოეული შეკვეთის კონტეინერი (ბარათი)
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
                        st.markdown(f"🏷️ **სტატუსი:** :{status_badge_color}[{row['status']}]")
                        
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
                        if btn_label and next_status:
                            if st.button(btn_label, key=f"btn_move_{row['id']}", type="primary", use_container_width=True):
                                update_order_status(row['id'], next_status)
                                st.success(f"შეკვეთა #{row['id']} გადავიდა სტატუსზე: {next_status}")
                                st.rerun()

                st.markdown("---")

        with tab1:
            st.subheader("📝 გაფორმებული შეკვეთები")
            render_pretty_orders(df_gaph, "orange", "✈️ გადაყვანა: ჩამოსული", "ჩამოსული")

        with tab2:
            st.subheader("✈️ ჩამოსული შეკვეთები")
            render_pretty_orders(df_chamo, "blue", "✅ გადაყვანა: ჩაბარებული", "ჩაბარებული")

        with tab3:
            st.subheader("✅ ჩაბარებული შეკვეთები")
            render_pretty_orders(df_chab, "green")
