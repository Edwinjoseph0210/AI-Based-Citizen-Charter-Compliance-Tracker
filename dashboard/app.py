import streamlit as st
import pandas as pd
import plotly.express as px
import requests

BACKEND_URL = 'http://localhost:8000/compliance/'

st.title('Citizen Charter Compliance Tracker')

@st.cache_data

def load_data():
    resp = requests.get(BACKEND_URL)
    data = resp.json()
    return pd.DataFrame(data)

df = load_data()

if df.empty:
    st.warning('No data available.')
else:
    st.subheader('Late Deliveries by Department')
    late_df = df[df['is_late'] == True]
    dept_late = late_df.groupby('department').size().reset_index(name='Late Deliveries')
    fig1 = px.bar(dept_late, x='department', y='Late Deliveries', title='Late Deliveries per Department')
    st.plotly_chart(fig1)

    st.subheader('Late Deliveries by Region')
    region_late = late_df.groupby('region').size().reset_index(name='Late Deliveries')
    fig2 = px.bar(region_late, x='region', y='Late Deliveries', title='Late Deliveries per Region')
    st.plotly_chart(fig2)

    st.subheader('Compliance Trend Over Time')
    df['request_date'] = pd.to_datetime(df['request_date'])
    trend = df.groupby(df['request_date'].dt.to_period('M')).apply(lambda x: (x['is_late'] == False).sum() / len(x)).reset_index(name='Compliance Rate')
    trend['request_date'] = trend['request_date'].astype(str)
    fig3 = px.line(trend, x='request_date', y='Compliance Rate', title='Compliance Rate Over Time')
    st.plotly_chart(fig3)

    st.subheader('Raw Data')
    st.dataframe(df)
