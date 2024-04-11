import streamlit as st
import pygwalker as pyg
import streamlit.components.v1 as components
import pandas as pd
from app import load_data

df = load_data()

# st.dataframe(df)


st.markdown(
        """
        <h1 style='text-align: center; '>Build your own Visualization from Scratch</h1>
        """,
        unsafe_allow_html=True)
 
# Generate the HTML using Pygwalker
pyg_html = pyg.to_html(df)
 
# Embed the HTML into the Streamlit app
components.html(pyg_html, height=1000, scrolling=True)