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
    <h1>Data Mirror</h1>
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

D1 = form.text_input("Input Interest Sheet ")
D2 = form.text_input("Input Profit Payment Sheet ")
D3 = form.text_input("Input Conventional Other Charges Sheet ")
D4 = form.text_input("Input Islamic Other Charges Sheet ")
D5 = form.text_input("Input IIS Sheet ")
D6 = form.text_input("Input PIS Sheet ")
D7 = form.text_input("Input Penalty Sheet ")
D8 = form.text_input("Input Tawidh Active Sheet ")
D9 = form.text_input("Input Tawidh Recovery Sheet ")


df1 = form.file_uploader(label= "Upload Latest Data Mirror:")

if df1:
  Interest = pd.read_excel(df1, sheet_name=D1, header=8)
  Profit = pd.read_excel(df1, sheet_name=D2, header=8)
  Other_payment_conv = pd.read_excel(df1, sheet_name=D3, header=8)
  Other_payment_isl = pd.read_excel(df1, sheet_name=D4, header=8)
  IIS = pd.read_excel(df1, sheet_name=D5, header=8)
  PIS = pd.read_excel(df1, sheet_name=D6, header=8)
  Penalty = pd.read_excel(df1, sheet_name=D7, header=8)
  T_A = pd.read_excel(df1, sheet_name=D8, header=8)
  T_R = pd.read_excel(df1, sheet_name=D9, header=8)

df2 = form.file_uploader(label= "Upload Loan Database:")

if df2:
  LDB_prev = pd.read_excel(df2, sheet_name="Loan Database", header=1)
  #st.write(LDB_prev.head(1))

submitted = form.form_submit_button("Submit")
if submitted:
  #st.write("Submitted")
  #st.write(year, month)

  st.write(f"File submitted for : "+str(year)+"-"+str(month))
  #st.write(f"All file submitted for :{str(year)+str(month)}")
  
  #---------------------------------Start

  Other_payment_conv['Type_of_Financing'] = 'Conventional'
  Other_payment_isl['Type_of_Financing'] = 'Islamic'

  Interest['Type_of_Financing'] = 'Conventional'
  Profit['Type_of_Financing'] = 'Islamic'

  IIS['Type_of_Financing'] = 'Conventional'
  PIS['Type_of_Financing'] = 'Islamic'

  Other_payment_isl.columns = Other_payment_isl.columns.str.replace("\n", "_")
  Other_payment_isl.columns = Other_payment_isl.columns.str.replace(" ", "_")
  Other_payment_isl.columns = Other_payment_isl.columns.str.replace(".", "_")

  Other_payment_conv.columns = Other_payment_conv.columns.str.replace("\n", "_")
  Other_payment_conv.columns = Other_payment_conv.columns.str.replace(" ", "_")
  Other_payment_conv.columns = Other_payment_conv.columns.str.replace(".", "_")

  Profit.columns = Profit.columns.str.replace("\n", "_")
  Profit.columns = Profit.columns.str.replace(" ", "_")
  Profit.columns = Profit.columns.str.replace(".", "_")

  Interest.columns = Interest.columns.str.replace("\n", "_")
  Interest.columns = Interest.columns.str.replace(" ", "_")
  Interest.columns = Interest.columns.str.replace(".", "_")

  IIS.columns = IIS.columns.str.replace("\n", "_")
  IIS.columns = IIS.columns.str.replace(" ", "_")
  IIS.columns = IIS.columns.str.replace(".", "_")

  PIS.columns = PIS.columns.str.replace("\n", "_")
  PIS.columns = PIS.columns.str.replace(" ", "_")
  PIS.columns = PIS.columns.str.replace(".", "_")

  #---------------------------------------------Penalty-------------------------------------------------------------

  #SJPP
  Other_payment_isl.loc[(~(Other_payment_isl.Account.isna())&(Other_payment_isl.Text.str.contains("SJPP"))),"______Amount_in_DC"] = 0
  Other_payment_isl.loc[(~(Other_payment_isl.Account.isna())&(Other_payment_isl.Text.str.contains("SJPP"))),"___Amt_in_loc_cur_"] = 0
    
  Other_payment_conv.loc[(~(Other_payment_conv.Account.isna())&(Other_payment_conv.Text.str.contains("SJPP"))),"______Amount_in_DC"] = 0
  Other_payment_conv.loc[(~(Other_payment_conv.Account.isna())&(Other_payment_conv.Text.str.contains("SJPP"))),"___Amt_in_loc_cur_"] = 0

  #Penalty
  IIS.loc[(~(IIS.Account.isna())&(IIS.Text.str.contains("Penalty"))),"Ta`widh Payment/Penalty Repayment (Facility Currency)"] = IIS['______Amount_in_DC']
  IIS.loc[(~(IIS.Account.isna())&(IIS.Text.str.contains("Penalty"))),"Ta`widh Payment/Penalty Repayment (MYR)"] = IIS['___Amt_in_loc_cur_']
  IIS.loc[(~(IIS.Account.isna())&(IIS.Text.str.contains("Penalty"))),"______Amount_in_DC"] = 0
  IIS.loc[(~(IIS.Account.isna())&(IIS.Text.str.contains("Penalty"))),"___Amt_in_loc_cur_"] = 0

  PIS.loc[(~(PIS.Account.isna())&((PIS.Text.str.contains("Penalty"))|(PIS.Text.str.contains("Ta'widh")))),"Ta`widh Payment/Penalty Repayment (Facility Currency)"] = PIS['______Amount_in_DC']
  PIS.loc[(~(PIS.Account.isna())&((PIS.Text.str.contains("Penalty"))|(PIS.Text.str.contains("Ta'widh")))),"Ta`widh Payment/Penalty Repayment (MYR)"] = PIS['___Amt_in_loc_cur_']
  PIS.loc[(~(PIS.Account.isna())&((PIS.Text.str.contains("Penalty"))|(PIS.Text.str.contains("Ta'widh")))),"______Amount_in_DC"] = 0
  PIS.loc[(~(PIS.Account.isna())&((PIS.Text.str.contains("Penalty"))|(PIS.Text.str.contains("Ta'widh")))),"___Amt_in_loc_cur_"] = 0

  #PIS blom ad nme kat text untuk penalty

  #---------------------------------------------Process-------------------------------------------------------------

  Other_payment_conv1 = Other_payment_conv.iloc[np.where(~(Other_payment_conv.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC']].sum().reset_index()
  Other_payment_conv1['___Amt_in_loc_cur_'] = -1*Other_payment_conv1['___Amt_in_loc_cur_']
  Other_payment_conv1['______Amount_in_DC'] = -1*Other_payment_conv1['______Amount_in_DC']
  Other_payment_conv1['Account'] = Other_payment_conv1['Account'].astype(int)

  Other_payment_isl1 = Other_payment_isl.iloc[np.where(~(Other_payment_isl.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC']].sum().reset_index()
  Other_payment_isl1['___Amt_in_loc_cur_'] = -1*Other_payment_isl1['___Amt_in_loc_cur_']
  Other_payment_isl1['______Amount_in_DC'] = -1*Other_payment_isl1['______Amount_in_DC']
  Other_payment_isl1['Account'] = Other_payment_isl1['Account'].astype(int)

  Profit1 = Profit.iloc[np.where(~(Profit.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC']].sum().reset_index()
  Profit1['___Amt_in_loc_cur_'] = -1*Profit1['___Amt_in_loc_cur_']
  Profit1['______Amount_in_DC'] = -1*Profit1['______Amount_in_DC']
  Profit1['Account'] = Profit1['Account'].astype(int)

  Interest1 = Interest.iloc[np.where(~(Interest.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC']].sum().reset_index()
  Interest1['___Amt_in_loc_cur_'] = -1*Interest1['___Amt_in_loc_cur_']
  Interest1['______Amount_in_DC'] = -1*Interest1['______Amount_in_DC']
  Interest1['Account'] = Interest1['Account'].astype(int)


  IIS1 = IIS.iloc[np.where(~(IIS.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC',
  "Ta`widh Payment/Penalty Repayment (Facility Currency)",
  "Ta`widh Payment/Penalty Repayment (MYR)"]].sum().reset_index()

  IIS1['___Amt_in_loc_cur_'] = -1*IIS1['___Amt_in_loc_cur_']
  IIS1['______Amount_in_DC'] = -1*IIS1['______Amount_in_DC']
  IIS1['Ta`widh Payment/Penalty Repayment (MYR)'] = -1*IIS1['Ta`widh Payment/Penalty Repayment (MYR)']
  IIS1['Ta`widh Payment/Penalty Repayment (Facility Currency)'] = -1*IIS1['Ta`widh Payment/Penalty Repayment (Facility Currency)']
  IIS1['Account'] = IIS1['Account'].astype(int)

  PIS1 = PIS.iloc[np.where(~(PIS.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC',
  "Ta`widh Payment/Penalty Repayment (Facility Currency)",
  "Ta`widh Payment/Penalty Repayment (MYR)"]].sum().reset_index()

  PIS1['___Amt_in_loc_cur_'] = -1*PIS1['___Amt_in_loc_cur_']
  PIS1['______Amount_in_DC'] = -1*PIS1['______Amount_in_DC']
  PIS1['Ta`widh Payment/Penalty Repayment (MYR)'] = -1*PIS1['Ta`widh Payment/Penalty Repayment (MYR)']
  PIS1['Ta`widh Payment/Penalty Repayment (Facility Currency)'] = -1*PIS1['Ta`widh Payment/Penalty Repayment (Facility Currency)']
  PIS1['Account'] = PIS1['Account'].astype(int)

  Interest1['Ta`widh Payment/Penalty Repayment (MYR)'] = 0
  Interest1['Ta`widh Payment/Penalty Repayment (Facility Currency)'] = 0
  Profit1['Ta`widh Payment/Penalty Repayment (MYR)'] = 0
  Profit1['Ta`widh Payment/Penalty Repayment (Facility Currency)'] = 0

  merge = pd.concat([Other_payment_conv1,Other_payment_isl1]).fillna(0).rename(columns={'___Amt_in_loc_cur_':'Other_Charges_Payment_MYR','______Amount_in_DC':'Other_Charges_Payment_FC'})

  merge1 = pd.concat([Interest1,IIS1,Profit1,PIS1]).fillna(0).rename(columns={'___Amt_in_loc_cur_':'Profit_Payment_Interest_Repayment_MYR','______Amount_in_DC':'Profit_Payment_Interest_Repayment_FC'})

  merge['Account'] = merge['Account'].astype(str)
  merge1['Account'] = merge1['Account'].astype(str)

  LDB_prev['Finance(SAP) Number'] = LDB_prev['Finance(SAP) Number'].astype(str)

  LDB_prev.columns = LDB_prev.columns.str.replace("\n", "")

  LDB_prev['Cumulative Profit Payment/Interest Repayment (Facility Currency)'].fillna(0,inplace=True)
  LDB_prev['Cumulative Profit Payment/Interest Repayment (MYR)'].fillna(0,inplace=True)
  LDB_prev['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)'].fillna(0,inplace=True)
  LDB_prev['Cumulative Ta`widh Payment/Penalty Repayment  (MYR)'].fillna(0,inplace=True)
  LDB_prev['Cumulative Other Charges Payment (Facility Currency)'].fillna(0,inplace=True)
  LDB_prev['Cumulative Other Charges Payment (MYR)'].fillna(0,inplace=True)

  merge_ldb = merge.merge(LDB_prev.iloc[np.where(LDB_prev['Finance(SAP) Number']!="nan")][['Finance(SAP) Number','EXIM Account No.','CIF Number','Customer Name',
                                              'Facility Currency',
                                              'Cumulative Other Charges Payment (Facility Currency)',
                                              'Cumulative Other Charges Payment (MYR)']].drop_duplicates('Finance(SAP) Number',keep='first').rename(columns={'Finance(SAP) Number':'Account'}),on=['Account'],how='outer', suffixes=('_x', ''),indicator=True)

  merge1_ldb = merge1.merge(LDB_prev.iloc[np.where(LDB_prev['Finance(SAP) Number']!="nan")][['Finance(SAP) Number','EXIM Account No.','CIF Number','Customer Name',
                                              'Facility Currency',
                                              'Cumulative Profit Payment/Interest Repayment (Facility Currency)',
                                              'Cumulative Profit Payment/Interest Repayment (MYR)',
                                              'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)',
                                              'Cumulative Ta`widh Payment/Penalty Repayment  (MYR)']].drop_duplicates('Finance(SAP) Number',keep='first').rename(columns={'Finance(SAP) Number':'Account'}),on=['Account'],how='outer', suffixes=('_x', ''),indicator=True)

  merge_ldb['Other_Charges_Payment_MYR'].fillna(0,inplace=True)
  merge_ldb['Other_Charges_Payment_FC'].fillna(0,inplace=True)
  merge_ldb['Cumulative Other Charges Payment (Facility Currency)'].fillna(0,inplace=True) 
  merge_ldb['Cumulative Other Charges Payment (MYR)'].fillna(0,inplace=True)

  merge1_ldb['Profit_Payment_Interest_Repayment_MYR'].fillna(0,inplace=True)
  merge1_ldb['Profit_Payment_Interest_Repayment_FC'].fillna(0,inplace=True)
  merge1_ldb['Ta`widh Payment/Penalty Repayment (MYR)'].fillna(0,inplace=True) 
  merge1_ldb['Ta`widh Payment/Penalty Repayment (Facility Currency)'].fillna(0,inplace=True)
  merge1_ldb['Cumulative Profit Payment/Interest Repayment (Facility Currency)'].fillna(0,inplace=True)
  merge1_ldb['Cumulative Profit Payment/Interest Repayment (MYR)'].fillna(0,inplace=True)
  merge1_ldb['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)'].fillna(0,inplace=True)
  merge1_ldb['Cumulative Ta`widh Payment/Penalty Repayment  (MYR)'].fillna(0,inplace=True)

  merge_ldb['Cumulative Other Charges Payment (MYR) New'] = merge_ldb['Other_Charges_Payment_MYR'] +  merge_ldb['Cumulative Other Charges Payment (MYR)'] 
  merge_ldb['Cumulative Other Charges Payment (Facility Currency) New'] = merge_ldb['Other_Charges_Payment_FC'] +  merge_ldb['Cumulative Other Charges Payment (Facility Currency)'] 


  merge1_ldb['Cumulative Profit Payment/Interest Repayment (MYR) New'] = merge1_ldb['Cumulative Profit Payment/Interest Repayment (MYR)'] +  merge1_ldb['Profit_Payment_Interest_Repayment_MYR'] 
  merge1_ldb['Cumulative Profit Payment/Interest Repayment (Facility Currency) New'] = merge1_ldb['Cumulative Profit Payment/Interest Repayment (Facility Currency)'] +  merge1_ldb['Profit_Payment_Interest_Repayment_FC'] 
  merge1_ldb['Cumulative Ta`widh Payment/Penalty Repayment  (MYR) New'] = merge1_ldb['Cumulative Ta`widh Payment/Penalty Repayment  (MYR)'] +  merge1_ldb['Ta`widh Payment/Penalty Repayment (MYR)'] 
  merge1_ldb['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency) New'] = merge1_ldb['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)'] +  merge1_ldb['Ta`widh Payment/Penalty Repayment (Facility Currency)'] 

  #'Type_of_Financing',
  merge_ldb = merge_ldb[[ 'CIF Number','EXIM Account No.','Account', 'Customer Name',
       'Facility Currency',
       'Other_Charges_Payment_FC', 'Other_Charges_Payment_MYR',
       #'Cumulative Other Charges Payment (Facility Currency)',
       #'Cumulative Other Charges Payment (MYR)',
       'Cumulative Other Charges Payment (Facility Currency) New',
       'Cumulative Other Charges Payment (MYR) New']]

  merge1_ldb = merge1_ldb[['CIF Number','EXIM Account No.','Account', 'Type_of_Financing','Customer Name',
       'Facility Currency',
       'Profit_Payment_Interest_Repayment_FC',
       'Profit_Payment_Interest_Repayment_MYR',
       #'Cumulative Profit Payment/Interest Repayment (Facility Currency)',
       #'Cumulative Profit Payment/Interest Repayment (MYR)',
       'Cumulative Profit Payment/Interest Repayment (Facility Currency) New',
       'Cumulative Profit Payment/Interest Repayment (MYR) New'
       #'Ta`widh Payment/Penalty Repayment (Facility Currency)',
       #'Ta`widh Payment/Penalty Repayment (MYR)',
       #'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)',
       #'Cumulative Ta`widh Payment/Penalty Repayment  (MYR)', 
       #'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency) New',
       #'Cumulative Ta`widh Payment/Penalty Repayment  (MYR) New'
       ]]

  #combine
  combine = merge_ldb.merge(merge1_ldb[['Account', 
       'Profit_Payment_Interest_Repayment_FC',
       'Profit_Payment_Interest_Repayment_MYR',
       #'Cumulative Profit Payment/Interest Repayment (Facility Currency)',
       #'Cumulative Profit Payment/Interest Repayment (MYR)',
       'Cumulative Profit Payment/Interest Repayment (Facility Currency) New',
       'Cumulative Profit Payment/Interest Repayment (MYR) New'
       #'Ta`widh Payment/Penalty Repayment (Facility Currency)',
       #'Ta`widh Payment/Penalty Repayment (MYR)',
       #'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)',
       #'Cumulative Ta`widh Payment/Penalty Repayment  (MYR)', 
       #'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency) New',
       #'Cumulative Ta`widh Payment/Penalty Repayment  (MYR) New'
       ]],on="Account", how="outer") #,indicator=True

  #---------------------------------------------Ta'widh-------------------------------------------------------------

  Penalty.columns = Penalty.columns.str.replace("\n", "_")
  Penalty.columns = Penalty.columns.str.replace(" ", "_")
  Penalty.columns = Penalty.columns.str.replace(".", "_")

  T_A.columns = T_A.columns.str.replace("\n", "_")
  T_A.columns = T_A.columns.str.replace(" ", "_")
  T_A.columns = T_A.columns.str.replace(".", "_")
  
  T_R.columns = T_R.columns.str.replace("\n", "_")
  T_R.columns = T_R.columns.str.replace(" ", "_")
  T_R.columns = T_R.columns.str.replace(".", "_")

  Penalty.columns = T_A.columns = T_R.columns

  Penalty['Type_of_Financing'] = 'Conventional'
  T_A['Type_of_Financing'] = 'Islamic'
  T_R['Type_of_Financing'] = 'Islamic'

  Penalty1 = Penalty.iloc[np.where(~(Penalty.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC']].sum().reset_index()
  T_A1 = T_A.iloc[np.where(~(T_A.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC']].sum().reset_index()
  T_R1 = T_R.iloc[np.where(~(T_R.Account.isna()))].fillna(0).groupby(['Account','Type_of_Financing'])[['___Amt_in_loc_cur_','______Amount_in_DC']].sum().reset_index()

  Tawidh_Comb = pd.concat([Penalty1, T_A1, T_R1])
  
  Tawidh_Comb['___Amt_in_loc_cur_'] = -1*Tawidh_Comb['___Amt_in_loc_cur_']
  Tawidh_Comb['______Amount_in_DC'] = -1*Tawidh_Comb['______Amount_in_DC']

  Tawidh_Comb.rename(columns={'___Amt_in_loc_cur_':"Ta`widh Payment/Penalty Repayment (MYR)",
                  '______Amount_in_DC':"Ta`widh Payment/Penalty Repayment (Facility Currency)"},inplace=True)

  
  Tawidh_Comb['Account'] = Tawidh_Comb['Account'].astype(int)
  Tawidh_Comb['Account'] = Tawidh_Comb['Account'].astype(str)
  
  Tawidh_Comb1 = Tawidh_Comb.merge(LDB_prev.iloc[np.where(LDB_prev['Finance(SAP) Number']!="nan")][['Finance(SAP) Number','EXIM Account No.','CIF Number','Customer Name',
                                              'Facility Currency',
                                              'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)',
                                              'Cumulative Ta`widh Payment/Penalty Repayment  (MYR)']].drop_duplicates('Finance(SAP) Number',keep='first').rename(columns={'Finance(SAP) Number':'Account'}),on=['Account'],how='outer', suffixes=('_x', ''),indicator=True)

  Tawidh_Comb1['Ta`widh Payment/Penalty Repayment (MYR)'].fillna(0,inplace=True) 
  Tawidh_Comb1['Ta`widh Payment/Penalty Repayment (Facility Currency)'].fillna(0,inplace=True)

  Tawidh_Comb1['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)'].fillna(0,inplace=True)
  Tawidh_Comb1['Cumulative Ta`widh Payment/Penalty Repayment  (MYR)'].fillna(0,inplace=True)
  
  Tawidh_Comb1['Cumulative Ta`widh Payment/Penalty Repayment  (MYR) New'] = Tawidh_Comb1['Cumulative Ta`widh Payment/Penalty Repayment  (MYR)'] +  Tawidh_Comb1['Ta`widh Payment/Penalty Repayment (MYR)'] 
  Tawidh_Comb1['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency) New'] = Tawidh_Comb1['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)'] +  Tawidh_Comb1['Ta`widh Payment/Penalty Repayment (Facility Currency)'] 

  Tawidh_Comb1 = Tawidh_Comb1[[ 'CIF Number','EXIM Account No.','Account', 'Customer Name',
       'Facility Currency',
       'Ta`widh Payment/Penalty Repayment (Facility Currency)',
       'Ta`widh Payment/Penalty Repayment (MYR)',
       #'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)',
       #'Cumulative Ta`widh Payment/Penalty Repayment  (MYR)', 
       'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency) New',
       'Cumulative Ta`widh Payment/Penalty Repayment  (MYR) New']]

  
  #combine2
  combine2 = combine.merge(Tawidh_Comb1[['Account', 
       'Ta`widh Payment/Penalty Repayment (Facility Currency)',
       'Ta`widh Payment/Penalty Repayment (MYR)',
       #'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency)',
       #'Cumulative Ta`widh Payment/Penalty Repayment  (MYR)', 
       'Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency) New',
       'Cumulative Ta`widh Payment/Penalty Repayment  (MYR) New'
       ]],on="Account", how="outer") #,indicator=True
  
  #st.write(combine2['Account'].value_counts())

  #---------------------------------------------Download-------------------------------------------------------------

  #st.write('Sum Total Loans Outstanding (MYR) : RM'+str(sum))

  st.write("")
  #st.write(f"Sum Other Charges Payment (FC) : ${float(sum(combine['Other_Charges_Payment_FC']))}")
  st.write(f"Sum Other Charges Payment (MYR) : RM{float(sum(combine['Other_Charges_Payment_MYR']))}")
  st.write("")
  #st.write(f"Sum Cummulative Other Charges Payment (FC) : ${float(sum(combine['Cumulative Other Charges Payment (Facility Currency) New']))}")
  st.write(f"Sum Cummulative Other Charges Payment (MYR) : RM{float(sum(combine['Cumulative Other Charges Payment (MYR) New']))}")
  st.write("")
  #st.write(f"Sum Profit Payment (FC) : ${float(sum(combine['Profit_Payment_Interest_Repayment_FC']))}")
  st.write(f"Sum Profit Payment (MYR) : RM{float(sum(combine['Profit_Payment_Interest_Repayment_MYR']))}")
  st.write("")
  #st.write(f"Sum Cummulative Profit Payment (FC) : ${float(sum(combine['Cumulative Profit Payment/Interest Repayment (Facility Currency) New']))}")
  st.write(f"Sum Cummulative Profit Payment (MYR) : RM{float(sum(combine['Cumulative Profit Payment/Interest Repayment (MYR) New']))}")
  st.write("")
  #st.write(f"Sum Ta`widh Payment (FC) : ${float(sum(combine['Ta`widh Payment/Penalty Repayment (Facility Currency)']))}")
  st.write(f"Sum Ta`widh Payment (MYR) : RM{float(sum(combine2['Ta`widh Payment/Penalty Repayment (MYR)']))}")
  st.write("")
  #st.write(f"Sum Cumulative Ta`widh Payment (FC) : ${float(sum(combine['Cumulative Ta`widh Payment/Penalty Repayment (Facility Currency) New']))}")
  st.write(f"Sum Cumulative Ta`widh Payment (MYR) : RM{float(sum(combine2['Cumulative Ta`widh Payment/Penalty Repayment  (MYR) New']))}")

  st.write("")
  st.write("Row Column Checking: ")
  st.write(combine2.shape)

  st.write(combine2)

  st.write("Download file: ")
  st.download_button("Download CSV",
                   combine2.to_csv(index=False),
                   file_name='05. Profit Payment & Other Charges Payment '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')
  

  #st.write("Row Column Checking: ")
  #st.write(merge1_ldb.shape)

  #st.write(merge1_ldb)
           
  #st.write("SAP Duplication Checking: ")
  #st.write(appendfinal3['Account'].value_counts())

  #st.write("Download file: ")
  #st.download_button("Download CSV",
  #                 merge1_ldb.to_csv(index=False),
  #                 file_name='05. Profit Payment '+str(year)+"-"+str(month)+'.csv',
  #                 mime='text/csv')