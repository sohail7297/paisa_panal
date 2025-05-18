# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import json
# # import os

# # st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# # # Login System
# # if "authenticated" not in st.session_state:
# #     st.session_state.authenticated = False

# # if not st.session_state.authenticated:
# #     st.title("PaisaPanel Login")
# #     username = st.text_input("Username")
# #     password = st.text_input("Password", type="password")
# #     login_button = st.button("Login")

# #     if login_button:
# #         if username == "admin" and password == "admin123":
# #             st.session_state.authenticated = True
# #             st.success("Login successful!")
# #             st.experimental_dialog(title="My Dialog")
# #         elif username == "sohail7297" and password == "sohail0852":
# #             st.session_state.authenticated = True
# #             st.success("Login successful!")
# #             st.experimental_dialog(title="My Dialog")
# #         else:
# #             ("Invalid username or password")
# #     st.stop()

# # category_file_path = "categories.json"

# # if "categories" not in st.session_state:
# #     st.session_state.categories = {
# #         "Uncategorized": [],
# #     }

# # if os.path.exists(category_file_path):
# #     with open(category_file_path, "r") as f:
# #         st.session_state.categories = json.load(f)


# # def save_categories():
# #     with open(category_file_path, "w") as f:
# #         json.dump(st.session_state.categories, f)


# # # def categorize_transactions(df):
# # #     df["Category"] = "Uncategorized"

# # #     for category, keywords in st.session_state.categories.items():
# # #         if category == "Uncategorized" or not keywords:
# # #             continue

# # #         cleaned_keywords = [keyword.lower().strip() for keyword in keywords]

# # #         for index, row in df.iterrows():
# # #             detail_text = row["Details"].lower().strip()
# # #             if any(keyword in detail_text for keyword in cleaned_keywords):
# # #                 df.at[index, "Category"] = category

# # #     return df

# # def categorize_transactions(df):
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


# # def load_transactions(uploaded_file):
# #     try:
# #         df = pd.read_csv(uploaded_file)
# #         df.columns = [col.strip() for col in df.columns]
# #         df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
# #         df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")

# #         return categorize_transactions(df)
# #     except Exception as e:
# #         str.error(f"Error processing file: {str(e)}")
# #         return None


# # def add_keyword_to_category(category, keyword_text):
# #     keyword_text = keyword_text.strip()
# #     if keyword_text and keyword_text not in st.session_state.categories[category]:
# #         st.session_state.categories[category].append(keyword_text)
# #         save_categories()
# #         return True
    
# #     return False


# # def main():
# #     st.title("PaisaPanel")

# #     uploaded_file = st.file_uploader("Welcome to Paisa Panel!💹💸💳 Please upload your transactions file.", type=["csv"])

# #     if uploaded_file is not None:
# #         df = load_transactions(uploaded_file)

# #         if df is not None:
# #             debits_df = df[df["Debit/Credit"] == "Debit"].copy()
# #             credits_df = df[df["Debit/Credit"] == "Credit"].copy()

# #             st.session_state.debits_df = debits_df.copy()

# #             tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
# #             with tab1:
# #                 category_input = st.text_input("New Category Name")
# #                 add_category_button = st.button("Add Category")

# #                 if add_category_button and category_input:
# #                     if category_input not in st.session_state.categories:
# #                         st.session_state.categories[category_input] = []
# #                         save_categories()
# #                         st.reload()

# #                 st.subheader("Your Expenses")
# #                 editable_debits = st.data_editor(
# #                     st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
# #                     column_config={
# #                         "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
# #                         "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
# #                         "Category": st.column_config.SelectboxColumn(
# #                             "Category", 
# #                             options=list(st.session_state.categories.keys())
# #                         )
# #                 },
# #                 hide_index=True,
# #                 use_container_width=True,
# #                 key="category_editor"
# #             )

# #             apply_changes_button = st.button("Apply Changes", type="primary")
# #             if apply_changes_button:
# #                 for index, row in editable_debits.iterrows():
# #                     new_category = row["Category"]
# #                     if new_category == st.session_state.debits_df.at[index, "Category"]:
# #                         continue
# #                     detail_text = row["Details"]
# #                     st.session_state.debits_df.at[index, "Category"] = new_category
# #                     add_keyword_to_category(new_category, detail_text)

# #             st.subheader('Expense Summary')
# #             category_summary = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
# #             category_summary = category_summary.sort_values("Amount", ascending=False)

# #             st.df(
# #                 category_summary,
# #                 column_config={
# #                     "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
# #                 },
                 
# #                 use_container_width=True, 
# #                 hide_index=True
# #             )

# #             fig = px.pie(
# #                 category_summary, 
# #                 values="Amount",
# #                 names="Category", 
# #                 title="Expenses by Category"
# #             )
# #             st.plotly_chart(fig, use_container_width=True)

# #             with tab2:
# #                 st.subheader("Payments Summary")
# #                 total_payments = credits_df["Amount"].sum()
# #                 st.metric("Total Payments", f"{total_payments:,.2f} AED")
# #                 st.write(credits_df)
# # main()

# # main()
# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import json
# # import os

# # st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# # # Add background image function
# # def add_bg_from_url():
# #     st.markdown(
# #          """
# #          <style>
# #             /* Make the image cover the entire background */
# #         .bg-img {
# #         position: fixed;
# #         top: 0;
# #         left: 0;
# #         width: 100vw;
# #         height: 100vh;
# #         z-index: -1; /* behind everything */
# #         object-fit: cover;
# #         opacity: 0.3; /* adjust transparency */
# #     }

# #     /* Make the main container background transparent */
# #     .main .block-container {
# #         background-color: transparent !important;
# #     }
# #     </style>

# #     <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80" class="bg-img" />
# #     """,
# #         unsafe_allow_html=True
# #     )

# # add_bg_from_url()

# # # Login System
# # if "authenticated" not in st.session_state:
# #     st.session_state.authenticated = False

# # if not st.session_state.authenticated:
# #     st.title("PaisaPanel Login")
# #     username = st.text_input("Username")
# #     password = st.text_input("Password", type="password")
# #     login_button = st.button("Login")

# #     if login_button:
# #         # Replace with your valid usernames and passwords
# #         valid_users = {
# #             "admin": "admin123",
# #             "sohail7297": "sohail0852"
# #         }
# #         if username in valid_users and password == valid_users[username]:
# #             st.session_state.authenticated = True
# #             st.success("Login successful!")
# #             st.experimental_dialog(title="My Dialog")
# #         else:
# #             ("Invalid username or password")
# #     st.stop()

# # category_file_path = "categories.json"

# # if "categories" not in st.session_state:
# #     st.session_state.categories = {"Uncategorized": []}

# # if os.path.exists(category_file_path):
# #     with open(category_file_path, "r") as file:
# #         st.session_state.categories = json.load(file)


# # def save_categories():
# #     with open(category_file_path, "w") as file:
# #         json.dump(st.session_state.categories, file)


# # def categorize_transactions(df):
# #     df["Category"] = "Uncategorized"

# #     for category, keywords in st.session_state.categories.items():
# #         if category == "Uncategorized" or not keywords:
# #             continue

# #         cleaned_keywords = [keyword.lower().strip() for keyword in keywords]

# #         for index, row in df.iterrows():
# #             detail_text = row["Details"].lower().strip()
# #             if any(keyword in detail_text for keyword in cleaned_keywords):
# #                 df.at[index, "Category"] = category

# #     return df


# # def load_transactions(uploaded_file):
# #     try:
# #         df = pd.read_csv(uploaded_file)
# #         df.columns = [col.strip() for col in df.columns]
# #         df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
# #         df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")

# #         return categorize_transactions(df)
# #     except Exception :
# #         (f"Error processing file: {s)}")
# #         return None


# # def add_keyword_to_category(category, keyword_text):
# #     keyword_text = keyword_text.strip()
# #     if keyword_text and keyword_text not in st.session_state.categories[category]:
# #         st.session_state.categories[category].append(keyword_text)
# #         save_categories()
# #         return True
# #     return False


# # def main():
# #     st.title("PaisaPanel")

# #     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

# #     if uploaded_file is not None:
# #         df = load_transactions(uploaded_file)

# #         if df is not None:
# #             debits_df = df[df["Debit/Credit"] == "Debit"].copy()
# #             credits_df = df[df["Debit/Credit"] == "Credit"].copy()

# #             st.session_state.debits_df = debits_df.copy()

# #             tab_expenses, tab_payments = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
# #             with tab_expenses:
# #                 category_input = st.text_input("New Category Name")
# #                 add_category_button = st.button("Add Category")

# #                 if add_category_button and category_input:
# #                     if category_input not in st.session_state.categories:
# #                         st.session_state.categories[category_input] = []
# #                         save_categories()
# #                         st.experimental_dialog(title="My Dialog")

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

# #                 st.df(category_summary, column_config={
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
# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import json
# # import os

# # st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# # # Add background image function
# # def add_bg_from_url():
# #     st.markdown(
# #          '''
# #          <style>
# #             .bg-img {
# #             position: fixed;
# #             top: 0;
# #             left: 0;
# #             width: 100vw;
# #             height: 100vh;
# #             z-index: -1;
# #             object-fit: cover;
# #             opacity: 0.3;
# #         }
# #         .main .block-container {
# #             background-color: transparent !important;
# #         }
# #         </style>
# #         <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80" class="bg-img" />
# #         ''',
# #         unsafe_allow_html=True
# #     )

# # add_bg_from_url()

# # if "authenticated" not in st.session_state:
# #     st.session_state.authenticated = False

# # if not st.session_state.authenticated:
# #     st.title("PaisaPanel Login")
# #     username = st.text_input("Username")
# #     password = st.text_input("Password", type="password")
# #     login_button = st.button("Login")

# #     valid_users = {
# #         "admin": "admin123",
# #         "sohail7297": "sohail0852"
# #     }
# #     if login_button:
# #         if username in valid_users and password == valid_users[username]:
# #             st.session_state.authenticated = True
# #             st.success("Login successful!")
# #         else:
# #             ("Invalid username or password")
# #     st.stop()

# # category_file_path = "categories.json"

# # if "categories" not in st.session_state:
# #     st.session_state.categories = {"Uncategorized": []}

# # if os.path.exists(category_file_path):
# #     with open(category_file_path, "r") as file:
# #         st.session_state.categories = json.load(file)


# # def save_categories():
# #     with open(category_file_path, "w") as file:
# #         json.dump(st.session_state.categories, file)


# # def categorize_transactions(df):
# #     df["Category"] = "Uncategorized"
# #     for category, keywords in st.session_state.categories.items():
# #         if category == "Uncategorized" or not keywords:
# #             continue
# #         cleaned_keywords = [keyword.lower().strip() for keyword in keywords]
# #         for index, row in df.iterrows():
# #             detail_text = str(row["Details"]).lower().strip()
# #             if any(keyword in detail_text for keyword in cleaned_keywords):
# #                 df.at[index, "Category"] = category
# #     return df


# # def load_transactions(uploaded_file):
# #     try:
# #         df = pd.read_csv(uploaded_file)
# #         df.columns = [col.strip() for col in df.columns]
# #         df["Amount"] = pd.to_numeric(df["Amount"].astype(str).str.replace(",", ""), errors='coerce')
# #         df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors='coerce')
# #         return categorize_transactions(df)
# #     except Exception :
# #         (f"Error processing file: {s)}")
# #         return None


# # def main():
# #     st.title("PaisaPanel")
# #     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
# #     if uploaded_file is not None:
# #         df = load_transactions(uploaded_file)
# #         if df is not None:
# #             st.df(df)


# # main()

# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import matplotlib as plt
# # import json
# # import os

# # st.set_page_config(page_title="PaisaPanel", page_icon="💰", layout="wide")

# # # Add background image function
# # def add_bg_from_url():
# #     st.markdown(
# #          '''
# #          <style>
# #             .bg-img {
# #             position: fixed;
# #             top: 0;
# #             left: 0;
# #             width: 100vw;
# #             height: 100vh;
# #             z-index: -1;
# #             object-fit: cover;
# #             opacity: 0.3;
# #         }
# #         .main .block-container {
# #             background-color: transparent !important;
# #         }
# #         </style>
# #         <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80" class="bg-img" />
# #         ''',
# #         unsafe_allow_html=True
# #     )

# # add_bg_from_url()

# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if not st.session_state.authenticated:
#     st.title("PaisaPanel Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     login_button = st.button("Login")

#     valid_users = {
#         "admin": "admin123",
#         "sohail7297": "sohail0852"
#     }
#     if login_button:
#         if username in valid_users and password == valid_users[username]:
#             st.session_state.authenticated = True
#             st.success("Login successful!")
#         else:
#             ("Invalid username or password")
#     st.stop()

# # category_file_path = "categories.json"

# # if "categories" not in st.session_state:
# #     st.session_state.categories = {"Uncategorized": []}

# # if os.path.exists(category_file_path):
# #     with open(category_file_path, "r") as file:
# #         st.session_state.categories = json.load(file)


# # def save_categories():
# #     with open(category_file_path, "w") as file:
# #         json.dump(st.session_state.categories, file)


# # def categorize_transactions(df):
# #     df["Category"] = "Uncategorized"
# #     for category, keywords in st.session_state.categories.items():
# #         if category == "Uncategorized" or not keywords:
# #             continue
# #         cleaned_keywords = [keyword.lower().strip() for keyword in keywords]
# #         for index, row in df.iterrows():
# #             detail_text = str(row["Details"]).lower().strip()
# #             if any(keyword in detail_text for keyword in cleaned_keywords):
# #                 df.at[index, "Category"] = category
# #     return df


# # def load_transactions(uploaded_file):
# #     try:
# #         df = pd.read_csv(uploaded_file)
# #         df.columns = [col.strip() for col in df.columns]
# #         df["Amount"] = pd.to_numeric(df["Amount"].astype(str).str.replace(",", ""), errors='coerce')
# #         df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y", errors='coerce')
# #         return categorize_transactions(df)
# #     except Exception :
# #         (f"Error processing file: {s)}")
# #         return None


# # def visualize_data(df):
# #     st.header("Data Visualizations")
# #     bar_chart = px.bar(df, x="Date", y="Amount", title="Amount vs. Date (Bar Chart)")
# #     st.plotly_chart(bar_chart)

# #     pie_chart = px.pie(df, values="Amount", names="Category", title="Amount Distribution by Category (Pie Chart)")
# #     st.plotly_chart(pie_chart)

# #     histogram = px.histogram(df, x="Amount", nbins=20, title="Amount Distribution (Histogram)")
# #     st.plotly_chart(histogram)


# # def main():
# #     st.title("PaisaPanel")
# #     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
# #     if uploaded_file is not None:
# #         df = load_transactions(uploaded_file)
# #         if df is not None:
# #             st.df(df)
# #             visualize_data(df)


# # main()


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import json
# import os

# st.set_page_config(page_title="Simple Finance App", page_icon="💰", layout="wide")

# category_file = "categories.json"

# if "categories" not in st.session_state:
#     st.session_state.categories = {
#         "Uncategorized": [],
#     }
    
# if os.path.exists(category_file):
#     with open(category_file, "r") as f:
#         st.session_state.categories = json.load(f)
        
# def save_categories():
#     with open(category_file, "w") as f:
#         json.dump(st.session_state.categories, f)

# def categorize_transactions(df):
#     df["Category"] = "Uncategorized"
    
#     for category, keywords in st.session_state.categories.items():
#         if category == "Uncategorized" or not keywords:
#             continue
        
#         lowered_keywords = [keyword.lower().strip() for keyword in keywords]
        
#         for idx, row in df.iterrows():
#             details = row["Details"].lower().strip()
#             if details in lowered_keywords:
#                 df.at[idx, "Category"] = category
                
#     return df  

# def load_transactions(file):
#     try:
#         df = pd.read_csv(file)
#         df.columns = [col.strip() for col in df.columns]
#         df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
#         df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y") 
        
#         return categorize_transactions(df)
#     except Exception as e:
#         st.error(f"Error processing file: {str(e)}")
#         return None

# def add_keyword_to_category(category, keyword):
#     keyword = keyword.strip()
#     if keyword and keyword not in st.session_state.categories[category]:
#         st.session_state.categories[category].append(keyword)
#         save_categories()
#         return True
    
#     return False

# def main():
#     st.title("Simple Finance Dashboard")
    
#     uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])
    
#     if uploaded_file is not None:
#         df = load_transactions(uploaded_file)
        
#         if df is not None:
#             debits_df = df[df["Debit/Credit"] == "Debit"].copy()
#             credits_df = df[df["Debit/Credit"] == "Credit"].copy()
            
#             st.session_state.debits_df = debits_df.copy()
            
#             tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
#             with tab1:
#                 new_category = st.text_input("New Category Name")
#                 add_button = st.button("Add Category")
                
#                 if add_button and new_category:
#                     if new_category not in st.session_state.categories:
#                         st.session_state.categories[new_category] = []
#                         save_categories()
#                         st.rerun()
                
#                 st.subheader("Your Expenses")
#                 edited_df = st.data_editor(
#                     st.session_state.debits_df[["Date", "Details", "Amount", "Category","GST"]],
#                     column_config={
#                         "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
#                         "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
#                         "Category": st.column_config.SelectboxColumn(
#                             "Category",
#                             options=list(st.session_state.categories.keys())
#                         )
#                     },
#                     hide_index=True,
#                     use_container_width=True,
#                     key="category_editor"
#                 )
                
#                 save_button = st.button("Apply Changes", type="primary")
#                 if save_button:
#                     for idx, row in edited_df.iterrows():
#                         new_category = row["Category"]
#                         if new_category == st.session_state.debits_df.at[idx, "Category"]:
#                             continue
                        
#                         details = row["Details"]
#                         st.session_state.debits_df.at[idx, "Category"] = new_category
#                         add_keyword_to_category(new_category, details)
                        
#                 st.subheader('Expense Summary')
#                 category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
#                 category_totals = category_totals.sort_values("Amount", ascending=False)
                
#                 st.dataframe(
#                     category_totals, 
#                     column_config={
#                      "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")   
#                     },
#                     use_container_width=True,
#                     hide_index=True
#                 )
                
#                 fig = px.pie(
#                     category_totals,
#                     values="Amount",
#                     names="Category",
#                     title="Expenses by Category"
#                 )
#                 st.plotly_chart(fig, use_container_width=True)
                
#             with tab2:
#                 st.subheader("Payments Summary")
#                 total_payments = credits_df["Amount"].sum()
#                 st.metric("Total Payments", f"{total_payments:,.2f} AED")
#                 st.write(credits_df)
        
# main()

import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="PAISA PANEL", page_icon="💰", layout="wide")


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Paisa Panel Login" \
    "Your expenditure tracking dashboard")
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
            st.success("Login successful! Check again to login and see your transactions")
        else:
            ("Invalid username or password. Plz retry!")
    st.stop()


category_file = "categories.json"

if "categories" not in st.session_state:
    st.session_state.categories = {
        "Uncategorized": [],
    }
    
if os.path.exists(category_file):
    with open(category_file, "r") as f:
        st.session_state.categories = json.load(f)
        
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

def main():
    st.title("Paisa Panel💹")
    st.markdown("""
    <style>
    .custom-title {
        font-family: 'Arial Black', sans-serif;
        font-size: 40px;
        color: #FF5733;
        text-align: center;
    }
    </style>
    <h1 class="custom-title">Welcome to paisa panal you can check you expenditure here</h1>
    """, 
    unsafe_allow_html=True)

    
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
                        st.rerun()
                
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
                        new_category = row["Category"]
                        if new_category == st.session_state.debits_df.at[idx, "Category"]:
                            continue
                        
                        details = row["Details"]
                        st.session_state.debits_df.at[idx, "Category"] = new_category
                        add_keyword_to_category(new_category, details)
                        
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

# Sample data for demonstration
                

                    # Plotting the bar graph using Plotly
                fig = px.bar(df, x=df.columns[1], y=df.columns[2], title='Expense Distribution', color=df.columns[3])
                st.plotly_chart(fig, use_container_width=True,  key="expense_bar")

                    # Display the bar graph using Streamlit
                # st.plotly_chart(fig)

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
        
main()