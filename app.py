# pip install pymssql==2.2.7

import os
import streamlit as st

def main():
    st.title("OpenAI Demo")
    st.subheader("Exploring Azure OpenAI and Azure SqlServer")
    st.info("This app using azure OpenAI to generate the sql query according to user question, and execute the query to get results from Azure SQL database.")

if __name__ == '__main__':
    main()
