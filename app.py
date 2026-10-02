import streamlit as st
import pandas as pd

# Page Config

st.set_page_config(
    page_title="Customer Retention Dashboard",
    layout="wide"
)

st.title("Customer Engagement & Product Utilization Analytics")

# Load Data

df = pd.read_csv("European_Bank.csv")

# Fixed threshold - must match notebook definition, do not recompute after filtering
global_balance_median = df["Balance"].median()

# Filters

st.sidebar.header("Filters")

activity_filter = st.sidebar.selectbox(
    "Activity Status",
    ["All", "Active", "Inactive"]
)

product_filter = st.sidebar.slider(
    "Number of Products",
    1,
    4,
    1
)

balance_filter = st.sidebar.slider(
    "Minimum Balance",
    0,
    int(df["Balance"].max()),
    0
)

salary_filter = st.sidebar.slider(
    "Minimum Salary",
    0,
    int(df["EstimatedSalary"].max()),
    0
)

# Apply Filters

filtered_df = df.copy()

if activity_filter == "Active":
    filtered_df = filtered_df[
        filtered_df["IsActiveMember"] == 1
    ]

elif activity_filter == "Inactive":
    filtered_df = filtered_df[
        filtered_df["IsActiveMember"] == 0
    ]

filtered_df = filtered_df[
    filtered_df["NumOfProducts"] >= product_filter
]

filtered_df = filtered_df[
    filtered_df["Balance"] >= balance_filter
]

filtered_df = filtered_df[
    filtered_df["EstimatedSalary"] >= salary_filter
]

# Guard against empty filter results

if filtered_df.empty:
    st.warning("No customers match the selected filters. Try adjusting them.")
    st.stop()

# Engagement vs Churn Overview

st.header("Engagement vs Churn Overview")

col1, col2 = st.columns(2)

total_customers = len(filtered_df)

churn_rate = (
    filtered_df["Exited"].mean() * 100
)

col1.metric(
    "Total Customers",
    total_customers
)

col2.metric(
    "Churn Rate %",
    round(churn_rate, 2)
)

activity_churn = (
    filtered_df
    .groupby("IsActiveMember")["Exited"]
    .mean()
)

activity_churn.index = activity_churn.index.map({0: "Inactive", 1: "Active"})

st.bar_chart(activity_churn)

# engagement segmentation - same logic as notebook

def engagement_segment(row):
    if row["IsActiveMember"] == 1:
        if row["NumOfProducts"] >= 2:
            return "Active Engaged"
        else:
            return "Active Low-Product"
    else:
        if row["Balance"] > global_balance_median:
            return "Inactive High-Balance"
        else:
            return "Inactive Disengaged"

filtered_df["EngagementSegment"] = filtered_df.apply(engagement_segment, axis=1)

segment_churn = (
    filtered_df
    .groupby("EngagementSegment")["Exited"]
    .mean()
)

st.subheader("Churn Rate by Engagement Segment")
st.bar_chart(segment_churn)

# Product Utilization Impact Analysis

st.header("Product Utilization Impact Analysis")

product_churn = (
    filtered_df
    .groupby("NumOfProducts")["Exited"]
    .mean()
)

st.bar_chart(product_churn)

# High Value Disengaged Customer Detector

st.header("High Value Disengaged Customer Detector")

high_balance = global_balance_median

high_value_customers = filtered_df[
    (filtered_df["Balance"] > high_balance)
    &
    (filtered_df["IsActiveMember"] == 0)
]

st.metric(
    "High Value Disengaged Customers",
    len(high_value_customers)
)

st.dataframe(high_value_customers)

# Retention Strength Scoring Panel

st.header("Retention Strength Scoring Panel")

product_depth_index = (
    filtered_df["NumOfProducts"].mean()
)

active_churn = filtered_df[
    filtered_df["IsActiveMember"] == 1
]["Exited"].mean()

inactive_churn = filtered_df[
    filtered_df["IsActiveMember"] == 0
]["Exited"].mean()

if active_churn != 0:
    engagement_retention_ratio = (
        inactive_churn / active_churn
    )
else:
    engagement_retention_ratio = 0

# High-Balance Disengagement Rate

high_balance_customers = filtered_df[filtered_df["Balance"] > global_balance_median]

if len(high_balance_customers) > 0:
    high_balance_disengagement_rate = (
        high_balance_customers[high_balance_customers["IsActiveMember"] == 0].shape[0]
        / high_balance_customers.shape[0] * 100
    )
else:
    high_balance_disengagement_rate = 0

# Credit Card Effectiveness Score

churn_with_card = filtered_df[filtered_df["HasCrCard"] == 1]["Exited"].mean()
churn_without_card = filtered_df[filtered_df["HasCrCard"] == 0]["Exited"].mean()
credit_card_effectiveness_score = churn_without_card - churn_with_card

# Relationship Strength Index

filtered_df["RelationshipStrengthIndex"] = (
    filtered_df["IsActiveMember"] + (filtered_df["NumOfProducts"] / filtered_df["NumOfProducts"].max())
)
relationship_strength_index = filtered_df["RelationshipStrengthIndex"].mean()

col1, col2 = st.columns(2)

col1.metric(
    "Product Depth Index",
    round(product_depth_index, 2)
)

col2.metric(
    "Engagement Retention Ratio",
    round(engagement_retention_ratio, 2)
)

col3, col4, col5 = st.columns(3)

col3.metric(
    "High-Balance Disengagement %",
    round(high_balance_disengagement_rate, 2)
)

col4.metric(
    "Credit Card Effectiveness Score",
    round(credit_card_effectiveness_score, 4)
)

col5.metric(
    "Relationship Strength Index",
    round(relationship_strength_index, 2)
)

# Filtered Dataset

st.header("Filtered Dataset")

st.dataframe(filtered_df)