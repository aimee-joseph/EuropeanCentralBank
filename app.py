import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Customer Churn Analysis - European Central Bank", page_icon = "ECB_Logo.png", layout = "wide")

ECB_BLUE = "#003299"
ECB_YELLOW = "#FFF315"

st.title("Bank Customer Churn Analysis")

data = pd.read_csv("churn_analysis_cleaned.csv")

col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    st.image("ECB_Logo.png", width = 110)

st.sidebar.markdown("---")

page = st.sidebar.selectbox("Navigate", ["Overview", "Data Exploration", "Customer Insights"])

# GLOBAL FILTERS (applied everywhere now)
st.sidebar.subheader("Filters")
geography = st.sidebar.multiselect("Select Country", options = data["Geography"].unique(), default = data["Geography"].unique())
gender = st.sidebar.multiselect("Select Gender", options = data["Gender"].unique(), default = data["Gender"].unique())
active_status = st.sidebar.multiselect("Active Member", options = [0, 1], default = [0, 1], format_func = lambda x: "Active" if x == 1 else "Inactive")

filtered_data = data[(data["Geography"].isin(geography)) & (data["Gender"].isin(gender)) & (data["IsActiveMember"].isin(active_status))]

# ================= OVERVIEW =================
if page == "Overview":
    st.header("Overview")

    total_customers = filtered_data.shape[0]
    churned = filtered_data["Exited"].sum()
    retained = total_customers - churned
    churn_rate = filtered_data["Exited"].mean()*100
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", total_customers)
    col2.metric("Churned", churned, delta = f"{churn_rate:.2f}%")
    col3.metric("Retained", retained)
    col4.metric("Churn Rate (%)", round(churn_rate, 2))

    st.markdown("---")

    st.subheader("Churn Distribution")
    churn_counts = filtered_data["Exited"].value_counts().reset_index()
    churn_counts.columns = ["Status", "Count"]
    churn_counts["Status"] = churn_counts["Status"].map({0: "Retained", 1: "Churned"})
    fig = px.pie(churn_counts, names = "Status", values = "Count", color = "Status", color_discrete_map = {"Retained": ECB_BLUE, "Churned": ECB_YELLOW})
    st.plotly_chart(fig, use_container_width = True)

    st.subheader("Geography-wise Churn")
    geo_churn = filtered_data.groupby("Geography")["Exited"].mean().reset_index()
    fig_geo = px.bar(geo_churn, x = "Geography", y = "Exited", color_discrete_sequence = [ECB_BLUE], labels = {"Exited": "Churn Rate"})
    fig_geo.update_yaxes(tickformat = ".0%")
    st.plotly_chart(fig_geo, use_container_width = True)

# ================= DATA EXPLORATION =================
if page == "Data Exploration":
    st.header("Data Exploration")

    st.subheader("Filtered Data")
    st.dataframe(filtered_data, use_container_width = True)

    st.subheader("Summary")
    total = filtered_data.shape[0]
    churned = filtered_data["Exited"].sum()
    churn_rate = filtered_data["Exited"].mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Customers", total)
    col2.metric("Churned", churned)
    col3.metric("Churn Rate (%)", round(churn_rate, 2))

# ================= CUSTOMER INSIGHTS =================
if page == "Customer Insights":
    st.header("Customer Insights")

    tab1, tab2, tab3 = st.tabs(["Behavioral", "Financial", "High Value"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            churn_products = filtered_data.groupby("NumOfProducts")["Exited"].mean().reset_index()
            fig1 = px.bar(churn_products, x = "NumOfProducts", y = "Exited", title = "Churn by Number of Products", color_discrete_sequence = [ECB_BLUE], labels = {"NumOfProducts": "Number of Products"})
            fig1.update_yaxes(tickformat = ".0%")
            st.plotly_chart(fig1, use_container_width = True)

        with col2:
            churn_active = filtered_data.groupby("IsActiveMember")["Exited"].mean().reset_index()
            fig2 = px.bar(churn_active, x = "IsActiveMember", y = "Exited", title = "Churn by Activity Status", color_discrete_sequence = [ECB_BLUE], labels = {"IsActiveMember": "Activity"})
            fig2.update_xaxes(tickvals = [0, 1], ticktext = ["Inactive", "Active"])
            fig2.update_yaxes(tickformat = ".0%")
            st.plotly_chart(fig2, use_container_width = True)

        st.subheader("Churn by Age Group")
        age_bins = [0, 30, 45, 60, 100]
        age_labels = ["<30", "30-45", "46-60", "60+"]
        filtered_data["AgeGroup"] = pd.cut(filtered_data["Age"], bins = age_bins, labels = age_labels)
        churn_age = filtered_data.groupby("AgeGroup")["Exited"].mean().reset_index()
        fig_age = px.bar(churn_age, x = "AgeGroup", y = "Exited", color_discrete_sequence = [ECB_BLUE], labels = {"AgeGroup": "Age Group", "Exited": "Churn Rate"})
        fig_age.update_yaxes(tickformat = ".0%")
        st.plotly_chart(fig_age, use_container_width = True)

    with tab2:
        churn_balance = filtered_data.groupby("BalanceSegment")["Exited"].mean().reset_index()
        fig3 = px.bar(churn_balance, x = "BalanceSegment", y = "Exited", title = "Churn by Balance Segment", color_discrete_sequence = [ECB_BLUE], labels = {"BalanceSegment": "Balance Segment"})
        fig3.update_yaxes(tickformat = ".0%")
        st.plotly_chart(fig3, use_container_width = True)

        st.subheader("Churn by Tenure Group")
        tenure_bins = [0, 3, 7, 10]
        tenure_labels = ["New", "Mid-term", "Long-term"]
        filtered_data["TenureGroup"] = pd.cut(filtered_data["Tenure"], bins = tenure_bins, labels = tenure_labels)
        churn_tenure = filtered_data.groupby("TenureGroup")["Exited"].mean().reset_index()
        fig_tenure = px.bar(churn_tenure, x = "TenureGroup", y = "Exited", color_discrete_sequence = [ECB_BLUE], labels = {"TenureGroup": "Tenure Group", "Exited": "Churn Rate"})
        fig_tenure.update_yaxes(tickformat = ".0%")
        st.plotly_chart(fig_tenure, use_container_width = True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            churn_high_value = filtered_data.groupby("HighValueCustomer")["Exited"].mean().reset_index()
            fig4 = px.bar(churn_high_value, x = "HighValueCustomer", y = "Exited", title = "High Value Customer Churn", color_discrete_sequence = [ECB_BLUE], labels = {"HighValueCustomer": "High Value Customer"})
            fig4.update_xaxes(tickvals = [0, 1], ticktext = ["Regular", "High Value"])
            fig4.update_yaxes(tickformat = ".0%")
            st.plotly_chart(fig4, use_container_width = True)

        with col2:
            hv_data = filtered_data[(filtered_data["Exited"] == 1) & (filtered_data["HighValueCustomer"] == 1)]
            geo_counts = hv_data["Geography"].value_counts().reset_index()
            geo_counts.columns = ["Geography", "Count"]
            fig5 = px.pie(geo_counts, names = "Geography", values = "Count", title = "High Value Churn by Geography")
            st.plotly_chart(fig5, use_container_width = True)