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
  page_title = 'Loan Database - Automation',
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
    <h1>Trade ECL Template</h1>
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

#D1 = form.text_input("Input Islamic Cost Sheet ")

df1 = form.file_uploader(label= "Upload Latest Trade - ECL Template:")
if df1:
  T1 = pd.read_excel(df1, sheet_name="Summary", header=6)

df2 = form.file_uploader(label= "Upload Month End Rate:")
if df2:
  MRate = pd.read_excel(df2, sheet_name="Forex", header=2)
  #st.write(MRate.head(1))

df3 = form.file_uploader(label= "Upload Loan Database:")
if df3:
  LDB_prev = pd.read_excel(df3, sheet_name="Loan Database", header=1)
  #st.write(LDB_prev.head(1))

submitted = form.form_submit_button("Submit")
if submitted:
  #st.write("Submitted")
  #st.write(year, month)

  st.write(f"File submitted for : "+str(year)+"-"+str(month))
  #st.write(f"All file submitted for :{str(year)+str(month)}")
  
  #---------------------------------Start

  T1.columns = T1.columns.str.strip()
  T1['Account No'] = T1['Account No'].astype(str)

  LDB_prev.columns = LDB_prev.columns.str.strip()
  LDB_prev = LDB_prev.iloc[np.where(LDB_prev['EXIM Account No.']!="Total")]
  LDB_prev['Finance(SAP) Number'] = LDB_prev['Finance(SAP) Number'].astype(str)

  T2 = T1.iloc[np.where(~T1.Currency.isna())][['Account No',
                                               'Borrower name',
                                               'Undrawn amount (base currency)',
                                               'Profit Rate/ EIR',
                                               'Currency',
                                               'First Released Date',
                                               'Maturity date',
                                               'Availability period',
                                               'DPD',
                                               'Principal payment frequency',
                                               'Interest payment frequency']].rename(columns={'Account No':'Finance(SAP) Number'})

  merge = T2.merge(LDB_prev[['CIF Number',
                             'EXIM Account No.',
                             'Finance(SAP) Number',
                             'Currency']].rename(columns={'Currency':'Currency LDB'}), on='Finance(SAP) Number', how='left')

  merge1 = merge.merge(MRate[['Month','Curr']].rename(columns={'Month':'Currency'}), on='Currency', how='left')

  merge1['Unutilised/ Undrawn Amount (MYR)'] = merge1['Undrawn amount (base currency)']*merge1['Curr']
  merge1['Profit Rate/ EIR'] = merge1['Profit Rate/ EIR']*100

  merge1 = merge1.rename(columns={'Undrawn amount (base currency)':'Unutilised/ Undrawn Amount (Facility Currency)',
                               'Profit Rate/ EIR':'Average Profit/Interest Rate'})

  merge1 = merge1.fillna(0)[['CIF Number',
                   'EXIM Account No.',
                   'Finance(SAP) Number',
                   #'Borrower name',
                   'Currency', 
                   'Currency LDB', 
                   'Curr',
                   'Unutilised/ Undrawn Amount (Facility Currency)',
                   'Unutilised/ Undrawn Amount (MYR)',
                   'Average Profit/Interest Rate',
                   'First Released Date',
                   'Maturity date',
                   'Availability period',
                   'DPD',
                   'Principal payment frequency',
                   'Interest payment frequency']]
  
  #---------------------------------Download-------------------------------------------------------------

  st.write("")
  st.write("Row Column Checking: ")
  st.write(merge1.shape)
  
  st.write("")
  #st.write('Sum Total Loans Outstanding (MYR) : RM'+str(sum))
  st.write(f"Sum Undrawn (FC) : ${float(sum(merge1['Unutilised/ Undrawn Amount (Facility Currency)']))}")
  st.write(f"Sum Undrawn (MYR) : RM{float(sum(merge1['Unutilised/ Undrawn Amount (MYR)']))}")
  st.write(f"Sum DPD : {float(sum(merge1['DPD']))}")
            
  #st.write("SAP Duplication Checking: ")
  #st.write(appendfinal3['Finance(SAP) Number'].value_counts())
  st.write("")
  st.write(merge1)
  
  st.write("")
  st.write("Download file: ")
  st.download_button("Download CSV",
                   merge1.to_csv(index=False),
                   file_name='07. Trade - ECL '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')