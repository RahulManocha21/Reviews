import streamlit as st  # Importing the Streamlit library to create a web app 
import pandas as pd  # Importing the Pandas library to handle data manipulation and analysis
import numpy as np  # Importing the Numpy library for numerical computations
from datetime import date  # Importing the date class from the datetime module for date manipulation
from matplotlib import pyplot as plt
# Load the CSV file
# Define a function to load the data
def extract_category(row):
    row = row.replace("-Catalog", "").strip()
    row = row.replace("-E-Collections", "").strip()
    row = row.replace("-Solo", "").strip()
    row = row.replace("- CATALOG", "").strip()
    row = row.replace("-CATALOG", "").strip()
    row = row.replace("- OTHER", "").strip()
    return row

@st.cache_data  # Decorator to cache data for faster loading
def load_data():
    df = pd.read_csv('Reviews.csv')  # Load the CSV file named 'Reviews.csv'
    df = df.drop(columns=[  # Drop unnecessary columns from the DataFrame
        'Date',
        'Review Bottomline',
        'Review Location',
        'Review Location',
        'Locale',
        'Site Status',
        'Is PWR Publishable',
        'Page ID Variant',
        'PGC',
        'Reviewer Type',
        'Review Nickname',
        'UGC ID'
    ])
    df['Created Date'] = pd.to_datetime(df['Created Date']).dt.date  # Convert the 'Created Date' column to a datetime format
    df['Category'] = df['PGC_Desc'].apply(extract_category)
    return df


if __name__ == "__main__":  # Main execution block
    st.set_page_config(  # Set the layout of the web app to wide
                        layout="wide",
                        page_title='Review System App',
                        page_icon='⭐')
    
    st.markdown(
        """
        <h1 style='text-align: center; '>Reviews Analysing System</h1>
        """,
        unsafe_allow_html=True)
    df = load_data()  # Load the data
    # st.subheader('Actual DataFrame')
    # st.dataframe(df,column_order=['PGC_Desc','Category'], hide_index=True)
    # Sidebar filters
    st.markdown("""<h3 style='text-align: center;'>Filters</h3>""", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        start_date = st.date_input("Start date", value= df['Created Date'].min() , min_value=df['Created Date'].min(), max_value=date.today())
    with col2:
        end_date = st.date_input("End date",value=df['Created Date'].max(),min_value=df['Created Date'].min(), max_value=df['Created Date'].max())
        filtered_df = df[(df['Created Date'] >= start_date) &  (df['Created Date'] <= end_date)]
        available_products = filtered_df['Product Name'].unique()
        available_pgc = filtered_df['Category'].unique()
        available_rating = filtered_df['Review Rating'].unique()
    with col3:            
        selected_brands = st.multiselect("Brand", filtered_df['Brand Name'].unique())
        if selected_brands:
            filtered_df = filtered_df[filtered_df['Brand Name'].isin(selected_brands)]
            available_pgc = filtered_df['Category'].unique()
            available_products = filtered_df['Product Name'].unique()
            available_ratings = filtered_df['Review Rating'].unique()
    with col4:
        selected_pgc_descriptions = st.multiselect("PGC Category", available_pgc)
        if selected_pgc_descriptions:
            filtered_df = filtered_df[filtered_df['Category'].isin(selected_pgc_descriptions)]
            available_products = filtered_df['Product Name'].unique()
            available_ratings = filtered_df['Review Rating'].unique()
    with col5:
        selected_products = st.multiselect("Product Name", available_products)
        if selected_products:
            filtered_df = filtered_df[filtered_df['Product Name'].isin(selected_products)]
            available_ratings = filtered_df['Review Rating'].unique()
    with col6:
        selected_ratings = st.multiselect("Ratings", available_rating)
        if selected_ratings:
            filtered_df = filtered_df[filtered_df['Review Rating'].isin(selected_ratings)]

    st.markdown("***")

    #############################Metrics Calculations starts############################################################################
    st.subheader("Have a look on Major Metrics")
    one_star_count = filtered_df[(filtered_df['Review Rating'] == 1)].shape[0]
    five_star_count = filtered_df[(filtered_df['Review Rating'] == 5)].shape[0]
    # five_star_count = 1000
    threshold_count_1star = filtered_df.shape[0] * 0.05
    threshold_count_5star = filtered_df.shape[0] * 0.60
    one_star_delta = np.round((one_star_count - threshold_count_1star),decimals=2)
    five_star_delta = np.round((five_star_count - threshold_count_5star),decimals=2)
    metric0, metric1, metric2,metric3,metric4 = st.columns([0.4,1,1,1,1])
    metric1.metric("Total number of reviews", len(filtered_df))
    metric2.metric("Average Rating", np.round(filtered_df['Review Rating'].mean(),decimals=2))
    metric3.metric("5-star reviews",
                   five_star_count,
                   five_star_delta,
                   )
    metric4.metric("1-star reviews",
                   one_star_count,
                   one_star_delta,
                   delta_color="inverse"
                   )
    st.markdown("***")

    #############################Metrics Calculations ends############################################################################
    
    data, graph = st.columns(2)
    # data, graph = st.tabs(['DataFrame','Graphs'])
    with data:
        filtered_df['Created Date'] = pd.to_datetime(filtered_df['Created Date'])
        filtered_df['Created Year'] = filtered_df['Created Date'].dt.year
        avg_rating_df = filtered_df.groupby(['Brand Name', 'Category',  'Created Year'])['Review Rating'].mean().reset_index()
        avg_rating_df['Review Rating'] = np.round(avg_rating_df['Review Rating'], 2)
        avg_rating_df = avg_rating_df.sort_values(by='Created Year', ascending=False)
        pro_avg_rating_df = filtered_df.groupby(['Brand Name', 'Product Name', 'Created Year'])['Review Rating'].mean().reset_index()
        pro_avg_rating_df['Review Rating'] = np.round(pro_avg_rating_df['Review Rating'], 2)
        pro_avg_rating_df = pro_avg_rating_df.sort_values(by='Created Year', ascending=False)
        st.subheader('Average Rating by PGC Desc and Year')
        st.dataframe(avg_rating_df, hide_index=True,height=350, width=1500)
        st.markdown("***")
        st.subheader('Average Rating by Product and Year')    
        st.dataframe(pro_avg_rating_df,hide_index=True, height=350, width=1500)


        
    with graph:
        st.subheader('Visualization')
        st.bar_chart(avg_rating_df, x= "Created Year", y ="Review Rating",color='Category' )
        st.markdown("***")
        st.subheader('Visualization')    
        st.bar_chart(pro_avg_rating_df,x='Created Year', y='Review Rating', color='Product Name')
    
        
    st.markdown("***")

    st.subheader('Read Reviews')
    st.dataframe(filtered_df[['Brand Name','SKU','Product Name','Review Rating','Review Headline','Review Comments']],
                 width=1500, hide_index=True)
    