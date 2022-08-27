import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title='Survey Results')
st.header('Survey Results - 2022')

### --- LOAD DATABASE

excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(
    excel_file,
    sheet_name=sheet_name,
    usecols='B:D',
    header=3
)

df_participants = pd.read_excel(
    excel_file,
    sheet_name=sheet_name,
    usecols='F:G',
    header=3
)
df_participants.dropna(
    how='any',
     inplace=True
)
department_options = df['Department'].unique().tolist()
age_options = df['Age'].unique().tolist()

age_selection = st.slider(
    'Age:',
    min_value= min(age_options),
    max_value = max(age_options),
    value=(min(age_options),max(age_options))

)

department_selection = st.multiselect(
    'Department:',
    default=department_options,
    options=department_options
)

mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
df_number = df[mask].shape[0]
df_filter = df[mask]

st.markdown(f'*Available Results: {df_number}*')

df_grouped = df_filter.groupby(['Rating']).count()[['Age']]
df_grouped.rename(columns={'Age':'Votes'}, inplace=True)
df_grouped.reset_index(inplace=True)

bar_chart = px.bar(
    df_grouped,
    x='Rating',
    y='Votes',
    text='Votes',
    color_discrete_sequence= (['#F63366']*len(df_grouped)),
    template='plotly_white'
)

st.plotly_chart(bar_chart)


col1, col2 = st.columns(2)
col1.image('images/survey-icon-12.png')
col2.dataframe(df_filter)


pie_chart = px.pie(
    df_participants,
    title='Total No. of Participants',
    values = 'Participants',
    names='Departments'
)


st.plotly_chart(pie_chart)