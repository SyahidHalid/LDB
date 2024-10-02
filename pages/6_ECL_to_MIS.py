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
    <h1>ECL Submission to MIS</h1>
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

D1 = form.text_input("Input LAF Sheet ")
D2 = form.text_input("Input C&C Sheet ")


df1 = form.file_uploader(label= "Upload Latest ECL Submission to MIS:")

if df1:
  LAF = pd.read_excel(df1, sheet_name=D1, header=2)
  CnC = pd.read_excel(df1, sheet_name=D2, header=2)

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

  LAF.columns = LAF.columns.str.replace("\n", "_")
  LAF.columns = LAF.columns.str.replace(" ", "_")
  LAF.columns = LAF.columns.str.replace(".", "_")

  CnC.columns = CnC.columns.str.replace("\n", "_")
  CnC.columns = CnC.columns.str.replace(" ", "_")
  CnC.columns = CnC.columns.str.replace(".", "_")

  LAF1 = LAF.iloc[np.where(~(LAF.Account_No.isna()))]

  LAF1['LAF_ECL_MYR'] = LAF1['Stage_1_Conventional'] + LAF1['Stage_2_Conventional'] + LAF1['Stage_1_Islamic'] + LAF1['Stage_2_Islamic']

  LAF1['Account_No'] = LAF1['Account_No'].astype(str)

  LAF1 = LAF1.fillna(0).groupby(['Account_No','Borrower_name','Category','Unnamed:_5'])[['LAF_ECL_MYR']].sum().reset_index()

  LAF1['Unnamed:_5'] = LAF1['Unnamed:_5'].astype(str)
  #LAF1['Unnamed:_5'] = LAF1['Unnamed:_5'].str.strip()

  LAF1.rename(columns={'Account_No':'Account_No'},inplace=True)
  LAF1['Account_No'] = LAF1['Account_No'].astype(str)

  LDB_prev['Finance(SAP) Number'] = LDB_prev['Finance(SAP) Number'].astype(str)

  LDB_prev.columns = LDB_prev.columns.str.replace("\n", "")

  #LDB
  LAF1_1 = LAF1.merge(LDB_prev[['Finance(SAP) Number','Currency','Status']].drop_duplicates('Finance(SAP) Number',keep='first').rename(columns={'Finance(SAP) Number':'Account_No'}),on=['Account_No'],how='left', suffixes=('_x', '')) #,indicator=True


  #LAF1_1['Currency'] = LAF1_1['Currency'].str.strip()
  LAF1_1['Currency'] = LAF1_1['Currency'].astype(str)
  #MRate['Month'] = MRate['Month'].str.strip()
  MRate['Month'] = MRate['Month'].astype(str)

  #Rate
  LAF2 = LAF1_1.rename(columns={'Currency':'Month'}).merge(MRate[['Month','Curr']], on='Month', how='left')

  LAF2['LAF_ECL_FC'] = LAF2['LAF_ECL_MYR']/LAF2['Curr']

  CnC['Account_No'] = CnC['Account_No'].astype(str)

  CnC1 = CnC.iloc[np.where(~(CnC.Account_No.isna()))]

  CnC1['CnC_ECL_MYR'] = CnC1['Stage_1_Conventional'] + CnC1['Stage_2_Conventional'] + CnC1['Stage_1_Islamic'] + CnC1['Stage_2_Islamic']

  CnC1 = CnC1.fillna(0).groupby(['Account_No','Borrower_name','Category','Unnamed:_5'])[['CnC_ECL_MYR']].sum().reset_index()

  #CnC1['Account_No'] = CnC1['Account_No'].str.strip()


  #LDB
  CnC1_1 = CnC1.merge(LDB_prev[['Finance(SAP) Number','Currency','Status']].drop_duplicates('Finance(SAP) Number',keep='first').rename(columns={'Finance(SAP) Number':'Account_No'}),on=['Account_No'],how='left', suffixes=('_x', '')) #,indicator=True

  #MRate['Month'] = MRate['Month'].str.strip()
  MRate['Month'] = MRate['Month'].astype(str)

  #Rate
  CnC2 = CnC1_1.rename(columns={'Currency':'Month'}).merge(MRate[['Month','Curr']], on='Month', how='left')

  CnC2['CnC_ECL_FC'] = CnC2['CnC_ECL_MYR']/CnC2['Curr']

  merge = pd.concat([LAF2,CnC2])

  merge.fillna(0, inplace=True)

  #merge.Borrower_name = merge.Borrower_name.str.strip()
  merge.Borrower_name = merge.Borrower_name.str.upper()
  
  #st.write(CnC)

  merge1 = merge.iloc[np.where(merge['Account_No']!="nan")].fillna(0).groupby(['Account_No','Borrower_name','Category','Month'])[['LAF_ECL_FC',
                                                            'LAF_ECL_MYR',
                                                            'CnC_ECL_FC',
                                                            'CnC_ECL_MYR']].sum().reset_index()
  
  #


  #---------------------------------------------Download-------------------------------------------------------------

  #st.write('Sum Total Loans Outstanding (MYR) : RM'+str(sum))
  st.write("")
  st.write(f"Sum ECL LAF (FC) : ${float(sum(merge1['LAF_ECL_FC']))}")
  st.write(f"Sum ECL LAF (MYR) : RM{float(sum(merge1['LAF_ECL_MYR']))}")

  st.write("")
  st.write(f"Sum ECL C&C (FC) : ${float(sum(merge1['CnC_ECL_FC']))}")
  st.write(f"Sum ECL C&C (MYR) : RM{float(sum(merge1['CnC_ECL_MYR']))}")

  st.write("")
  st.write("Row Column Checking: ")
  st.write(merge1.shape)

  st.write(merge1)
           
  #st.write("SAP Duplication Checking: ")
  #st.write(appendfinal3['Account'].value_counts())

  st.write("Download file: ")
  st.download_button("Download CSV",
                   merge1.to_csv(index=False),
                   file_name='04. ECL to MIS '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')