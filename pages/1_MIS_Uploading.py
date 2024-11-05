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
    <h1>MIS Uploading</h1>
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
#sheet = form.text_input("Input sheet Name ")
sheet = "Loan Database"

#age = form.slider("Age", min_value=18, max_value=100, step=1)
#date = form.date_input("Date", value=dt.date.today())

df1 = form.file_uploader(label= "Upload Latest Loan Database:")

if df1:
  df1 = pd.read_excel(df1, sheet_name=sheet, header=1)
  #st.write(df1.head(1))

submitted = form.form_submit_button("Submit")
if submitted:
  #st.write("Submitted")
  #st.write(year, month)

  st.write(f"File submitted for : "+str(year)+"-"+str(month))
  #st.write(f"All file submitted for :{str(year)+str(month)}")

  LDB1 = df1.iloc[np.where(~df1['CIF Number'].isna())]

  LDB1.columns = LDB1.columns.str.strip()
  LDB1.columns = LDB1.columns.str.replace("\n", "")

  #st.write(LDB1.head(3))

  LDB1['LGD'] = ""

  LDB1['Expected Credit Loss (ECL) LAF (Facility Currency)'].fillna(0,inplace=True)
  LDB1['Expected Credit Loss LAF (ECL) (MYR)'].fillna(0,inplace=True)
  LDB1['Expected Credit Loss C&C (ECL) (Facility Currency)'].fillna(0,inplace=True)
  LDB1['Expected Credit Loss C&C (ECL) (MYR)'].fillna(0,inplace=True)
  LDB1['Expected Credit Loss (ECL) (Facility Currency)'] = LDB1["Expected Credit Loss (ECL) LAF (Facility Currency)"] + LDB1["Expected Credit Loss C&C (ECL) (Facility Currency)"]
  LDB1['Expected Credit Loss (ECL) (MYR)'] = LDB1["Expected Credit Loss LAF (ECL) (MYR)"] + LDB1["Expected Credit Loss C&C (ECL) (MYR)"]
  
  LDB2 = LDB1[['EXIM Account No.',
                            'CIF Number',
                            'Application System Code',
                            'CCRIS Master Account Number',
                            'CCRIS Sub Account Number',
                            'Facility Currency', #rename Currency
                            'Nature of Account',
                            '1st Disbursement Date / 1st Drawdown Date',
                            '1st Payment/Repayment Date',
                            'Status',
                            'Cancellation Date/Fully Settled Date',
                            'Write off Date',
                            'Partial Write off Date',
                            #'Ownership',
                            #'Officer in Charge',
                            'Relationship Manager (RM)',
                            'Team',
                            'Facility Agreement Date',
                            'Annual Review Date',
                            'Expiry of Availability Period',
                            'Maturity/Expired Date',
                            'Grace Period (Month)',
                            'Moratorium Period (Month)',
                            'Start Moratorium Date',
                            'Tenure (Month)',
                            'Payment/Repayment Frequency (Profit/Interest)',
                            'Payment/Repayment Frequency (Cost/Principal)',
                            'Effective cost of borrowings',
                            'Profit/Interest Margin',
                            'Effective Interest Rate (EIR)',
                            #'Average Profit/Interest Rate',
                            'Ta`widh Compensation/Penalty Rate',
                            'Cost/Principal Outstanding (Facility Currency)',
                            'Cost/Principal Outstanding (MYR)',
                            'Accrued Profit/Interest of the month (Facility Currency)',
                            'Accrued Profit/Interest of the month (MYR)',
                            'Cumulative Accrued Profit/Interest (Facility Currency)',
                            'Cumulative Accrued Profit/Interest (MYR)',                           
                            'Penalty/Ta`widh (Facility Currency)',
                            'Penalty/Ta`widh (MYR)',
                            'Income/Interest in Suspense (Facility Currency)',
                            'Income/Interest in Suspense (MYR)',
                            'Other Charges (Facility Currency)',
                            'Other Charges (MYR)',
                            'Contingent Liability Letter of Credit (Facility Currency)',
                            'Contingent Liability Letter of Credit (MYR)',
                            'Contingent Liability (Facility Currency)',
                            'Contingent Liability (MYR)',
             'Expected Credit Loss (ECL) (Facility Currency)',
             'Expected Credit Loss (ECL) (MYR)',
                            'Disbursement/Drawdown (Facility Currency)',
                            'Disbursement/Drawdown (MYR)',
                            'Cumulative Disbursement/Drawdown (Facility Currency)',
                            'Cumulative Disbursement/Drawdown (MYR)',
                            'Cost Payment/Principal Repayment (Facility Currency)',
                            'Cost Payment/Principal Repayment (MYR)',                            
                            'Cumulative Cost Payment/Principal Repayment (Facility Currency)',
                            'Cumulative Cost Payment/Principal Repayment (MYR)',
                            'Profit Payment/Interest Repayment (Facility Currency)',
                            'Profit Payment/Interest Repayment (MYR)',
                            'Cumulative Profit Payment/Interest Repayment (Facility Currency)',
                            'Cumulative Profit Payment/Interest Repayment (MYR)',
                            'Disbursement/Drawdown Status',
                            'Unutilised/Undrawn Amount (Facility Currency)',
                            'Unutilised/Undrawn Amount (MYR)',
                            'Overdue Amount (Facility Currency)',
                            'Overdue Amount (MYR)',
                            'Overdue (Days)',
                            'Month in Arrears',
                            'Date of Overdue',
                            'Risk Analyst',
                            'Internal Credit Rating (PD/PF)',
                            'CCPT Classification',
                            #'PD',
                            #'PF',
                            'LGD',
                            'MFRS9 Staging',
             'Date Classified as Watchlist',
                            'Watchlist Reason',
                            'Date Declassified from Watchlist',
                            'Reason for Impairment',
                            'Date Impaired',
                            'Industry (Risk)',
                            'Industry Classification',
                            'Amount Approved / Facility Limit (Facility Currency)','Position as At' ]]
  
  #---------------------------------------------Details-------------------------------------------------------------



  st.write(LDB2)

  st.write("Column checking: ")
  st.write(LDB2.shape)

  st.write("")
  st.write("Download file: ")
  #st.write("Download file: ")
  st.download_button("Download CSV",
                   LDB2.to_csv(index=False),
                   file_name='Loan Database as at '+str(year)+"-"+str(month)+' - MIS RAW.csv',
                   mime='text/csv')
  

  #st.write("Amount checking: ")
  #st.write(LDB2.fillna(0).groupby(['Status'])[['Cost/Principal Outstanding (MYR)']].sum().reset_index())
  
  #st.write("Account duplicate checking: ")
  #st.write(LDB2['EXIM Account No.'].value_counts())

  


