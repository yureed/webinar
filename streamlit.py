import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configurations
st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")

# Load Dataset
@st.cache_data

def load_data(file_path):
    data = pd.read_csv(file_path, encoding='latin1')
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    return data

data_path = './supermarket_sales.csv'  # Update path if necessary
data = load_data(data_path)



# Sidebar for Filters
st.sidebar.header("Filters")
selected_branch = st.sidebar.multiselect("Select Branch", options=data['Branch'].unique(), default=data['Branch'].unique())
selected_product = st.sidebar.multiselect("Select Product Line", options=data['Product line'].unique(), default=data['Product line'].unique())
selected_customer = st.sidebar.multiselect("Select Customer Type", options=data['Customer type'].unique(), default=data['Customer type'].unique())
min_date = data['Date'].min().date()
max_date = data['Date'].max().date()

# Sidebar Date Range Filter
st.sidebar.markdown(f"**Available Date Range:** `{min_date}` to `{max_date}`")
selected_date = st.sidebar.date_input(
    label="Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
# Filtered Data
filtered_data = data[(data['Branch'].isin(selected_branch)) &
                     (data['Product line'].isin(selected_product)) &
                     (data['Customer type'].isin(selected_customer)) &
                     (data['Date'] >= pd.to_datetime(selected_date[0])) &
                     (data['Date'] <= pd.to_datetime(selected_date[1]))]
# Calculate Metrics
total_sales = filtered_data['Total'].sum()
gross_income = filtered_data['gross income'].sum()
total_quantity = filtered_data['Quantity'].sum()
avg_rating = filtered_data['Rating'].mean()
sales_by_branch = filtered_data.groupby('Branch')['Total'].sum().reset_index()
sales_by_product = filtered_data.groupby('Product line')['Total'].sum().reset_index()
avg_rating_product = filtered_data.groupby('Product line')['Rating'].mean().reset_index()
sales_by_customer = filtered_data.groupby('Customer type')['Total'].sum().reset_index()
sales_by_payment = filtered_data.groupby('Payment')['Total'].sum().reset_index()
sales_trend = filtered_data.groupby('Date')['Total'].sum().reset_index()

# Header
st.markdown("""
<style>
    .header {
        background-color: #2C3E50;
        color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
<div class="header">
    <h1>Supermarket Sales Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# Key Metrics
st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Gross Income", value=f"${gross_income:,.2f}")
with col3:
    st.metric(label="Total Quantity", value=f"{total_quantity}")
with col4:
    st.metric(label="Average Rating", value=f"{avg_rating:.2f}")

# Visualizations
# Sales by Branch
st.markdown("### Sales by Branch")
fig_branch_sales = px.bar(
    sales_by_branch, x="Branch", y="Total", title="Total Sales by Branch", text="Total",
    color="Branch", color_discrete_sequence=px.colors.sequential.Teal
)
st.plotly_chart(fig_branch_sales, use_container_width=True)

# Sales and Ratings by Product Line
st.markdown("### Sales and Ratings by Product Line")
col1, col2 = st.columns(2)
with col1:
    fig_product_sales = px.bar(
        sales_by_product, x="Total", y="Product line", orientation="h", title="Sales by Product Line",
        text="Total", color="Product line", color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_product_sales, use_container_width=True)
with col2:
    fig_product_ratings = px.bar(
        avg_rating_product, x="Rating", y="Product line", orientation="h", title="Average Rating by Product Line",
        text="Rating", color="Product line", color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_product_ratings, use_container_width=True)

# Sales by Customer Type
st.markdown("### Sales by Customer Type")
fig_customer_sales = px.pie(
    sales_by_customer, names="Customer type", values="Total", title="Sales Distribution by Customer Type",
    color="Customer type", color_discrete_sequence=px.colors.sequential.Teal
)
st.plotly_chart(fig_customer_sales, use_container_width=True)

# Sales by Payment Method
st.markdown("### Sales by Payment Method")
fig_payment_sales = px.pie(
    sales_by_payment, 
    names="Payment", 
    values="Total", 
    title="Sales Distribution by Payment Method",
    color="Payment", 
    color_discrete_sequence=px.colors.sequential.Purples  # Note the change to 'Purples'
)

st.plotly_chart(fig_payment_sales, use_container_width=True)

# Sales Trends
st.markdown("### Sales Trends Over Time")
fig_sales_trend = px.line(
    sales_trend, x="Date", y="Total", title="Daily Sales Trend", markers=True,
    color_discrete_sequence=["#2C3E50"]
)
st.plotly_chart(fig_sales_trend, use_container_width=True)
