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
    <h1>BNM Supervision</h1>
</div>
"""
st.markdown(html_template, unsafe_allow_html=True)
#st.header('asd')
st.subheader("Reminder to copy data to template before start:")
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

####form = st.form("Basic form")
#name = form.text_input("Name")

#date_format = form.text_input("Input Date (i.e. 202409):")

#change form to st
year = st.slider("Year", min_value=2020, max_value=2030, step=1)
month = st.slider("Month", min_value=1, max_value=12, step=1)
#sheet = form.text_input("Input sheet Name ")
sheet = "Loan Database"

#age = form.slider("Age", min_value=18, max_value=100, step=1)
#date = form.date_input("Date", value=dt.date.today())

df1 = st.file_uploader(label= "Upload Latest Loan Database:")

if df1:
  df1 = pd.read_excel(df1, sheet_name=sheet, header=1)
  #st.write(df1.head(1))

  ####submitted = form.form_submit_button("Submit")
  ####if submitted:
  #st.write("Submitted")
  #st.write(year, month)

  st.write(f"File submitted for : "+str(year)+"-"+str(month))
  #st.write(f"All file submitted for :{str(year)+str(month)}")

  LDB1 = df1.iloc[np.where(~df1['CIF Number'].isna())]

  LDB1.columns = LDB1.columns.str.strip()
  LDB1.columns = LDB1.columns.str.replace("\n", "")

  #st.write(LDB1.head(3))
  LDB2 = LDB1[['CIF Number','EXIM Account No.',
                            'Company Group',
                            'Customer Name',
                            'Syndicated / Club Deal',
                            'Nature of Account',
                            'Facility',
                            'Type of Financing',
                            'Status',
                            'Amount Approved / Facility Limit (Facility Currency)',
                            'Amount Approved / Facility Limit (MYR)',
                            'Cost/Principal Outstanding (Facility Currency)',
                            'Cost/Principal Outstanding (MYR)',
                            'Contingent Liability Letter of Credit (Facility Currency)',
                            'Contingent Liability Letter of Credit (MYR)',
                            'Contingent Liability (Facility Currency)',
                            'Contingent Liability (MYR)',
                            'BNM Main Sector',
                            'BNM Sub Sector',
                            'Industry (Risk)',
                            'Industry Classification',
                            'Date Approved at Origination',
                            '1st Disbursement Date / 1st Drawdown Date',
                            '1st Payment/Repayment Date',
                            'Maturity/Expired Date',
                            'Grace Period (Month)',
                            'Tenure (Month)',
                            'Country Exposure',
                            'Country Rating',
                            #'Residency Status',
                            'CCPT Classification',
                            #'SME Commercial Corporate',
                            'Corporate Status']]
  
  #---------------------------------------------Details-------------------------------------------------------------
  


  
  LDB2["EXIM Account No."].fillna("Not Applicable Account", inplace=True)
  LDB2["EXIM Account No."] = LDB2["EXIM Account No."].astype(str)


  query = st.text_input("Filter dataframe in lowercase")

  if query:
    mask = LDB2.applymap(lambda x: query in str(x).lower()).any(axis=1)
    LDB2 = LDB2[mask]

  st.data_editor(
    LDB2,
    hide_index=True, 
    column_order=LDB2#("Customer Name","Status","Amount Approved / Facility Limit (MYR)")
  ) 

  #filter = st.selectbox('Select Status', options=LDB2["Status"].unique())
  #filtered_df = LDB2[LDB2["Status"]==filter]
  #st.dataframe(filtered_df)

  #st.write(LDB2)

  st.write("Column checking: ")
  st.write(LDB2.shape)

  st.write("Account duplication checking: ")
  st.write(LDB2["EXIM Account No."].value_counts())

  st.write("")
  st.write("Download file: ")
  #st.write("Download file: ")
  st.download_button("Download CSV",
                   LDB2.to_csv(index=False),
                   file_name='Loan Database as at '+str(year)+"-"+str(month)+' - BNM RAW.csv',
                   mime='text/csv')