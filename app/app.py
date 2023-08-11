# pip install pymssql==2.2.7

import os
import streamlit as st
import openai
import re
import pymssql
import pandas as pd

def generate_sql_text(prompt):
    openai.api_type = "azure"
    openai.api_base = "https://qingshanopenaitest.openai.azure.com/"
    openai.api_version = "2022-12-01"
    openai.api_key = "dfd3034b1b7d4806b0dde842b353d6b7"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.8,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        best_of=1,
        stop=None)

    # print(response)

    sqltext = response.choices[0].text
    try:
        sqltext = sqltext.split(';')[0]
        sqltext = sqltext.replace('\n', ' ')

        if 'select' not in sqltext.lower() or 'CERData_20230328' not in sqltext:
            sqltext = ''
    except:
        sqltext = ''

    return sqltext

def execute_sql_query(sqltext):
    conn = pymssql.connect('qingshandataserver.database.windows.net', 'CERAdmin', '!!abc123', 'qingshandatabase')
    cursor = conn.cursor(as_dict=True)

    cursor.execute(sqltext)

    columns = []
    data = []
    for row in cursor:
        if not columns:
            for key in row.keys():
                columns.append(key)

        if columns:
            rowdata = []
            for column in columns:
                rowdata.append(row[column]) 

            data.append(rowdata)

    conn.close()

    df = pd.DataFrame(data, columns = columns)
    return df

def generate_prompt(user_input):
    prompt = '''
                You are an assistant to create query for user. If you don't know how to create the query, just return the query without any condition.
                Table CERData_20230328, columns = [Device, Posting_Date, Season, Manufacturer, Model, Marketing_Collection, ArcheType, Chipset, Processor, RAM_GB, Storage_Size_GB, Display, Graphics, Battery_Life, Fast_Startup]
                Please create a standard query for Microsoft sqlserver. Do use top expression and do not put top to the end of the query.
                Columns Device, Season, Manufacturer and Processor must be selected, and column associated with the user question also should be selected.
            '''
    prompt += user_input + "\n\n"

    return prompt

def main():
    st.title("OpenAI Demo")
    st.subheader("Exploring Azure OpenAI and Azure SqlServer")
    st.info("This app using azure OpenAI to generate the sql query according to user question, and execute the query to get results from Azure SQL database.")
    
    question = st.selectbox(':blue[Select a question:]',
                        ('---Input your own question or select one---',
                         'I want to know the top 10 devices having the longest Battery_Life.',
                         'List the devices with loweast fast startup time, fast startup should not be null.',
                         'Give five devices release by Lenovo manufacture.',
                         'Please find 5 devices with more than 32GB RAM.'),
                         placeholder='Select ...')

    if question == '---Input your own question or select one---':
        question = st.text_input(':blue[Or your question:]', placeholder='Please input your question here.')

    st.divider()

    sqltext = ''
    if question and question != '---Input your own question or select one---':
        prompt = generate_prompt(question)
        sqltext = generate_sql_text(prompt)
        st.write(sqltext)

        st.divider()
        st.table(execute_sql_query(sqltext))

if __name__ == '__main__':
    main()
    main()
