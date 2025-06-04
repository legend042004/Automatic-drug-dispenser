import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("neon_sales_data.csv")
df['s_date'] = pd.to_datetime(df['s_date'])
df['total_amount'] = df['Quantity'] * df['unit_price']

# Sidebar filters
st.sidebar.title("Filters")
category_filter = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())
location_filter = st.sidebar.multiselect("Dispenser Location", options=df['Dispenser_location'].unique(), default=df['Dispenser_location'].unique())

# Filtered dataframe
filtered_df = df[(df['Category'].isin(category_filter)) & (df['Dispenser_location'].isin(location_filter))]

# KPIs
total_quantity = filtered_df['Quantity'].sum()
avg_sale_value = round(filtered_df['unit_price'].mean(), 2)
total_revenue = filtered_df['total_amount'].sum()

# Layout
st.title("MEDI-CLIQ")
st.markdown("### Live Dashboard Connected to Neon DB")

col1, col2, col3 = st.columns(3)
col1.metric("Total Quantity", total_quantity)
col2.metric("Avg Sale Value", avg_sale_value)
col3.metric("Sum of total amount", f"{total_revenue/1000:.2f}K")

# Charts
amount_by_med = filtered_df.groupby('Med_name')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=False)
quantity_by_med = filtered_df.groupby('Med_name')['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=False)

monthly_data = filtered_df.groupby(filtered_df['s_date'].dt.to_period('M')).agg({
    'Quantity': 'sum',
    'total_amount': 'sum'
}).reset_index()
monthly_data['s_date'] = monthly_data['s_date'].dt.to_timestamp()

# First row: bar charts
col1, col2 = st.columns(2)
col1.plotly_chart(px.bar(amount_by_med, x='Med_name', y='total_amount', title='Sum of total amount by Med_name'), use_container_width=True)
col2.plotly_chart(px.bar(quantity_by_med, x='Quantity', y='Med_name', orientation='h', title='Sum of Quantity by Med_name'), use_container_width=True)

# Line chart
fig_line = px.line(monthly_data, x='s_date', y=['Quantity', 'total_amount'], labels={'value': 'Count/Amount', 's_date': 'Month'},
                   title='Total Quantity and Total Revenue by Month')
st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
