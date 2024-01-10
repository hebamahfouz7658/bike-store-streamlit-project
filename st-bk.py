import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title='Bike Store Dashboard', page_icon=':bar_chart:', layout='wide')

st.snow()

# Title with custom styling
st.title("Bike Store Dashboard")
st.markdown(
    """
    <style>
        .title-container {
            display: flex;
            align-items: center;
            border-bottom: 2px solid #000; /* Border under the container */
            padding-bottom: 10px; /* Adjust the padding as needed */
            margin-bottom: 20px; /* Adjust the margin as needed */
        }

        .bike-icon {
            font-size: 2em;
            margin-right: 10px;
        }

        .title-text {
            font-size: 1.5em;
            font-weight: bold;
        }
    </style>
    <div class="title-container">
        <span class="bike-icon">🚴</span>
        <span class="title-text">Bike Store Data analysis</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Load Dataset
sales = pd.read_csv('cleaned_data.csv')

# Drop duplicates
sales.drop_duplicates(inplace=True)

# Multiselect for filtering by year
selected_years = st.sidebar.multiselect("Select Year(s)", sorted(sales['Year'].unique()))
selected_gender = st.multiselect('Select Customer Gender', sales['Customer_Gender'].unique(), sales['Customer_Gender'].unique())

st.sidebar.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRXMCo5W8HO0eKoEEKbKG6NlIvB5dCC_ciPLU2NXEO0obRr5IOZz2uV5hN1r57nHhFzRc&usqp=CAU', width=280)

# Explore Global Bike Store Sales Data
st.markdown("## Exploring Global Bike Store Sales Data")

# Task 1: Familiarizing with the Data
st.markdown("### Task 1: Familiarizing with the Data")
st.write(sales.head())

# Filter data based on selected years
filtered_sales = sales[sales['Year'].isin(selected_years)]

# Task 2: Exploring Customer and Order Statistics
st.markdown("### Task 2: Exploring Customer and Order Statistics")

# Check if the column is numeric before applying round
if 'Customer_Age' in filtered_sales.columns and pd.api.types.is_numeric_dtype(filtered_sales['Customer_Age']):
    st.write("Mean Age of Customers:", round(filtered_sales['Customer_Age'].mean()))

# Check and handle NaN values before converting to integer
if 'Order_Quantity' in filtered_sales.columns and pd.api.types.is_numeric_dtype(filtered_sales['Order_Quantity']):
    order_quantity_mean = filtered_sales['Order_Quantity'].mean()
    st.write("Mean Order Quantity:", round(order_quantity_mean) if not pd.isna(order_quantity_mean) else 0)

# Visualizations
st.subheader("Visualizations:")

# Interactive KDE plot using Plotly Express
if 'Customer_Age' in filtered_sales.columns:
    fig_customer_age = px.histogram(filtered_sales, x='Customer_Age', nbins=20, title="Density (KDE) of Customer Age")
    st.plotly_chart(fig_customer_age)

# Interactive Box plot using Plotly Express
if 'Order_Quantity' in filtered_sales.columns:
    fig_order_quantity = px.box(filtered_sales, x='Order_Quantity', title="Box Plot of Order Quantity",
                                color_discrete_sequence=['lightgreen'])
    st.plotly_chart(fig_order_quantity)

# Task 3: Analyzing Sales Trends
st.subheader("Task 3: Analyzing Sales Trends")
sales_sum_revenue = filtered_sales.groupby('Year')['Revenue'].sum().reset_index()

# Line plot using Plotly Express
fig_sales_revenue = px.line(sales_sum_revenue, x='Year', y='Revenue', title='Revenue Trends by Year')
fig_sales_revenue.update_layout(xaxis_title='Year', yaxis_title='Revenue')
# Show the plot in Streamlit
st.plotly_chart(fig_sales_revenue)

# Pie chart for revenue distribution by year
sales_year = filtered_sales.groupby('Year')['Revenue'].sum().reset_index()
fig_pie = px.pie(sales_year, values='Revenue', names='Year', title='Revenue Distribution by Year',
                 labels={'Year': 'Year'})
st.plotly_chart(fig_pie)

# Task 4: Regional Sales Comparison
st.markdown("### Task 4: Regional Sales Comparison")
st.write("Country with the highest quantity of sales:")
# Group by Country and sum Order_Quantity
country_sales = sales.groupby('Country')['Order_Quantity'].sum().reset_index()

# Create a bar chart using Plotly Express
fig_country_sales = px.bar(country_sales, x='Country', y='Order_Quantity', title='Order Quantity by Country')
fig_country_sales.update_layout(xaxis_title='Country', yaxis_title='Order Quantity')

# Display the chart using Streamlit
st.plotly_chart(fig_country_sales)

# Task 5: Relationship Exploration
st.markdown("### Task 5: Relationship Exploration")
st.write("Scatter Plot - Unit Cost vs Unit Price:")
fig_scatter = plt.figure(figsize=(8, 6))
sns.scatterplot(x=sales['Unit_Cost'], y=sales['Unit_Price'])
plt.xlabel("Unit Cost")
plt.ylabel("Unit Price")
plt.title("Scatter Plot - Unit Cost vs Unit Price")
st.pyplot(fig_scatter)

# Task 6: Temporal Analysis
st.subheader("Task 6: Temporal Analysis")
st.write("Temporal Analysis of Sales:")
sales['Calculated_Date'] = pd.to_datetime(sales[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1))
sales_by_date = sales.groupby('Calculated_Date').size()

# Visualizations
st.subheader("Visualizations:")
fig_temporal_analysis = plt.figure(figsize=(12, 6))
sales_by_date.plot(kind='line', color='green')
plt.title("Temporal Analysis of Sales")
plt.xlabel("Date")
plt.ylabel("Sales Count")
st.pyplot(fig_temporal_analysis)

# Task 7: Revenue Adjustment and Further Analysis
st.markdown("### Task 7: Revenue Adjustment and Further Analysis")
st.write("Revenue Adjustment: Adding $50 to Each Sale")

# Adding $50 to each sale
sales['Revenue'] += 50

st.write("Number of Orders in Canada or France:", sales[(sales['Country']=='Canada') | (sales['Country']=='France')].shape[0])
st.write("Number of Bike Racks orders in Canada:", sales[(sales['Country']=='Canada') & (sales['Sub_Category']=='Bike Racks')].shape[0])
st.write("Sales in Each Region of France:")
st.write(sales[sales['Country']=='France']['State'].value_counts())

# Visualizations
fig_region_france = plt.figure(figsize=(10, 6))
sns.barplot(x=sales[sales['Country']=='France']['State'].value_counts().index,
            y=sales[sales['Country']=='France']['State'].value_counts().values, color='orange')
plt.title("Number of Orders in Each Region of France")
plt.xlabel("Region")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig_region_france)

# Group by state and sum the revenue
state_revenue = sales.groupby('State')['Revenue'].sum().reset_index()

# Create a bar chart using Plotly Express
fig_state_revenue = px.bar(state_revenue, x='State', y='Revenue', title='Revenue by State')
fig_state_revenue.update_layout(xaxis_title='State', yaxis_title='Revenue')

# Display the chart using Streamlit
st.plotly_chart(fig_state_revenue)

# Display a final message
st.write("Made by Heba Mahfouz.")

