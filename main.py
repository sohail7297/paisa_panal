# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import json
# import os

# st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# # Login System
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if not st.session_state.authenticated:
#     st.title("PaisaPanel Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     login_button = st.button("Login")

#     if login_button:
#         if username == "admin" and password == "admin123":
#             st.session_state.authenticated = True
#             st.success("Login successful!")
#             st.experimental_dialog(title="My Dialog")
#         elif username == "sohail7297" and password == "sohail0852":
#             st.session_state.authenticated = True
#             st.success("Login successful!")
#             st.experimental_dialog(title="My Dialog")
#         else:
#             st.error("Invalid username or password")
#     st.stop()

# category_file_path = "categories.json"

# if "categories" not in st.session_state:
#     st.session_state.categories = {"Uncategorized": []}

# if os.path.exists(category_file_path):
#     with open(category_file_path, "r") as file:
#         st.session_state.categories = json.load(file)


# def save_categories():
#     with open(category_file_path, "w") as file:
#         json.dump(st.session_state.categories, file)


# def categorize_transactions(dataframe):
#     dataframe["Category"] = "Uncategorized"

#     for category_name, keywords in st.session_state.categories.items():
#         if category_name == "Uncategorized" or not keywords:
#             continue

#         cleaned_keywords = [keyword.lower().strip() for keyword in keywords]

#         for index, row in dataframe.iterrows():
#             detail_text = row["Details"].lower().strip()
#             if any(keyword in detail_text for keyword in cleaned_keywords):
#                 dataframe.at[index, "Category"] = category_name

#     return dataframe


# def load_transactions(uploaded_file):
#     try:
#         dataframe = pd.read_csv(uploaded_file)
#         dataframe.columns = [col.strip() for col in dataframe.columns]
#         dataframe["Amount"] = dataframe["Amount"].str.replace(",", "").astype(float)
#         dataframe["Date"] = pd.to_datetime(dataframe["Date"], format="%d %b %Y")

#         return categorize_transactions(dataframe)
#     except Exception as error:
#         st.error(f"Error processing file: {str(error)}")
#         return None


# def add_keyword_to_category(category_name, keyword_text):
#     keyword_text = keyword_text.strip()
#     if keyword_text and keyword_text not in st.session_state.categories[category_name]:
#         st.session_state.categories[category_name].append(keyword_text)
#         save_categories()
#         return True
#     return False


# def main():
#     st.title("PaisaPanel")

#     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

#     if uploaded_file is not None:
#         dataframe = load_transactions(uploaded_file)

#         if dataframe is not None:
#             debits_df = dataframe[dataframe["Debit/Credit"] == "Debit"].copy()
#             credits_df = dataframe[dataframe["Debit/Credit"] == "Credit"].copy()

#             st.session_state.debits_df = debits_df.copy()

#             tab_expenses, tab_payments = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
#             with tab_expenses:
#                 category_input = st.text_input("New Category Name")
#                 add_category_button = st.button("Add Category")

#                 if add_category_button and category_input:
#                     if category_input not in st.session_state.categories:
#                         st.session_state.categories[category_input] = []
#                         save_categories()
#                         sload()

#                 st.subheader("Your Expenses")
#                 editable_debits = st.data_editor(
#                     st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
#                     column_config={
#                         "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
#                         "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
#                         "Category": st.column_config.SelectboxColumn("Category", options=list(st.session_state.categories.keys()))
#                     },
#                     hide_index=True,
#                     use_container_width=True,
#                     key="category_editor"
#                 )

#                 apply_changes_button = st.button("Apply Changes", type="primary")
#                 if apply_changes_button:
#                     for index, row in editable_debits.iterrows():
#                         new_category = row["Category"]
#                         if new_category == st.session_state.debits_df.at[index, "Category"]:
#                             continue
#                         detail_text = row["Details"]
#                         st.session_state.debits_df.at[index, "Category"] = new_category
#                         add_keyword_to_category(new_category, detail_text)

#                 st.subheader('Expense Summary')
#                 category_summary = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
#                 category_summary = category_summary.sort_values("Amount", ascending=False)

#                 st.dataframe(category_summary, column_config={
#                     "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
#                 }, use_container_width=True, hide_index=True)

#                 fig = px.pie(category_summary, values="Amount", names="Category", title="Expenses by Category")
#                 st.plotly_chart(fig, use_container_width=True)

#             with tab_payments:
#                 st.subheader("Payments Summary")
#                 total_credits = credits_df["Amount"].sum()
#                 st.metric("Total Payments", f"{total_credits:,.2f} AED")
#                 st.write(credits_df)


# main()
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import json
# import os

# st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# # Add background image function
# def add_bg_from_url():
#     st.markdown(
#          """
#          <style>
#             /* Make the image cover the entire background */
#         .bg-img {
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100vw;
#         height: 100vh;
#         z-index: -1; /* behind everything */
#         object-fit: cover;
#         opacity: 0.3; /* adjust transparency */
#     }

#     /* Make the main container background transparent */
#     .main .block-container {
#         background-color: transparent !important;
#     }
#     </style>

#     <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80" class="bg-img" />
#     """,
#         unsafe_allow_html=True
#     )

# add_bg_from_url()

# # Login System
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if not st.session_state.authenticated:
#     st.title("PaisaPanel Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     login_button = st.button("Login")

#     if login_button:
#         # Replace with your valid usernames and passwords
#         valid_users = {
#             "admin": "admin123",
#             "sohail7297": "sohail0852"
#         }
#         if username in valid_users and password == valid_users[username]:
#             st.session_state.authenticated = True
#             st.success("Login successful!")
#             st.experimental_dialog(title="My Dialog")
#         else:
#             st.error("Invalid username or password")
#     st.stop()

# category_file_path = "categories.json"

# if "categories" not in st.session_state:
#     st.session_state.categories = {"Uncategorized": []}

# if os.path.exists(category_file_path):
#     with open(category_file_path, "r") as file:
#         st.session_state.categories = json.load(file)


# def save_categories():
#     with open(category_file_path, "w") as file:
#         json.dump(st.session_state.categories, file)


# def categorize_transactions(dataframe):
#     dataframe["Category"] = "Uncategorized"

#     for category_name, keywords in st.session_state.categories.items():
#         if category_name == "Uncategorized" or not keywords:
#             continue

#         cleaned_keywords = [keyword.lower().strip() for keyword in keywords]

#         for index, row in dataframe.iterrows():
#             detail_text = row["Details"].lower().strip()
#             if any(keyword in detail_text for keyword in cleaned_keywords):
#                 dataframe.at[index, "Category"] = category_name

#     return dataframe


# def load_transactions(uploaded_file):
#     try:
#         dataframe = pd.read_csv(uploaded_file)
#         dataframe.columns = [col.strip() for col in dataframe.columns]
#         dataframe["Amount"] = dataframe["Amount"].str.replace(",", "").astype(float)
#         dataframe["Date"] = pd.to_datetime(dataframe["Date"], format="%d %b %Y")

#         return categorize_transactions(dataframe)
#     except Exception as error:
#         st.error(f"Error processing file: {str(error)}")
#         return None


# def add_keyword_to_category(category_name, keyword_text):
#     keyword_text = keyword_text.strip()
#     if keyword_text and keyword_text not in st.session_state.categories[category_name]:
#         st.session_state.categories[category_name].append(keyword_text)
#         save_categories()
#         return True
#     return False


# def main():
#     st.title("PaisaPanel")

#     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

#     if uploaded_file is not None:
#         dataframe = load_transactions(uploaded_file)

#         if dataframe is not None:
#             debits_df = dataframe[dataframe["Debit/Credit"] == "Debit"].copy()
#             credits_df = dataframe[dataframe["Debit/Credit"] == "Credit"].copy()

#             st.session_state.debits_df = debits_df.copy()

#             tab_expenses, tab_payments = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
#             with tab_expenses:
#                 category_input = st.text_input("New Category Name")
#                 add_category_button = st.button("Add Category")

#                 if add_category_button and category_input:
#                     if category_input not in st.session_state.categories:
#                         st.session_state.categories[category_input] = []
#                         save_categories()
#                         st.experimental_dialog(title="My Dialog")

#                 st.subheader("Your Expenses")
#                 editable_debits = st.data_editor(
#                     st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
#                     column_config={
#                         "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
#                         "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
#                         "Category": st.column_config.SelectboxColumn("Category", options=list(st.session_state.categories.keys()))
#                     },
#                     hide_index=True,
#                     use_container_width=True,
#                     key="category_editor"
#                 )

#                 apply_changes_button = st.button("Apply Changes", type="primary")
#                 if apply_changes_button:
#                     for index, row in editable_debits.iterrows():
#                         new_category = row["Category"]
#                         if new_category == st.session_state.debits_df.at[index, "Category"]:
#                             continue
#                         detail_text = row["Details"]
#                         st.session_state.debits_df.at[index, "Category"] = new_category
#                         add_keyword_to_category(new_category, detail_text)

#                 st.subheader('Expense Summary')
#                 category_summary = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
#                 category_summary = category_summary.sort_values("Amount", ascending=False)

#                 st.dataframe(category_summary, column_config={
#                     "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
#                 }, use_container_width=True, hide_index=True)

#                 fig = px.pie(category_summary, values="Amount", names="Category", title="Expenses by Category")
#                 st.plotly_chart(fig, use_container_width=True)

#             with tab_payments:
#                 st.subheader("Payments Summary")
#                 total_credits = credits_df["Amount"].sum()
#                 st.metric("Total Payments", f"{total_credits:,.2f} AED")
#                 st.write(credits_df)


# main()
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# Add background image function
def add_bg_from_url():
    st.markdown(
         '''
         <style>
            .bg-img {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            object-fit: cover;
            opacity: 0.3;
        }
        .main .block-container {
            background-color: transparent !important;
        }
        </style>
        <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80" class="bg-img" />
        ''',
        unsafe_allow_html=True
    )

add_bg_from_url()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("PaisaPanel Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    valid_users = {
        "admin": "admin123",
        "sohail7297": "sohail0852"
    }
    if login_button:
        if username in valid_users and password == valid_users[username]:
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")
    st.stop()

category_file_path = "categories.json"

if "categories" not in st.session_state:
    st.session_state.categories = {"Uncategorized": []}

if os.path.exists(category_file_path):
    with open(category_file_path, "r") as file:
        st.session_state.categories = json.load(file)


def save_categories():
    with open(category_file_path, "w") as file:
        json.dump(st.session_state.categories, file)


def categorize_transactions(dataframe):
    dataframe["Category"] = "Uncategorized"
    for category_name, keywords in st.session_state.categories.items():
        if category_name == "Uncategorized" or not keywords:
            continue
        cleaned_keywords = [keyword.lower().strip() for keyword in keywords]
        for index, row in dataframe.iterrows():
            detail_text = str(row["Details"]).lower().strip()
            if any(keyword in detail_text for keyword in cleaned_keywords):
                dataframe.at[index, "Category"] = category_name
    return dataframe


def load_transactions(uploaded_file):
    try:
        dataframe = pd.read_csv(uploaded_file)
        dataframe.columns = [col.strip() for col in dataframe.columns]
        dataframe["Amount"] = pd.to_numeric(dataframe["Amount"].astype(str).str.replace(",", ""), errors='coerce')
        dataframe["Date"] = pd.to_datetime(dataframe["Date"], format="%d %b %Y", errors='coerce')
        return categorize_transactions(dataframe)
    except Exception as error:
        st.error(f"Error processing file: {str(error)}")
        return None


def main():
    st.title("PaisaPanel")
    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
    if uploaded_file is not None:
        dataframe = load_transactions(uploaded_file)
        if dataframe is not None:
            st.dataframe(dataframe)


main()
