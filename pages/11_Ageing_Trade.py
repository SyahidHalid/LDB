import streamlit as st
import pandas as pd
import numpy as np
#import base64
#from PIL import Image
#import plotly.express as px

#warnings.filterwarnings('ignore')
#pd.set_option("display.max_columns", None) 
#pd.set_option("display.max_colwidth", 1000) #huruf dlm column
#pd.set_option("display.max_rows", 100)
#pd.set_option("display.precision", 2) #2 titik perpuluhan

#----------------------nama kat web atas yg newtab (png sahajer)--------------------
st.set_page_config(
  page_title = 'Syahid - Automation',
  page_icon = "EXIM.png",
  layout="wide"
  )

#to show code kat website

#with st.echo():
#  def sum(a, b):
#    return a + b

#----------------------header
html_template = """
<div style="display: flex; align-items: center;">
    <img src="https://www.exim.com.my/wp-content/uploads/2022/07/video-thumbnail-preferred-financier.png" alt="EXIM Logo" style="width: 200px; height: 72px; margin-right: 10px;">
    <h1>Trade Ageing</h1>
</div>
"""
st.markdown(html_template, unsafe_allow_html=True)
#st.header('asd')
st.subheader("Start:")
#----------------------------Title--------------------------------------------------------------------

#st.write('# Income Statement')
st.write('Please fill in the form below to auto run by uploading latest file received in xlsx format below:')

#----------------------------Input--------------------------------------------------------------------
#X = st.text_input("Input Date (i.e. 202409):")
#Y = st.text_input("Input Name (i.e. 09. Income statement Sep 2024):")

# klau nk user isi dlu bru boleh forward
#if not X:
#  st.warning("Enter Date!")
#  st.stop()
#st.success("Go ahead")

#if not Y:
#  st.warning("Enter Name!")
#  st.stop()
#st.success("Go ahead")

#----------------------------Form--------------------------------------------------------------------

form = st.form("Basic form")
#name = form.text_input("Name")
#date_format = form.text_input("Input Date (i.e. 202409):")

year = form.slider("Year", min_value=2020, max_value=2030, step=1)
month = form.slider("Month", min_value=1, max_value=12, step=1)

#age = form.slider("Age", min_value=18, max_value=100, step=1)
#date = form.date_input("Date", value=dt.date.today())

D1 = form.text_input("Input Ageing Sheet ")

df1 = form.file_uploader(label= "Upload Latest Trade - Ageing:")
if df1:
  T1 = pd.read_excel(df1, sheet_name=D1, header=5)


#df2 = form.file_uploader(label= "Upload Month End Rate:")
#if df2:
#  MRate = pd.read_excel(df2, sheet_name="Forex", header=2)
  #st.write(MRate.head(1))

#df3 = form.file_uploader(label= "Upload Loan Database:")
#if df3:
#  LDB_prev = pd.read_excel(df3, sheet_name="Loan Database", header=1)
  #st.write(LDB_prev.head(1))

submitted = form.form_submit_button("Submit")
if submitted:
  #st.write("Submitted")
  #st.write(year, month)

  st.write(f"File submitted for : "+str(year)+"-"+str(month))
  #st.write(f"All file submitted for :{str(year)+str(month)}")
  
  #---------------------------------Start
  T1_1 = T1.iloc[np.where((~T1['Account'].isna())&(~T1['Account'].isin(['Account','Number','NAME OF COMPANY'])))]

  T1_2 = T1_1[['Customer ',
               'Account',
               'NAME OF COMPANY',
               'OIC',
               'RM/ Head of Team',
               'CURRENCY',
               'INTEREST',
               'PRODUCT',
               'Unnamed: 14',
               'ACTUAL',
               'COMMITTED',
               'TOTAL',
               'AMOUNT',
               'DAYS',
               'Unnamed: 23',
               'SJPP',
               'Unnamed: 25',
               'DISBURSEMENT  FOR',
               'CUMULATIVE DISBURSEMENT',
               'PAYMENT FOR',
               '1ST UTILIZATION',
               'EXPIRY  DATE',
               'INTEREST ',
               'INTEREST.1',
               'Undrawn Amount']].rename(columns={'RM/ Head of Team':'RM',
                                                        'FACILITY ':'FACILITY LIMIT',
                                                        'Unnamed: 14':'STATUS',
                                                        'ACTUAL':'ACTUAL AMOUNT',
                                                        'COMMITTED':'COMMITTED AMOUNT',
                                                        'TOTAL':'TOTAL OUTSTANDING',
                                                        'AMOUNT':'AMOUNT OVERDUE',
                                                        'DAYS':'DAYS PAST DUE',
                                                        'Unnamed: 23':'SJPP BG COLLATERAL VALUE',
                                                        'SJPP':'SJPP EXPIRY DATE',
                                                        'Unnamed: 25':'SJPP CERT NO.',
                                                        'DISBURSEMENT  FOR':'DISBURSEMENT FOR THE MONTH',
                                                        'PAYMENT FOR':'PAYMENT FOR THE MONTH',
                                                        '1ST UTILIZATION':'1ST UTILIZATION DATE',
                                                        'INTEREST ':'INTEREST AMOUNT',
                                                        'INTEREST.1':'INTEREST OUTSTANDING',
                                                        'Undrawn Amount':'UNDRAWN AMOUNT'})
  
  T1_2.loc[~(T1_2['SJPP EXPIRY DATE'].isna()),"Guarantee"] = "SJPP"
  T1_2.loc[(T1_2['SJPP EXPIRY DATE'].isna()),"Guarantee"] = "Not Applicable"
  
  #st.write(T1_1['Account'].value_counts())


  
  #---------------------------------Download-------------------------------------------------------------

  st.write("")
  st.write("Row Column Checking: ")
  st.write(T1_2.shape)
  
  st.write("")
  st.write(T1_2)
  
  st.write("")
  st.write("Download file: ")
  st.download_button("Download CSV",
                   T1_2.to_csv(index=False),
                   file_name='09. Ageing Trade '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')