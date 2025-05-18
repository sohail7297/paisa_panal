import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import sqlite3
import hashlib

st.set_page_config(page_title="PAISA PANEL", page_icon="💰", layout="wide")

DB_NAME = "users.db"
category_file = "categories.json"


# --- Database setup ---
def create_users_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_users_table()


# --- Password hashing ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# --- User functions ---
def register_user(username, password, email="", phone=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, hashed_password, email, phone) VALUES (?, ?, ?, ?)",
                  (username, hashed, email, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result and hash_password(password) == result[0]:
        return True
    else:
        return False


def check_user_contact(username, email="", phone=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if email:
        c.execute("SELECT username FROM users WHERE username = ? AND email = ?", (username, email))
    elif phone:
        c.execute("SELECT username FROM users WHERE username = ? AND phone = ?", (username, phone))
    else:
        return False
    result = c.fetchone()
    conn.close()
    return result is not None


def reset_password(username, new_password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed = hash_password(new_password)
    c.execute("UPDATE users SET hashed_password = ? WHERE username = ?", (hashed, username))
    conn.commit()
    conn.close()


# --- Categories management ---
if "categories" not in st.session_state:
    if os.path.exists(category_file):
        with open(category_file, "r") as f:
            st.session_state.categories = json.load(f)
    else:
        st.session_state.categories = {
            "Uncategorized": [],
        }


def save_categories():
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f)


def categorize_transactions(df):
    df["Category"] = "Uncategorized"

    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue

        lowered_keywords = [keyword.lower().strip() for keyword in keywords]

        for idx, row in df.iterrows():
            details = row["Details"].lower().strip()
            if details in lowered_keywords:
                df.at[idx, "Category"] = category

    return df


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")

        return categorize_transactions(df)
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def add_keyword_to_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True

    return False


# --- Main app logic ---
def main():
    st.title("Paisa Panel💹")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # If not authenticated, show login/register/reset forms
    if not st.session_state.authenticated:
        st.header("Login to Paisa Panel")
        login_mode = st.radio("Choose action:", ["Login", "Register", "Forgot Password"])

        if login_mode == "Login":
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"Welcome back, {username}!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password.")

        elif login_mode == "Register":
            username = st.text_input("Choose a Username", key="reg_username")
            password = st.text_input("Choose a Password", type="password", key="reg_password")
            email = st.text_input("Email (optional)", key="reg_email")
            phone = st.text_input("Phone (optional)", key="reg_phone")
            if st.button("Register"):
                if not username or not password:
                    st.error("Username and password are required.")
                else:
                    success = register_user(username, password, email, phone)
                    if success:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username already exists.")

        elif login_mode == "Forgot Password":
            username = st.text_input("Enter your Username", key="fp_username")
            contact_method = st.radio("Verify via", ["Email", "Phone"])
            if contact_method == "Email":
                email = st.text_input("Enter your registered Email", key="fp_email")
                phone = ""
            else:
                phone = st.text_input("Enter your registered Phone", key="fp_phone")
                email = ""

            if st.button("Verify and Reset Password"):
                if check_user_contact(username, email=email, phone=phone):
                    new_password = st.text_input("Enter your new password", type="password", key="new_password")
                    confirm_password = st.text_input("Confirm your new password", type="password", key="confirm_password")
                    if new_password and confirm_password:
                        if new_password == confirm_password:
                            reset_password(username, new_password)
                            st.success("Password reset successful! Please login with your new password.")
                        else:
                            st.error("Passwords do not match.")
                    else:
                        st.info("Please enter and confirm your new password.")
                else:
                    st.error("Username and contact info do not match our records.")

        return  # Do not proceed until logged in

    # --- Logged in user dashboard below ---

    st.markdown(f"### Welcome, **{st.session_state.username}**! Your expenditure dashboard")

    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()

            st.session_state.debits_df = debits_df.copy()

            tab1, tab2 = st.tabs(["Expenses (Debits)💸", "Payments (Credits)💳"])
            with tab1:
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")

                if add_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.experimental_rerun()

                st.subheader("Your Expenses")
                edited_df = st.data_editor(
                    st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )

                save_button = st.button("Apply Changes", type="primary")
                if save_button:
                    for idx, row in edited_df.iterrows():
                        new_cat = row["Category"]
                        if new_cat == st.session_state.debits_df.at[idx, "Category"]:
                            continue

                        details = row["Details"]
                        st.session_state.debits_df.at[idx, "Category"] = new_cat
                        add_keyword_to_category(new_cat, details)

                st.subheader('Expense Summary')
                category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
                category_totals = category_totals.sort_values("Amount", ascending=False)

                st.dataframe(
                    category_totals,
                    column_config={
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
                    },
                    use_container_width=True,
                    hide_index=True
                )

                fig = px.pie(
                    category_totals,
                    values="Amount",
                    names="Category",
                    title="Expenses by Category"
                )
                st.plotly_chart(fig, use_container_width=True)

                st.title("Expense Bar Graph")
                # Using your df columns: Details (index 1), Amount (index 2), Category (index 3)
                fig_bar = px.bar(
                    df,
                    x="Details",
                    y="Amount",
                    color="Category",
                    title="Expense Distribution"
                )
                st.plotly_chart(fig_bar, use_container_width=True, key="expense_bar")

                st.subheader("Expense From Debit and Credit")
                try:
                    fig_pie = px.pie(df, values='Amount', names='Debit/Credit', title='Expense Breakdown')
                    st.plotly_chart(fig_pie)
                except Exception as e:
                    st.error(f"Error in Pie Chart: {e}")

            with tab2:
                st.subheader("Payments Summary")
                total_payments = credits_df["Amount"].sum()
                st.metric("Total Payments", f"{total_payments:,.2f} AED")
                st.write(credits_df)
                

if __name__ == "__main__":
    main()
