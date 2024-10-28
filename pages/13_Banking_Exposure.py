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
    <h1>Banking Exposure</h1>
</div>
"""
st.markdown(html_template, unsafe_allow_html=True)
#st.header('asd')
st.subheader("Start:")
#----------------------------Title--------------------------------------------------------------------

#st.write('# Income Statement')
st.write('Please fill in the form below to auto run by uploading latest loan database received in xlsx format below:')

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
sheet = "Loan Database"#form.text_input("Input Sheet Name ")

#age = form.slider("Age", min_value=18, max_value=100, step=1)
#date = form.date_input("Date", value=dt.date.today())

df1 = form.file_uploader(label= "Upload Latest Draf Loan Database:")

if df1:
  df1 = pd.read_excel(df1, sheet_name=sheet, header=1)
  #st.write(df1.head(1))

#df2 = form.file_uploader(label= "Upload Month End Rate:")
#if df2:
#  MRate = pd.read_excel(df2, sheet_name="Forex", header=2)

submitted = form.form_submit_button("Submit")
if submitted:
  #st.write("Submitted")
  #st.write(year, month)

  st.write(f"File submitted for : "+str(year)+"-"+str(month))
  #st.write(f"All file submitted for :{str(year)+str(month)}")
  
  
  #---------------------------------------------Start-------------------------------------------------------------
  
  df1.columns = df1.columns.str.replace("\n", "")
  #df1.columns = df1.columns.str.replace(" ", "")
  
  #st.write(df1)

  merge_MIA = df1.iloc[np.where((df1['EXIM Account No.']!="Total")&
                                ~(df1['EXIM Account No.'].isna()))][['CIF Number','EXIM Account No.','Finance(SAP) Number',"Customer Name",
                   'Nature of Account',
                   'Disbursement/Drawdown Status',
                   'Status',
                   'Cost/Principal Outstanding (Facility Currency)',
                   'Cost/Principal Outstanding (MYR)',
                   'Amount Approved / Facility Limit (Facility Currency)',
                   'Amount Approved / Facility Limit (MYR)']]

  def NOB(a_exp,b_exp,c_exp,d_exp,f_exp):
    if (a_exp=='Non Trade')&((b_exp=="No Further Disbursement")|(b_exp=="Fully Disbursed")):
        return d_exp
    elif (a_exp=='Non Trade')&((b_exp=="Ongoing Disbursement")|(b_exp=="Pending Disbursement")): 
        return f_exp
    elif ((a_exp=='Trade')|(a_exp=='Trade - Guarantee'))&((b_exp=="Ongoing Disbursement")|(b_exp=="Pending Disbursement")): 
        return f_exp
    elif c_exp == 'Impaired': 
        return d_exp
    else: 
        return 0
  merge_MIA['Total Banking Exposure (Facility Currency)'] = merge_MIA.apply(lambda x: NOB(x['Nature of Account'], x['Disbursement/Drawdown Status'], x['Status'], x['Cost/Principal Outstanding (Facility Currency)'],x['Amount Approved / Facility Limit (Facility Currency)']), axis=1)


  def NOB_MYR(a_exp_M,b_exp_M,c_exp_M,d_exp_M,f_exp_M):
    if (a_exp_M=='Non Trade')&((b_exp_M=="No Further Disbursement")|(b_exp_M=="Fully Disbursed")):
        return d_exp_M
    elif (a_exp_M=='Non Trade')&((b_exp_M=="Ongoing Disbursement")|(b_exp_M=="Pending Disbursement")): 
        return f_exp_M
    elif ((a_exp_M=='Trade')|(a_exp_M=='Trade - Guarantee'))&((b_exp_M=="Ongoing Disbursement")|(b_exp_M=="Pending Disbursement")): 
        return f_exp_M
    elif ((a_exp_M=='Trade')|(a_exp_M=='Trade - Guarantee'))&((b_exp_M=="No Further Disbursement")|(b_exp_M=="Fully Disbursed")): 
        return d_exp_M
    elif c_exp_M == 'Impaired': 
        return d_exp_M
    else: 
        return 0
  merge_MIA['Total Banking Exposure (MYR)'] = merge_MIA.apply(lambda x: NOB(x['Nature of Account'], x['Disbursement/Drawdown Status'], x['Status'], x['Cost/Principal Outstanding (MYR)'],x['Amount Approved / Facility Limit (MYR)']), axis=1)


  #---------------------------------------------Details-------------------------------------------------------------



  st.write(merge_MIA)

  st.write("Column checking: ")
  st.write(merge_MIA.shape)

  st.write("")
  st.write("Download file: ")
  #st.write("Download file: ")
  st.download_button("Download CSV",
                   merge_MIA.to_csv(index=False),
                   file_name='11. Banking Exposure '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')
  

  #st.write("Amount checking: ")
  #st.write(LDB2.fillna(0).groupby(['Status'])[['Cost/Principal Outstanding (MYR)']].sum().reset_index())
  
  #st.write("Account duplicate checking: ")
  #st.write(LDB2['EXIM Account No.'].value_counts())

  


