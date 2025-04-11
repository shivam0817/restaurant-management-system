import streamlit as st
import pandas as pd
from fpdf import FPDF
from db import create_tables, add_menu_item, get_menu, delete_menu_item, place_order, get_orders

# Initialize DB tables
create_tables()

st.set_page_config(page_title="Restaurant Manager", layout="wide")
st.title("🍽️ Restaurant Management System")

menu = st.sidebar.radio("Menu", ["Add Menu Item", "View Menu", "Place Order", "View Orders"])

# 1. Add Menu Items
if menu == "Add Menu Item":
    st.subheader("➕ Add Menu Item")
    name = st.text_input("Item Name")
    category = st.selectbox("Category", ["Starter", "Main Course", "Dessert", "Beverage"])
    price = st.number_input("Price", min_value=0.0)
    if st.button("Add Item"):
        if name and price > 0:
            add_menu_item(name, category, price)
            st.success("Item added to menu.")
        else:
            st.warning("Fill all fields.")

# 2. View Menu
elif menu == "View Menu":
    st.subheader("📋 Menu")
    items = get_menu()
    if items:
        st.table(items)
        item_ids = [f"{item[0]} - {item[1]}" for item in items]
        selected = st.selectbox("Select item to delete", item_ids)
        if st.button("Delete"):
            item_id = int(selected.split(" - ")[0])
            delete_menu_item(item_id)
            st.success("Item deleted.")
    else:
        st.info("No items in the menu.")

# 3. Place Order
elif menu == "Place Order":
    st.subheader("🛒 Place Order")
    menu_items = get_menu()
    if not menu_items:
        st.warning("No menu items available.")
    else:
        item_names = [f"{item[1]} - Rs. {item[3]}" for item in menu_items]
        selected = st.selectbox("Select Item", item_names)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        if st.button("Place Order"):
            index = item_names.index(selected)
            item_name = menu_items[index][1]
            price = menu_items[index][3]
            total = price * quantity
            place_order(item_name, quantity, total)
            st.success(f"Order placed: {item_name} x {quantity} (Total Rs. {total:.2f})")

# 4. View Orders + Export
elif menu == "View Orders":
    st.subheader("📦 Orders")
    orders = get_orders()

    if orders:
        df_orders = pd.DataFrame(orders, columns=["Order ID", "Item", "Quantity", "Total (Rs)"])
        st.table(df_orders)

        # CSV Export
        csv = df_orders.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Orders as CSV",
            data=csv,
            file_name='restaurant_orders.csv',
            mime='text/csv',
        )

        # PDF Export
        if st.button("📄 Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Restaurant Orders Report", ln=True, align='C')
            pdf.ln(10)

            for index, row in df_orders.iterrows():
                line = f"{row['Order ID']} | {row['Item']} | Qty: {row['Quantity']} | Rs. {row['Total (Rs)']}"
                pdf.cell(200, 10, txt=line, ln=True)

            pdf_path = "restaurant_orders.pdf"
            pdf.output(pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Orders as PDF", f, file_name="restaurant_orders.pdf")

    else:
        st.info("No orders placed yet.")
