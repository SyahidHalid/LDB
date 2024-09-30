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
    <h1>Debtor Listing</h1>
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

D1 = form.text_input("Input BG Sheet ")
D2 = form.text_input("Input LC Sheet ")


df1 = form.file_uploader(label= "Upload Latest Contigent Liability:")

if df1:
  BG1 = pd.read_excel(df1, sheet_name=D1, header=2)
  LC1 = pd.read_excel(df1, sheet_name=D2, header=1)



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
  
  #---------------------------------------------Start

  BG1['C/I'] = BG1['C/I'].str.strip()
  BG2 = BG1.iloc[np.where(BG1['C/I'].isin(['C','I']))]

  #BG2['Exposure (RM)'] = BG2['Exposure (RM)'].str.strip()
  #BG2.loc[BG2['Exposure (RM)']=='-', 'Exposure (RM)'] == 0
  BG2['Exposure (RM)'] = BG2['Exposure (RM)'].astype(float)

  #BG2['Facility Limit Undrawn (FC)'] = BG2['Facility Limit Undrawn (FC)'].str.strip()
  #BG2.loc[(BG2['Facility Limit Undrawn (FC)']=='-'),'Facility Limit Undrawn (FC)'] = 0
  #BG2.loc[BG2['Facility Limit Undrawn (FC)']=='REFER TO ABOVE', 'Facility Limit Undrawn (FC)'] = 0
  BG2['Facility Limit Undrawn (FC)'] = BG2['Facility Limit Undrawn (FC)'].astype(float)

  #BG2['Facility Limit Undrawn (FC)'] = BG2['Facility Limit Undrawn (FC)'].str.strip()
  #BG2.loc[BG2['Facility Limit Undrawn (MYR)']=='-', 'Facility Limit Undrawn (MYR)'] = 0
  #BG2.loc[BG2['Facility Limit Undrawn (MYR)']=='REFER TO ABOVE', 'Facility Limit Undrawn (MYR)'] = 0
  BG2['Facility Limit Undrawn (MYR)'] = BG2['Facility Limit Undrawn (MYR)'].astype(float)
  
  BG2.Borrower = BG2.Borrower.str.upper()

  BG2.loc[(BG2.Borrower.str.contains('BOUSTEAD')),'CIF Number'] = 'EXIM000491'
  BG2.loc[(BG2.Borrower.str.contains('PERTAMA')),'CIF Number'] = 'EXIM000140'
  BG2.loc[(BG2.Borrower.str.contains('OM MATERIAL')),'CIF Number'] = 'EXIM000145'
  BG2.loc[(BG2.Borrower.str.contains('SMH RAIL')),'CIF Number'] = 'EXIM000210'
  BG2.loc[(BG2.Borrower.str.contains('DESTINI')),'CIF Number'] = 'EXIM000169'
  BG2.loc[(BG2.Borrower.str.contains('ASIA CARGO')),'CIF Number'] = 'EXIM000277'
  BG2.loc[(BG2.Borrower.str.contains('PRINSIPTEK')),'CIF Number'] = 'EXIM000110'
  BG2.loc[(BG2.Borrower.str.contains('URBAN PINNACLE')),'CIF Number'] = 'EXIM000563'
  BG2.loc[(BG2.Borrower.str.contains('PETROLIAM NASIONAL')),'CIF Number'] = 'EXIM000432'
  BG2.loc[(BG2.Borrower.str.contains('HELMS GEOMARINE')),'CIF Number'] = 'EXIM000282'

  BG2.loc[(BG2.Borrower.str.contains('BOUSTEAD')),'EXIM Account No.'] = '3308-02137-119-0330-00'
  BG2.loc[(BG2.Borrower.str.contains('PERTAMA')),'EXIM Account No.'] = '3308-01137-216-0133-00'
  BG2.loc[(BG2.Borrower.str.contains('OM MATERIAL'))&(BG2.Currency=="MYR"),'EXIM Account No.'] = '3308-01137-216-0058-00'
  BG2.loc[(BG2.Borrower.str.contains('OM MATERIAL'))&(BG2.Currency=="USD"),'EXIM Account No.'] = '3308-02137-211-0088-00'
  BG2.loc[(BG2.Borrower.str.contains('SMH RAIL')),'EXIM Account No.'] = '3308-02137-216-0046-00' #&(BG2.Currency=="USD")
  BG2.loc[(BG2.Borrower.str.contains('DESTINI')),'EXIM Account No.'] = '3308-02137-117-0071-00'
  BG2.loc[(BG2.Borrower.str.contains('ASIA CARGO')),'EXIM Account No.'] = '3308-01137-117-0313-00'
  BG2.loc[(BG2.Borrower.str.contains('PRINSIPTEK')),'EXIM Account No.'] = '3308-02224-216-0032-00'
  BG2.loc[(BG2.Borrower.str.contains('URBAN PINNACLE')),'EXIM Account No.'] = '3308-01137-117-0325-00'
  BG2.loc[(BG2.Borrower.str.contains('PETROLIAM NASIONAL')),'EXIM Account No.'] = '212137862'
  BG2.loc[(BG2.Borrower.str.contains('HELMS GEOMARINE')),'EXIM Account No.'] = '3308-02137-117-0353-00'

  BG2.loc[(BG2['C/I'].isin(['I'])),'Finance(SAP) Number'] = 'BG-I'
  BG2.loc[(BG2['C/I'].isin(['C'])),'Finance(SAP) Number'] = 'BG'
  BG2.loc[(BG2.Borrower.str.contains('OM MATERIAL'))&(BG2.Currency=="USD"),'Finance(SAP) Number'] = '500724'

  BG3 = BG2.fillna(0).groupby(['CIF Number','EXIM Account No.','Finance(SAP) Number','Borrower','C/I'])[['Exposure (RM)','Facility Limit Undrawn (FC)','Facility Limit Undrawn (MYR)']].sum().reset_index()
  #
  BG3.rename(columns={'Borrower':'Customer Name',
                    'Country':'Country Exposure',
                    'C/I':'Type of Financing',
                    'Currency':'Currency','Exposure (RM)':'Contingent Liability (MYR)',
                   'Facility Limit Undrawn (FC)':'Unutilised/Undrawn Amount (FC)','Facility Limit Undrawn (MYR)':'Unutilised/Undrawn Amount (MYR)'},inplace=True)

  #=========================================LC==============================================

  LC2 = LC1.iloc[np.where(LC1.TYPE.isin(["LC",'REVERSAL','AMENDMENT']))]

  LC2.loc[LC2.APPLICANT.str.contains('WSA VENTURE AUSTRALIA'),'EXIM Account No.'] = '3308-02137-122-0291-00'
  LC2.loc[LC2.APPLICANT.isin(['WSA VENTURE AUSTRALIA (M) SDN BHD (FAC 3)']),'CIF Number'] = 'EXIM000283'
  LC2.loc[LC2.APPLICANT.isin(['WSA VENTURE AUSTRALIA (M) SDN BHD (FAC 3)']),'Finance(SAP) Number'] = '501085'

  LC2.loc[LC2.APPLICANT.str.contains('PERTAMA FERROALLOYS SDN BHD'),'EXIM Account No.'] = '3308-02137-211-0142-00'
  LC2.loc[LC2.APPLICANT.isin(['PERTAMA FERROALLOYS SDN BHD']),'CIF Number'] = 'EXIM000140'
  LC2.loc[LC2.APPLICANT.isin(['PERTAMA FERROALLOYS SDN BHD']),'Finance(SAP) Number'] = '500840'

  LC2['Type of Financing'] = 'I'

  LC3 = LC2.fillna(0).groupby(['CIF Number','EXIM Account No.','Finance(SAP) Number','APPLICANT',
                             'Type of Financing'])[['AMOUNT (RM)']].sum().reset_index().rename(columns={'APPLICANT':'Customer Name',
  'AMOUNT (RM)':'Contingent Liability Letter of Credit (MYR)',
  'CURR':'Currency',
  'COUNTRY':'Country Exposure'}) #

  #'FOREIGN AMOUNT', 
  #'FOREIGN AMOUNT':'Contingent Liability Letter of Credit (Facility Currency)',
  LC3['Unutilised/Undrawn Amount (FC)'] = 0
  LC3['Unutilised/Undrawn Amount (MYR)'] = 0

  append = pd.concat([BG3,LC3]).fillna(0)

  LDB_prev['EXIM Account No.'] = LDB_prev['EXIM Account No.'].astype(str)

  appendfinal_ldb = append.merge(LDB_prev[['EXIM Account No.',
                                              'Currency']],on=['EXIM Account No.'],how='left', suffixes=('_x', ''),indicator=True)

  appendfinal_ldb['Currency'] = appendfinal_ldb['Currency'].str.strip()

  append1 = appendfinal_ldb.merge(MRate[['Month','Curr']].rename(columns={'Month':'Currency'}), on='Currency', how='left')

  append1['Contingent Liability (Facility Currency)'] = append1['Contingent Liability (MYR)']/append1['Curr']
  append1['Contingent Liability Letter of Credit (Facility Currency)'] = append1['Contingent Liability Letter of Credit (MYR)']/append1['Curr']
  append1['Unutilised/Undrawn Amount (FC)'] = append1['Unutilised/Undrawn Amount (MYR)']/append1['Curr']

  append2 = append1[['CIF Number',
                   'EXIM Account No.',
                   'Finance(SAP) Number',
                   'Customer Name',
                   #'Country Exposure',
                   'Type of Financing',
                   'Currency',
                   'Curr',
                   'Unutilised/Undrawn Amount (FC)',
                   'Unutilised/Undrawn Amount (MYR)',
                   'Contingent Liability Letter of Credit (Facility Currency)',
                   'Contingent Liability Letter of Credit (MYR)',
                   'Contingent Liability (Facility Currency)',
                   'Contingent Liability (MYR)']]
  
  #---------------------------------------------Download-------------------------------------------------------------
  
  st.write("")
  st.write(f"Sum Undrawn (FC) : RM{float(sum(append2['Unutilised/Undrawn Amount (FC)']))}")
  st.write(f"Sum Undrawn (MYR) : RM{float(sum(append2['Unutilised/Undrawn Amount (MYR)']))}")


  st.write("")
  st.write(f"Sum Contingent BG (FC) : RM{float(sum(append2['Contingent Liability (Facility Currency)']))}")
  st.write(f"Sum Contingent BG (MYR) : RM{float(sum(append2['Contingent Liability (MYR)']))}")
  
  st.write("")
  st.write(f"Sum Contingent LC (FC) : RM{float(sum(append2['Contingent Liability Letter of Credit (Facility Currency)']))}")
  st.write(f"Sum Contingent LC (MYR) : RM{float(sum(append2['Contingent Liability Letter of Credit (MYR)']))}")
  
  st.write("")
  st.write("Row Column Checking: ")
  st.write(append2.shape)

           
  #st.write("SAP Duplication Checking: ")
  #st.write(appendfinal3['Finance(SAP) Number'].value_counts())

  st.write(append2)

  st.write("Download file: ")
  st.download_button("Download CSV",
                   append2.to_csv(index=False),
                   file_name='06. Contigent & Undrawn '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')