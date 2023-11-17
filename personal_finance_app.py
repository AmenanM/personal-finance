import streamlit as st
import pandas as pd
import plotly
import plotly.express as px
from streamlit_elements import elements, mui, html
import numpy as np
from streamlit_extras.stylable_container import stylable_container 
from datetime import datetime


# Initial page config

st.set_page_config(
     page_title='personal finance ',
     layout="wide",
     initial_sidebar_state="expanded",
)
# read datasets
budget=pd.read_csv('Budget.csv')
transactions=pd.read_csv('personal_transactions.csv')

# turn date column to datetime d=format
transactions['Dates'] = pd.to_datetime(transactions['Date'], format='%m/%d/%Y') 
#display month year only
# transactions['Dates_month'] = pd.to_datetime(transactions['Dates']).dt.to_period('m')
transactions['Dates'] = transactions['Dates'].apply(lambda x: datetime.strftime(x, format="%b-%Y"))

with st.sidebar:
    st.write('')


#Header
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True) #reduce white space on top of page
st.markdown("<h1 style='text-align: left;'>Personal finance management</h1>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: left;'>An individual's personal budget and their list of transactions. Analysis of these data in detail.</h1>", unsafe_allow_html=True)
st.write('')
st.markdown("<h6 style='text-align: left;'>Budget overview</h6>", unsafe_allow_html=True)
st.write('')



col1,col2,col3,col4=st.columns([2,0.5,4,4])
with col1:
    st.dataframe(budget,width=400,height=400)

with col3:
    # st.write('**Visualization**')
    #historgram to visualize the budget categories
    budget_order=budget.sort_values(by=['Budget'], ascending=False)
    budget_order=budget_order.head(10)
    hist_categories=px.bar(budget_order,x='Category', y = 'Budget', labels={'Budget': 'Amount'}, title="Top ten budget categories")
    hist_categories.update_traces(marker_color = 'grey', marker_line_color = 'black',
                  marker_line_width = 2, opacity = 1)
    st.plotly_chart(hist_categories,use_container_width=True)
with col4:
    st.write('')
    #categorizing categories in imperative, leisure,selfcare
    dict_category={'Alcohol & Bars': 'Leisure','Auto Insurance' : 'Imperative', 'Coffee Shops': 'Leisure',
                    'Electronics & Software': 'Leisure', 'Entertainment': 'Leisure', 'Fast Food': 'Leisure',
                    'Gas & Fuel': 'Imperative', 'Groceries': 'Imperative','Haircut': 'Self-Care','Home Improvement':'Imperative' ,
                    'Internet': 'Imperative','Mobile Phone': 'Imperative','Mortgage & Rent': 'Imperative',
                    'Movies & DVDs':'Leisure' ,'Music': 'Leisure','Restaurants': 'Leisure','Shopping':'Self-Care' ,'Television':'Imperative','Utilities':'Imperative'}

    budget['Broader_category']=budget['Category'].apply(lambda x : dict_category[x])
    budget_broader=budget.groupby(['Broader_category']).sum().reset_index()
    # pie_chart with broader category
    budget_pie = px.pie(budget_broader, values='Budget', names='Broader_category', title='Budget in broader categories',
                        color_discrete_sequence=px.colors.sequential.Jet)
    budget_pie.update_layout(legend=dict(
        yanchor="top",
        y=1.1,
        xanchor="right",
        x=0.2,
        font=dict(size= 16)
    ),)
    
    st.plotly_chart(budget_pie)


#transactions month by month by category
st.subheader('Transactions month by month by category')
st.markdown("<h6 style='text-align: left;'>The transactions are listed over a year from january 2018 until September 2019</h6>", unsafe_allow_html=True)


select_date=st.selectbox('',list(np.unique(transactions.Dates)))

df_select=transactions[transactions['Dates']==select_date]
df_select=df_select[df_select['Transaction Type']!='credit'].reset_index()


#plotly by date selected
def category_budget(x):
    try:
        value_dict=dict_of_budget[x]
    except:
        value_dict=np.nan
    return value_dict

# def respected(x1,x2):
#     try:
#         if x1<x2:
#             respected_value="respected"
#         if x1>x2:
#             respected_value='not respected'
#     except:
#         respected_value='no budget'
#     return respected_value
#we check if the expenses respect the budget every month
dict_of_budget=dict(zip(budget.Category,budget.Budget))
df_select['budget']=df_select['Category'].apply(lambda x : category_budget(x))
# df_select['budget']=df_select['budget'].apply(lambda x : 'no budget' if x=='' else x)
# st.write(np.isnan(df_select.budget[5]))
# st.write(respected(df_select.Amount[5],df_select.budget[5]))
# # df_select['respected?']=df_select[['Amount', 'budget']].apply(lambda x : 'respected' if x.Amount<x.budget else 'not respected', axis=1)
# df_select['respected?']=df_select[['Amount', 'budget']].apply(lambda x : respected(x.Amount,x.budget), axis=1)
df_select['respected??']=df_select['Amount']-df_select['budget']
df_select['respected?']=df_select['respected??'].apply(lambda x : 'respected' if x<0 else 'not respected' if x>0 else 'no budget' if np.isnan(x) else 'respected' if x==0 else x)
hist_select=px.bar(df_select,x='Category', y = 'Amount', color='respected?')
col1,col2,col3,col4,col5=st.columns([6,0.5,1.5,0.5,2])
with col1:
    st.plotly_chart(hist_select,use_container_width=True)
with col3:
    st.write('')
    st.write('')
    st.write('')
    top_category=df_select[df_select.Amount == df_select.Amount.max()]
    top_category=top_category['Category'].values[0]
    st.markdown("<h5 style='text-align: left;'>Top expense</h1>", unsafe_allow_html=True)
    with stylable_container(
        key="container_with_border",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 2px)
            }
            """,
    ):
        st.markdown(f"""{top_category}""", unsafe_allow_html=True)
with col5:
    st.write('')
    st.write('')
    st.write('')
    st.markdown("<h5 style='text-align: left;'>Total credit/Total debit</h1>", unsafe_allow_html=True)
    total_expenses=df_select['Amount'].sum()
    df_select_credit=transactions[transactions['Dates']==select_date]
    df_select_credit=df_select_credit[df_select_credit['Transaction Type']=='credit']
    total_credit=df_select_credit['Amount'].sum()

    summary_df=pd.DataFrame()
    summary_df['Total credit']=pd.Series(total_credit)
    summary_df['Total debit']=pd.Series(total_expenses)
    summary_df['remaining']=summary_df['Total credit']-summary_df['Total debit']
    
    def color_negative_red(val):
        color = 'red' if val < 0 else 'black'
        return 'color: %s' % color
    # summary_df=summary_df.to_string(index=False)
    summary_df=summary_df.style.applymap(color_negative_red).format(precision=0)
    summary_df

#transactions month by month by category
st.write('---')
col1,col2,col3=st.columns([2,0.5,2])
with col1:
    st.subheader('Credit on the whole period')
    # st.write(transactions.groupby('Dates_month').sum())
    transactions_credit=transactions[transactions['Transaction Type']=='credit']
    transactions_credit=transactions_credit.groupby(['Dates']).sum().reset_index()
    # transactions_group
    transaction_credit_fig=px.bar(transactions_credit, x='Dates', y='Amount')
    # transaction_all.update_traces(width=100)
    transaction_credit_fig.update_traces(marker_color='#487a51', showlegend=False)

    st.plotly_chart(transaction_credit_fig)
with col3:
    st.subheader('Expenses on the whole period')
    # st.write(transactions.groupby('Dates_month').sum())
    transactions_debit=transactions[transactions['Transaction Type']!='credit']
    transactions_debit=transactions_debit.groupby(['Dates']).sum().reset_index()
    # transactions_group
    transactions_debit_fig=px.line(transactions_debit, x='Dates', y='Amount')
    transactions_debit_fig.update_traces(line_color='#9e4924', showlegend=False)
    st.plotly_chart(transactions_debit_fig)


