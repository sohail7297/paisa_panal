# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import json
# # import os

# # st.set_page_config(page_title="Simple Finance App", page_icon="💰", layout="wide")

# # file = "categories.json"

# # if "categories" not in st.session_state:
# #     st.session_state.categories = {
# #         "Uncategorized": [],
# #     }
    
# # if os.path.exists(file):
# #     with open(file, "r") as f:
# #         st.session_state.categories = json.load(f)
        
# # def SaveCategories():
# #     with open(file, "w") as f:
# #         json.dump(st.session_state.categories, f)

# # def CategorizeTrans(df):
# #     df["Category"] = "Uncategorized"
    
# #     for category, keywords in st.session_state.categories.items():
# #         if category == "Uncategorized" or not keywords:
# #             continue
        
# #         lowered_keywords = [keyword.lower().strip() for keyword in keywords]
        
# #         for idx, row in df.iterrows():
# #             details = row["Details"].lower().strip()
# #             if details in lowered_keywords:
# #                 df.at[idx, "Category"] = category
                
# #     return df  

# # def LoadTrans(file):
# #     try:
# #         df = pd.read_csv(file)
# #         df.columns = [col.strip() for col in df.columns]
# #         df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
# #         df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y") 
        
# #         return CategorizeTrans(df)
# #     except Exception as e:
# #         st.error(f"Error processing file: {str(e)}")
# #         return None

# # def AddKeyword(category, keyword):
# #     keyword = keyword.strip()
# #     if keyword and keyword not in st.session_state.categories[category]:
# #         st.session_state.categories[category].append(keyword)
# #         SaveCategories()
# #         return True
    
# #     return False

# # def main():
# #     st.title("PaisaPanel")
    
# #     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
    
# #     if uploaded_file is not None:
# #         df = LoadTrans(uploaded_file)
        
# #         if df is not None:
# #             debits_df = df[df["Debit/Credit"] == "Debit"].copy()
# #             credits_df = df[df["Debit/Credit"] == "Credit"].copy()
            
# #             st.session_state.debits_df = debits_df.copy()
            
# #             tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
# #             with tab1:
# #                 new_category = st.text_input("New Category Name")
# #                 add_button = st.button("Add Category")
                
# #                 if add_button and new_category:
# #                     if new_category not in st.session_state.categories:
# #                         st.session_state.categories[new_category] = []
# #                         SaveCategories()
# #                         st.rerun()
                
# #                 st.subheader("Your Expenses")
# #                 edited_df = st.data_editor(
# #                     st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
# #                     column_config={
# #                         "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
# #                         "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
# #                         "Category": st.column_config.SelectboxColumn(
# #                             "Category",
# #                             options=list(st.session_state.categories.keys())
# #                         )
# #                     },
# #                     hide_index=True,
# #                     use_container_width=True,
# #                     key="category_editor"
# #                 )
                
# #                 save_button = st.button("Apply Changes", type="primary")
# #                 if save_button:
# #                     for idx, row in edited_df.iterrows():
# #                         new_category = row["Category"]
# #                         if new_category == st.session_state.debits_df.at[idx, "Category"]:
# #                             continue
                        
# #                         details = row["Details"]
# #                         st.session_state.debits_df.at[idx, "Category"] = new_category
# #                      AddKeyword(new_category, details)
                        
# #                 st.subheader('Expense Summary')
# #                 category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
# #                 category_totals = category_totals.sort_values("Amount", ascending=False)
                
# #                 st.dataframe(
# #                     category_totals, 
# #                     column_config={
# #                      "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")   
# #                     },
# #                     use_container_width=True,
# #                     hide_index=True
# #                 )
                
# #                 fig = px.pie(
# #                     category_totals,
# #                     values="Amount",
# #                     names="Category",
# #                     title="Expenses by Category"
# #                 )
# #                 st.plotly_chart(fig, use_container_width=True)
                
# #             with tab2:
# #                 st.subheader("Payments Summary")
# #                 total_payments = credits_df["Amount"].sum()
# #                 st.metric("Total Payments", f"{total_payments:,.2f} AED")
# #                 st.write(credits_df)
        
# # main()

# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import json
# # import os

# # st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# # category_file_path = "categories.json"

# # if "categories" not in st.session_state:
# #     st.session_state.categories = {"Uncategorized": []}

# # if os.path.exists(category_file_path):
# #     with open(category_file_path, "r") as file:
# #         st.session_state.categories = json.load(file)


# # def save_categories():
# #     with open(category_file_path, "w") as file:
# #         json.dump(st.session_state.categories, file)


# # def categorize_transactions(dataframe):
# #     dataframe["Category"] = "Uncategorized"

# #     for category_name, keywords in st.session_state.categories.items():
# #         if category_name == "Uncategorized" or not keywords:
# #             continue

# #         cleaned_keywords = [keyword.lower().strip() for keyword in keywords]

# #         for index, row in dataframe.iterrows():
# #             detail_text = row["Details"].lower().strip()
# #             if any(keyword in detail_text for keyword in cleaned_keywords):
# #                 dataframe.at[index, "Category"] = category_name

# #     return dataframe


# # def load_transactions(uploaded_file):
# #     try:
# #         dataframe = pd.read_csv(uploaded_file)
# #         dataframe.columns = [col.strip() for col in dataframe.columns]
# #         dataframe["Amount"] = dataframe["Amount"].str.replace(",", "").astype(float)
# #         dataframe["Date"] = pd.to_datetime(dataframe["Date"], format="%d %b %Y")

# #         return categorize_transactions(dataframe)
# #     except Exception as error:
# #         st.error(f"Error processing file: {str(error)}")
# #         return None


# # def add_keyword_to_category(category_name, keyword_text):
# #     keyword_text = keyword_text.strip()
# #     if keyword_text and keyword_text not in st.session_state.categories[category_name]:
# #         st.session_state.categories[category_name].append(keyword_text)
# #         save_categories()
# #         return True
# #     return False


# # def main():
# #     st.title("PaisaPanel")

# #     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

# #     if uploaded_file is not None:
# #         dataframe = load_transactions(uploaded_file)

# #         if dataframe is not None:
# #             debits_df = dataframe[dataframe["Debit/Credit"] == "Debit"].copy()
# #             credits_df = dataframe[dataframe["Debit/Credit"] == "Credit"].copy()

# #             st.session_state.debits_df = debits_df.copy()

# #             tab_expenses, tab_payments = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
# #             with tab_expenses:
# #                 category_input = st.text_input("New Category Name")
# #                 add_category_button = st.button("Add Category")

# #                 if add_category_button and category_input:
# #                     if category_input not in st.session_state.categories:
# #                         st.session_state.categories[category_input] = []
# #                         save_categories()
# #                         st.experimental_rerun()

# #                 st.subheader("Your Expenses")
# #                 editable_debits = st.data_editor(
# #                     st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
# #                     column_config={
# #                         "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
# #                         "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
# #                         "Category": st.column_config.SelectboxColumn("Category", options=list(st.session_state.categories.keys()))
# #                     },
# #                     hide_index=True,
# #                     use_container_width=True,
# #                     key="category_editor"
# #                 )

# #                 apply_changes_button = st.button("Apply Changes", type="primary")
# #                 if apply_changes_button:
# #                     for index, row in editable_debits.iterrows():
# #                         new_category = row["Category"]
# #                         if new_category == st.session_state.debits_df.at[index, "Category"]:
# #                             continue
# #                         detail_text = row["Details"]
# #                         st.session_state.debits_df.at[index, "Category"] = new_category
# #                         add_keyword_to_category(new_category, detail_text)

# #                 st.subheader('Expense Summary')
# #                 category_summary = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
# #                 category_summary = category_summary.sort_values("Amount", ascending=False)

# #                 st.dataframe(category_summary, column_config={
# #                     "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
# #                 }, use_container_width=True, hide_index=True)

# #                 fig = px.pie(category_summary, values="Amount", names="Category", title="Expenses by Category")
# #                 st.plotly_chart(fig, use_container_width=True)

# #             with tab_payments:
# #                 st.subheader("Payments Summary")
# #                 total_credits = credits_df["Amount"].sum()
# #                 st.metric("Total Payments", f"{total_credits:,.2f} AED")
# #                 st.write(credits_df)


# # main()
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
#             st.experimental_rerun()
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
#                         st.experimental_rerun()

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

# Login System
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("PaisaPanel Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.experimental_rerun()
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
            detail_text = row["Details"].lower().strip()
            if any(keyword in detail_text for keyword in cleaned_keywords):
                dataframe.at[index, "Category"] = category_name

    return dataframe


def load_transactions(uploaded_file):
    try:
        dataframe = pd.read_csv(uploaded_file)
        dataframe.columns = [col.strip() for col in dataframe.columns]
        dataframe["Amount"] = dataframe["Amount"].str.replace(",", "").astype(float)
        dataframe["Date"] = pd.to_datetime(dataframe["Date"], format="%d %b %Y")

        return categorize_transactions(dataframe)
    except Exception as error:
        st.error(f"Error processing file: {str(error)}")
        return None


def add_keyword_to_category(category_name, keyword_text):
    keyword_text = keyword_text.strip()
    if keyword_text and keyword_text not in st.session_state.categories[category_name]:
        st.session_state.categories[category_name].append(keyword_text)
        save_categories()
        return True
    return False


def main():
    st.title("PaisaPanel")

    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

    if uploaded_file is not None:
        dataframe = load_transactions(uploaded_file)

        if dataframe is not None:
            debits_df = dataframe[dataframe["Debit/Credit"] == "Debit"].copy()
            credits_df = dataframe[dataframe["Debit/Credit"] == "Credit"].copy()

            st.session_state.debits_df = debits_df.copy()

            tab_expenses, tab_payments = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
            with tab_expenses:
                category_input = st.text_input("New Category Name")
                add_category_button = st.button("Add Category")

                if add_category_button and category_input:
                    if category_input not in st.session_state.categories:
                        st.session_state.categories[category_input] = []
                        save_categories()
                        st.experimental_rerun()

                st.subheader("Your Expenses")
                editable_debits = st.data_editor(
                    st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn("Category", options=list(st.session_state.categories.keys()))
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )

                apply_changes_button = st.button("Apply Changes", type="primary")
                if apply_changes_button:
                    for index, row in editable_debits.iterrows():
                        new_category = row["Category"]
                        if new_category == st.session_state.debits_df.at[index, "Category"]:
                            continue
                        detail_text = row["Details"]
                        st.session_state.debits_df.at[index, "Category"] = new_category
                        add_keyword_to_category(new_category, detail_text)

                st.subheader('Expense Summary')
                category_summary = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
                category_summary = category_summary.sort_values("Amount", ascending=False)

                st.dataframe(category_summary, column_config={
                    "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
                }, use_container_width=True, hide_index=True)

                fig = px.pie(category_summary, values="Amount", names="Category", title="Expenses by Category")
                st.plotly_chart(fig, use_container_width=True)

            with tab_payments:
                st.subheader("Payments Summary")
                total_credits = credits_df["Amount"].sum()
                st.metric("Total Payments", f"{total_credits:,.2f} AED")
                st.write(credits_df)


main()
