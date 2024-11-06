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

BalanceOS = form.text_input("Input Balance Column ") #"Balance_31stAugust2024"

year = form.slider("Year", min_value=2020, max_value=2030, step=1)
month = form.slider("Month", min_value=1, max_value=12, step=1)

#age = form.slider("Age", min_value=18, max_value=100, step=1)
#date = form.date_input("Date", value=dt.date.today())

D1 = form.text_input("Input Islamic Cost Sheet ")
D2 = form.text_input("Input Islamic Profit Sheet ")
D3 = form.text_input("Input Mora Sheet ")
D4 = form.text_input("Input Conventional Cost Sheet ")
D5 = form.text_input("Input Conventional Accrued Sheet ")
D6 = form.text_input("Input Conventional Other Charges Sheet ")
D7 = form.text_input("Input Islamic Other Charges Sheet ")
D8 = form.text_input("Input IIS Sheet ")
D9 = form.text_input("Input PIS Sheet ")
D10 = form.text_input("Input Penalty Sheet ")
D11 = form.text_input("Input Ta'widh Active Sheet ")
D12 = form.text_input("Input Ta'widh Recovery Sheet ")

df1 = form.file_uploader(label= "Upload Latest Debtor Listing:")

if df1:
  Isl_Cost = pd.read_excel(df1, sheet_name=D1, header=5)
  #st.write(Isl_Cost.head(1))
  Isl_Profit = pd.read_excel(df1, sheet_name=D2, header=3)
  Mora = pd.read_excel(df1, sheet_name=D3, header=5)
  Conv = pd.read_excel(df1, sheet_name=D4, header=2)
  Accrued = pd.read_excel(df1, sheet_name=D5, header=4)
  Others_conv = pd.read_excel(df1, sheet_name=D6, header=4)
  Others_Isl = pd.read_excel(df1, sheet_name=D7, header=4)
  IIS = pd.read_excel(df1, sheet_name=D8, header=4)
  PIS = pd.read_excel(df1, sheet_name=D9, header=4)
  Penalty = pd.read_excel(df1, sheet_name=D10, header=4)
  Ta_A = pd.read_excel(df1, sheet_name=D11, header=4)
  Ta_R = pd.read_excel(df1, sheet_name=D12, header=4)


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
  
  #---------------------------------Debtors Listing Islamic (Cost) include adjustment

  Isl_Cost1 = Isl_Cost.iloc[np.where(~Isl_Cost['Customer\nAccount'].isna())]

  Isl_Cost1.columns = Isl_Cost1.columns.str.replace("\n", "_")
  Isl_Cost1.columns = Isl_Cost1.columns.str.replace(" ", "")

  Isl_Cost1.Customer_Account = Isl_Cost1.Customer_Account.astype(int)
  Isl_Cost1.Disbursement = Isl_Cost1.Disbursement.astype(float)
  Isl_Cost1.Cost_Payment = Isl_Cost1.Cost_Payment.astype(float)
  Isl_Cost1[BalanceOS] = Isl_Cost1[BalanceOS].astype(float)

  Isl_Cost1.rename(columns={"Disbursement":"Disbursement - old"}, inplace=True)
  Isl_Cost1['Disbursement'] = Isl_Cost1['Disbursement - old'].fillna(0) + Isl_Cost1['Adjustment/_Capitalisation'].fillna(0)

  Isl_Cost1.rename(columns={"Cost_Payment":"Cost_Payment - old"}, inplace=True)
  Isl_Cost1['Cost_Payment'] = Isl_Cost1['Cost_Payment - old'].fillna(0) - Isl_Cost1['Adjustment/_Capitalisation.1'].fillna(0)

  Isl_Cost2 = Isl_Cost1.fillna(0).groupby(['Company','Customer_Account'\
  ,'Currency'])[['Disbursement'\
  ,'Cost_Payment',BalanceOS]].sum().reset_index()

  Isl_Cost2 = Isl_Cost2.rename(columns={BalanceOS: 'Principal'}).fillna(0).sort_values(by=['Principal'],ascending=[True])
  #Isl_Cost2['Sheet'] = 'Debtors Listing Islamic (Cost)'
  Isl_Cost2['Financing_Type'] = 'Islamic'
  
  #---------------------------------Debtors Listing Islamic (Profit) include adjustment
  
  Isl_Profit1 = Isl_Profit.iloc[np.where(~Isl_Profit['Customer\nAccount'].isna())]

  Isl_Profit1.columns = Isl_Profit1.columns.str.replace("\n", "_")
  Isl_Profit1.columns = Isl_Profit1.columns.str.replace(" ", "")

  Isl_Profit1.Customer_Account = Isl_Profit1.Customer_Account.astype(int)
  Isl_Profit1.Unearned_Profit = Isl_Profit1.Unearned_Profit.astype(float)
  Isl_Profit1.Profit_Payment = Isl_Profit1.Profit_Payment.astype(float)
  Isl_Profit1[BalanceOS] = Isl_Profit1[BalanceOS].astype(float)

  Isl_Profit1.rename(columns={"Profit_Payment":"Profit_Payment - old"}, inplace=True)
  Isl_Profit1['Profit_Payment'] = Isl_Profit1['Profit_Payment - old'].fillna(0) - Isl_Profit1['Adjustment/_Capitalisation.1'].fillna(0)

  Isl_Profit2 = Isl_Profit1.fillna(0).groupby(['Company','Customer_Account'\
  ,'Currency'])[['Unearned_Profit','Rental(Ijarah)','Profit_Payment',BalanceOS]].sum().reset_index()

  Isl_Profit2 = Isl_Profit2.rename(columns={BalanceOS: 'Interest'}).fillna(0).sort_values(by=['Interest'],ascending=[True])
  #Isl_Profit2['Sheet'] = 'Debtors Listing Islamic (Profit)'
  Isl_Profit2['Financing_Type'] = 'Islamic'

  #Combine Islamic Cost+Profit
  A001 = Isl_Cost2.merge(Isl_Profit2,on=['Customer_Account','Company','Currency','Financing_Type'],how='outer',indicator=True)

  A001 = A001.drop(columns=['_merge'])

  A002 = A001.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type'])[['Disbursement'\
  ,'Cost_Payment','Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest']].sum().reset_index()

  NamaCompany = A001[['Company','Customer_Account']].drop_duplicates('Customer_Account', keep='first')
  A003 = A002.merge(NamaCompany,on='Customer_Account',how='left')

  #---------------------------------Modification MORA & R&R Apr2024

  Mora1 = Mora.fillna(0).rename(columns={'Borrower code': 'Customer_Account',
                            'Borrower':'Company',
                            'Modification impact (RM)':'Mora',
                            'Islamic/ conventional':'Financing_Type'}).iloc[np.where((~Mora['Borrower code'].isna())&(Mora['Borrower code']!='Borrower code'))]

  Mora1.columns = Mora1.columns.str.replace("\n", "_")
  Mora1.columns = Mora1.columns.str.replace(" ", "")

  Mora1.Customer_Account = Mora1.Customer_Account.astype(int)
  Mora1.Mora = Mora1.Mora.astype(float)

  Mora1.loc[Mora1.Currency.isin(['RM']),'Currency'] = 'MYR'

  A004 = A003.merge(Mora1[['Customer_Account','Company','Currency','Financing_Type','SLOacceptancedate','Mora']],on=['Customer_Account','Company','Currency','Financing_Type'],how='outer',indicator=True)

  NamaMora = A004[['Company','Customer_Account']].drop_duplicates('Customer_Account', keep='first')
  A004 = A004.drop(['Company','_merge'],axis=1).merge(NamaMora,on='Customer_Account',how='left')

  A004 = A004.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Cost_Payment','Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest','Mora']].sum().reset_index()

  #---------------------------------Other Debtors Islamic Apr2024
  
  Others_Isl1 = Others_Isl.iloc[np.where(~Others_Isl.Customer.isna())].fillna(0)

  Others_Isl1.columns = Others_Isl1.columns.str.replace("\n", "_")
  Others_Isl1.columns = Others_Isl1.columns.str.replace(" ", "")

  Others_Isl1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Other_Charges'},inplace=True)

  Others_Isl1.Customer_Account = Others_Isl1.Customer_Account.astype(int)
  Others_Isl1.Other_Charges = Others_Isl1.Other_Charges.astype(float)

  Others_Isl1 = Others_Isl1.fillna(0).groupby(['Company','Customer_Account'])[['Other_Charges']].sum().reset_index()

  Others_Isl1['Financing_Type'] = 'Islamic'

  A005 = A004.merge(Others_Isl1,on=['Customer_Account','Company','Financing_Type'],how='outer',indicator=True)

  NamaOther = A005[['Company','Customer_Account','Currency']].drop_duplicates('Customer_Account', keep='first')
  A005 = A005.drop(['Company','Currency','_merge'],axis=1).merge(NamaOther,on='Customer_Account',how='left')

  A005 = A005.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Cost_Payment','Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest','Mora','Other_Charges']].sum().reset_index()

  #---------------------------------PIS
  
  PIS1 = PIS.iloc[np.where(~PIS.Customer.isna())].fillna(0)

  PIS1.columns = PIS1.columns.str.replace("\n", "_")
  PIS1.columns = PIS1.columns.str.replace(" ", "")

  PIS1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Interest_in_Suspense'},inplace=True)

  PIS1.Customer_Account = PIS1.Customer_Account.astype(int)
  PIS1.Interest_in_Suspense = PIS1.Interest_in_Suspense.astype(float)

  PIS1 = PIS1.fillna(0).groupby(['Company','Customer_Account'])[['Interest_in_Suspense']].sum().reset_index()

  PIS1['Financing_Type'] = 'Islamic'

  A006 = A005.merge(PIS1,on=['Customer_Account','Company','Financing_Type'],how='outer',indicator=True)

  NamaPIS = A006[['Company','Customer_Account','Currency']].drop_duplicates('Customer_Account', keep='first')
  A006 = A006.drop(['Company','Currency','_merge'],axis=1).merge(NamaPIS,on='Customer_Account',how='left')

  A006 = A006.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Cost_Payment','Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest','Mora','Other_Charges','Interest_in_Suspense']].sum().reset_index()

  #---------------------------------Penalty Islamic
  
  Ta_A1 = Ta_A.iloc[np.where(~Ta_A.Customer.isna())].fillna(0)

  Ta_A1.columns = Ta_A1.columns.str.replace("\n", "_")
  Ta_A1.columns = Ta_A1.columns.str.replace(" ", "")

  Ta_A1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Penalty_Tawidh'},inplace=True)
  
  Ta_A1.Customer_Account = Ta_A1.Customer_Account.astype(int)
  Ta_A1.Penalty_Tawidh = Ta_A1.Penalty_Tawidh.astype(float)

  Ta_A1 = Ta_A1.fillna(0).groupby(['Company','Customer_Account'])[['Penalty_Tawidh']].sum().reset_index()

  Ta_A1['Financing_Type'] = 'Islamic'

  Ta_R1 = Ta_R.iloc[np.where(~Ta_R.Customer.isna())].fillna(0)

  Ta_R1.columns = Ta_R1.columns.str.replace("\n", "_")
  Ta_R1.columns = Ta_R1.columns.str.replace(" ", "")

  Ta_R1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Recovery_Tawidh'},inplace=True)
  
  Ta_R1.Customer_Account = Ta_R1.Customer_Account.astype(int)
  Ta_R1.Recovery_Tawidh = Ta_R1.Recovery_Tawidh.astype(float)

  Ta_R1 = Ta_R1.fillna(0).groupby(['Company','Customer_Account'])[['Recovery_Tawidh']].sum().reset_index()

  Ta_R1['Financing_Type'] = 'Islamic'

  #Ta_A1.columns = Ta_R1.columns
  Ta_AR = pd.concat([Ta_A1,Ta_R1])
  Ta_AR.fillna(0, inplace=True)

  #st.write(Ta_AR)

  A006_1 = A006.merge(Ta_AR,on=['Customer_Account','Company','Financing_Type'],how='outer',indicator=True)

  NamaTa_AR = A006_1[['Company','Customer_Account','Currency']].drop_duplicates('Customer_Account', keep='first')
  A006_1 = A006_1.drop(['Company','Currency','_merge'],axis=1).merge(NamaTa_AR,on='Customer_Account',how='left')

  A006_1 = A006_1.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Cost_Payment','Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest','Mora','Other_Charges','Interest_in_Suspense',"Penalty_Tawidh",'Recovery_Tawidh']].sum().reset_index()

  #st.write(sum(A006_1["Penalty_Tawidh"]))
  #st.write(sum(Ta_AR["Penalty_Tawidh"]))
  
  #-------------------------------------------------conv--------------------------------------------------

  #Debtors Listing Conv Apr 2024
  Conv1 = Conv.iloc[np.where(~Conv['Customer Account Number'].isna())]

  Conv1.columns = Conv1.columns.str.replace("\n", "_")
  Conv1.columns = Conv1.columns.str.replace(" ", "")

  Conv1 = Conv1.rename(columns={'CustomerAccountNumber': 'Customer_Account',
                            'CustomerName':'Company',
                            'LoanCurrency':'Currency',
                            'ClosingPrincipal':'Principal'}).fillna(0)

  Conv1.Customer_Account = Conv1.Customer_Account.astype(int)
  Conv1.Principal = Conv1.Principal.astype(float)

  #[['Customer_Account','Company','Currency','Disbursement','Repayment','Principal']]

  Conv1.rename(columns={"Disbursement":"Disbursement - old"}, inplace=True)
  Conv1['Disbursement'] = Conv1['Disbursement - old'].fillna(0) + Conv1['AdjustmentCapitalization'].fillna(0)

  Conv1.rename(columns={"Repayment":"Repayment - old"}, inplace=True)
  Conv1['Repayment'] = Conv1['Repayment - old'].fillna(0) - Conv1['AdjustmentCapitalization.1'].fillna(0)

  Conv1 = Conv1.fillna(0).groupby(['Company','Customer_Account'\
  ,'Currency'])[['Disbursement'\
  ,'Repayment','Principal']].sum().reset_index()

  Conv1['Financing_Type'] = 'Conventional'

  #---------------------------------Accrued Interest Apr2024
  Accrued1 = Accrued.iloc[np.where(~Accrued.Customer.isna())].fillna(0)

  Accrued1.columns = Accrued1.columns.str.replace("\n", "_")
  Accrued1.columns = Accrued1.columns.str.replace(" ", "")

  Accrued1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Interest',
                            'Debitrept.period':'Interest_For_the_Month',
                            'Creditreportper.':'Profit_Payment'},inplace=True)

  Accrued1.Customer_Account = Accrued1.Customer_Account.astype(int)
  Accrued1.Interest = Accrued1.Interest.astype(float)
  Accrued1.Interest_For_the_Month = Accrued1.Interest_For_the_Month.astype(float)
  Accrued1.Profit_Payment = Accrued1.Profit_Payment.astype(float)

  Accrued1.loc[(Accrued1['SGLInd.'].isin(['X'])),'Interest_For_the_Month'] = Accrued1.Interest_For_the_Month
  Accrued1.loc[(~Accrued1['SGLInd.'].isin(['X'])),'Interest_For_the_Month'] = 0

  Accrued1.loc[(Accrued1['SGLInd.'].isin(['X'])),'Profit_Payment'] = Accrued1.Profit_Payment
  Accrued1.loc[(~Accrued1['SGLInd.'].isin(['X'])),'Profit_Payment'] = 0

  Accrued1 = Accrued1.fillna(0).groupby(['Company','Customer_Account'])[['Interest_For_the_Month','Interest','Profit_Payment']].sum().reset_index()

  Accrued1['Financing_Type'] = 'Conventional'
  
  #Combine Conv Principal+Accrued
  C001 = Conv1.merge(Accrued1,on=['Customer_Account','Company','Financing_Type'],how='outer',indicator=True)

  NamaConv = C001[['Company','Customer_Account','Currency']].drop_duplicates('Customer_Account', keep='first')
  C002 = C001.drop(['Company','Currency','_merge'],axis=1).merge(NamaConv,on='Customer_Account',how='left')

  C002 = C002.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Repayment','Principal','Interest_For_the_Month','Interest','Profit_Payment']].sum().reset_index()

  #Other Debtors Apr2024
  Others_conv1 = Others_conv.iloc[np.where(~Others_conv.Customer.isna())].fillna(0)

  Others_conv1.columns = Others_conv1.columns.str.replace("\n", "_")
  Others_conv1.columns = Others_conv1.columns.str.replace(" ", "")

  Others_conv1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Other_Charges'},inplace=True)

  Others_conv1.Customer_Account = Others_conv1.Customer_Account.astype(int)
  Others_conv1.Other_Charges = Others_conv1.Other_Charges.astype(float)

  Others_conv1 = Others_conv1.fillna(0).groupby(['Company','Customer_Account'])[['Other_Charges']].sum().reset_index()

  Others_conv1['Financing_Type'] = 'Conventional'

  C003 = C002.merge(Others_conv1,on=['Customer_Account','Company','Financing_Type'],how='outer',indicator=True)

  NamaOtherConv = C003[['Company','Customer_Account','Currency']].drop_duplicates('Customer_Account', keep='first')
  C004 = C003.drop(['Company','Currency','_merge'],axis=1).merge(NamaOtherConv,on='Customer_Account',how='left')

  C004 = C004.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Repayment','Principal','Interest_For_the_Month','Interest','Profit_Payment','Other_Charges']].sum().reset_index()

  #IIS
  IIS1 = IIS.iloc[np.where(~IIS.Customer.isna())].fillna(0)

  IIS1.columns = IIS1.columns.str.replace("\n", "_")
  IIS1.columns = IIS1.columns.str.replace(" ", "")

  IIS1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Interest_in_Suspense'},inplace=True)

  IIS1.Customer_Account = IIS1.Customer_Account.astype(int)
  IIS1.Interest_in_Suspense = IIS1.Interest_in_Suspense.astype(float)

  IIS1 = IIS1.fillna(0).groupby(['Company','Customer_Account'])[['Interest_in_Suspense']].sum().reset_index()

  IIS1['Financing_Type'] = 'Conventional'

  C005 = C004.merge(IIS1,on=['Customer_Account','Company','Financing_Type'],how='outer', indicator=True)

  NamaIIS = C005[['Company','Customer_Account','Currency']].drop_duplicates('Customer_Account', keep='first')
  C005 = C005.drop(['Company','Currency','_merge'],axis=1).merge(NamaIIS,on='Customer_Account',how='left')

  C005 = C005.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Repayment','Principal','Interest_For_the_Month','Interest','Profit_Payment','Other_Charges','Interest_in_Suspense']].sum().reset_index()
  
  #---------------------------------Penalty Conventional
  
  Penalty1 = Penalty.iloc[np.where(~Penalty.Customer.isna())].fillna(0)

  Penalty1.columns = Penalty1.columns.str.replace("\n", "_")
  Penalty1.columns = Penalty1.columns.str.replace(" ", "")

  Penalty1.rename(columns={'Customer': 'Customer_Account',
                            'SearchTerm':'Company',
                            'Crcy':'Currency',
                            'Accumulatedbalance':'Penalty_Tawidh'},inplace=True)
  
  Penalty1.Customer_Account = Penalty1.Customer_Account.astype(int)
  Penalty1.Penalty_Tawidh = Penalty1.Penalty_Tawidh.astype(float)

  Penalty1 = Penalty1.fillna(0).groupby(['Company','Customer_Account'])[['Penalty_Tawidh']].sum().reset_index()

  Penalty1['Financing_Type'] = 'Conventional'
  
  
  C005_1 = C005.merge(Penalty1,on=['Customer_Account','Company','Financing_Type'],how='outer', indicator=True)

  NamaPenal = C005_1[['Company','Customer_Account','Currency']].drop_duplicates('Customer_Account', keep='first')
  C005_1 = C005_1.drop(['Company','Currency','_merge'],axis=1).merge(NamaPenal,on='Customer_Account',how='left')

  C005_1 = C005_1.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Repayment','Principal','Interest_For_the_Month','Interest','Profit_Payment','Other_Charges','Interest_in_Suspense',"Penalty_Tawidh"]].sum().reset_index()
  
  #st.write(sum(C005_1["Penalty_Tawidh"]))
  #st.write(sum(Penalty1["Penalty_Tawidh"]))

  #-------------------------------------------------combine-------------------------------------------------
  C005_1['Recovery_Tawidh'] = 0
  C005_1['Cost_Payment'] = 0
  C005_1['Unearned_Profit'] = C005['Interest_For_the_Month']
  #C005['Profit_Payment'] = 0
  C005_1['Mora'] = 0
  C005_1['Rental(Ijarah)'] = 0

  C006 = C005_1[['Customer_Account','Currency','Financing_Type','Company','Disbursement','Repayment','Cost_Payment',
             'Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest','Mora','Other_Charges',
             'Interest_in_Suspense',"Penalty_Tawidh",'Recovery_Tawidh']]

  A006_1['Repayment'] = 0

  A007 = A006_1[['Customer_Account','Currency','Financing_Type','Company','Disbursement','Repayment','Cost_Payment',
               'Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest','Mora','Other_Charges',
               'Interest_in_Suspense',"Penalty_Tawidh",'Recovery_Tawidh']]

  #Isl_Cost1.columns = Isl_Profit1.columns = Mora1.columns = Conv1.columns
  #appendR = pd.concat([Isl_Cost1,Isl_Profit1,Mora1,Conv1] )

  C006.columns = A007.columns
  appendR = pd.concat([C006,A007])

  NamaappendR = appendR.iloc[np.where(~(appendR.Currency.isin([0,'0'])))][['Company','Currency','Customer_Account']].drop_duplicates('Customer_Account', keep='first')
  appendR = appendR.drop(['Company','Currency'],axis=1).merge(NamaappendR,on='Customer_Account',how='left')

  appendfinal = appendR.fillna(0).groupby(['Customer_Account'\
  ,'Currency','Financing_Type','Company'])[['Disbursement'\
  ,'Repayment','Cost_Payment','Principal','Unearned_Profit','Rental(Ijarah)','Profit_Payment','Interest','Mora','Other_Charges','Interest_in_Suspense',"Penalty_Tawidh",'Recovery_Tawidh']].sum().reset_index()

  appendfinal['Total Loans Outstanding (MYR)'] = appendfinal['Principal'] + appendfinal['Interest'] + appendfinal['Mora'] + appendfinal['Other_Charges'] + appendfinal['Penalty_Tawidh']

  appendfinal['Cost Payment/Principal Repayment (MYR)'] = (-1*appendfinal['Repayment']) + appendfinal['Cost_Payment']
  appendfinal['Accrued Profit/Interest of the month (MYR)'] = appendfinal['Unearned_Profit'] + appendfinal['Rental(Ijarah)'] #+ profit for the month

  appendfinal.rename(columns={'Customer_Account':'Finance(SAP) Number',
                           'Currency':'Facility Currency',
                           'Financing_Type':'Type of Financing',
                            "Company":"Customer Name",
                            "Disbursement":"Disbursement/Drawdown (MYR)",
                           'Principal':'Cost/Principal Outstanding (MYR)',
                           'Profit_Payment':"Profit Payment/Interest Repayment (MYR)",
                           'Interest':'Cumulative Accrued Profit/Interest (MYR)',
                           'Mora':'Modification of Loss (MYR)',
                           'Other_Charges':'Other Charges (MYR)',
                           'Interest_in_Suspense':'Income/Interest in Suspense (MYR)',
                           "Penalty_Tawidh":"Ta`widh Payment/Penalty Repayment (MYR)",
                           'Recovery_Tawidh':"Ta'widh (Compensation) (MYR)"}, inplace=True)

  appendfinal.drop(columns=['Repayment','Cost_Payment','Unearned_Profit','Rental(Ijarah)'], axis=1, inplace=True)

                           #"Repayment":"1. Cost Payment/Principal Repayment (MYR)",
                           #"Cost_Payment":'2. Cost Payment/Principal Repayment (MYR)',


                           #'Unearned_Profit':'Accrued Profit/Interest of the month (MYR)',
                           #'Rental(Ijarah)':'Ijarah',
  appendfinal['Finance(SAP) Number'] = appendfinal['Finance(SAP) Number'].astype(str)

  LDB_prev['Finance(SAP) Number'] = LDB_prev['Finance(SAP) Number'].astype(str)

  LDB_prev.columns = LDB_prev.columns.str.replace("\n", "")

  appendfinal_ldb = appendfinal.merge(LDB_prev.iloc[np.where(LDB_prev['EXIM Account No.']!="Total")][['EXIM Account No.','Finance(SAP) Number',
                                              'Customer Name',
                                              'Facility Currency',
                                              'Cumulative Disbursement/Drawdown (Facility Currency)',
                                              'Cumulative Disbursement/Drawdown (MYR)',
                                              'Cumulative Cost Payment/Principal Repayment (Facility Currency)',
                                              'Cumulative Cost Payment/Principal Repayment (MYR)',
                                              'Cumulative Profit Payment/Interest Repayment (Facility Currency)',
                                              'Cumulative Profit Payment/Interest Repayment (MYR)']].drop_duplicates('Finance(SAP) Number',keep='first'),on=['Finance(SAP) Number'],how='inner', suffixes=('_x', ''),indicator=True)

  appendfinal_ldb['Facility Currency'] = appendfinal_ldb['Facility Currency'].astype(str)
  appendfinal_ldb['Facility Currency'] = appendfinal_ldb['Facility Currency'].str.strip()

  appendfinal2 = appendfinal_ldb.merge(MRate[['Month','Curr']].rename(columns={'Month':'Facility Currency'}), on='Facility Currency', how='left')

  appendfinal2['Cost/Principal Outstanding (Facility Currency)'] = appendfinal2['Cost/Principal Outstanding (MYR)']/appendfinal2['Curr']
  appendfinal2['Accrued Profit/Interest of the month (Facility Currency)'] = appendfinal2['Accrued Profit/Interest of the month (MYR)']/appendfinal2['Curr']
  appendfinal2['Modification of Loss (Facility Currency)'] = appendfinal2['Modification of Loss (MYR)']/appendfinal2['Curr']
  appendfinal2['Cumulative Accrued Profit/Interest (Facility Currency)'] = appendfinal2['Cumulative Accrued Profit/Interest (MYR)']/appendfinal2['Curr']
  appendfinal2['Income/Interest in Suspense (Facility Currency)'] = appendfinal2['Income/Interest in Suspense (MYR)']/appendfinal2['Curr']
  appendfinal2['Other Charges (Facility Currency)'] = appendfinal2['Other Charges (MYR)']/appendfinal2['Curr']
  appendfinal2['Total Loans Outstanding (Facility Currency)'] = appendfinal2['Total Loans Outstanding (MYR)']/appendfinal2['Curr']
  appendfinal2['Disbursement/Drawdown (Facility Currency)'] = appendfinal2['Disbursement/Drawdown (MYR)']/appendfinal2['Curr']
  appendfinal2['Cost Payment/Principal Repayment (Facility Currency)'] = appendfinal2['Cost Payment/Principal Repayment (MYR)']/appendfinal2['Curr']
  appendfinal2['Profit Payment/Interest Repayment (Facility Currency)'] = appendfinal2['Profit Payment/Interest Repayment (MYR)']/appendfinal2['Curr']
  appendfinal2["Ta`widh Payment/Penalty Repayment (Facility Currency)"] = appendfinal2["Ta`widh Payment/Penalty Repayment (MYR)"]/appendfinal2['Curr']
  appendfinal2["Ta'widh (Compensation) (Facility Currency)"] = appendfinal2["Ta'widh (Compensation) (MYR)"]/appendfinal2['Curr']


  appendfinal2['Cumulative Disbursement/Drawdown (Facility Currency) New'] = appendfinal2['Disbursement/Drawdown (Facility Currency)'] +  appendfinal2['Cumulative Disbursement/Drawdown (Facility Currency)'] 
  appendfinal2['Cumulative Disbursement/Drawdown (MYR) New'] = appendfinal2['Disbursement/Drawdown (MYR)'] +  appendfinal2['Cumulative Disbursement/Drawdown (MYR)'] 
  appendfinal2['Cumulative Cost Payment/Principal Repayment (Facility Currency) New'] = appendfinal2['Cost Payment/Principal Repayment (Facility Currency)'] +  appendfinal2['Cumulative Cost Payment/Principal Repayment (Facility Currency)'] 
  appendfinal2['Cumulative Cost Payment/Principal Repayment (MYR) New'] = appendfinal2['Cost Payment/Principal Repayment (MYR)'] +  appendfinal2['Cumulative Cost Payment/Principal Repayment (MYR)'] 
  appendfinal2['Cumulative Profit Payment/Interest Repayment (Facility Currency) New'] = appendfinal2['Profit Payment/Interest Repayment (Facility Currency)'] +  appendfinal2['Cumulative Profit Payment/Interest Repayment (Facility Currency)'] 
  appendfinal2['Cumulative Profit Payment/Interest Repayment (MYR) New'] = appendfinal2['Profit Payment/Interest Repayment (MYR)'] +  appendfinal2['Cumulative Profit Payment/Interest Repayment (MYR)'] 

  appendfinal2.sort_values('Total Loans Outstanding (MYR)', ascending=False, inplace=True)#.reset_index()

  appendfinal3 = appendfinal2[['EXIM Account No.','Finance(SAP) Number',
                             'Customer Name',
                             'Facility Currency',
                             'Type of Financing',
                             'Cost/Principal Outstanding (Facility Currency)',
                             'Cost/Principal Outstanding (MYR)',
                             'Accrued Profit/Interest of the month (Facility Currency)',
                             'Accrued Profit/Interest of the month (MYR)',
                             'Modification of Loss (Facility Currency)',
                             'Modification of Loss (MYR)',
                            'Cumulative Accrued Profit/Interest (Facility Currency)',
                            'Cumulative Accrued Profit/Interest (MYR)', 
                             'Income/Interest in Suspense (Facility Currency)',
                             'Income/Interest in Suspense (MYR)',
                             'Other Charges (Facility Currency)',
                             'Other Charges (MYR)',
                             "Ta`widh Payment/Penalty Repayment (Facility Currency)",
                             "Ta`widh Payment/Penalty Repayment (MYR)",
                             "Ta'widh (Compensation) (Facility Currency)",
                             "Ta'widh (Compensation) (MYR)",
                             'Total Loans Outstanding (Facility Currency)',
                             'Total Loans Outstanding (MYR)',
                            #'Disbursement/Drawdown (Facility Currency)',
                            #'Disbursement/Drawdown (MYR)',
                             #'Cumulative Disbursement/Drawdown (Facility Currency) New',
                             #'Cumulative Disbursement/Drawdown (Facility Currency)',
                             #'Cumulative Disbursement/Drawdown (MYR) New',
                             #'Cumulative Disbursement/Drawdown (MYR)',
                            #'Cost Payment/Principal Repayment (Facility Currency)',
                            #'Cost Payment/Principal Repayment (MYR)',
                             #'Cumulative Cost Payment/Principal Repayment (Facility Currency) New',
                             #'Cumulative Cost Payment/Principal Repayment (Facility Currency)',
                             #'Cumulative Cost Payment/Principal Repayment (MYR) New',
                             #'Cumulative Cost Payment/Principal Repayment (MYR)',
                            #'Profit Payment/Interest Repayment (Facility Currency)',
                            #'Profit Payment/Interest Repayment (MYR)',
                             #'Cumulative Profit Payment/Interest Repayment (Facility Currency) New',
                             #'Cumulative Profit Payment/Interest Repayment (Facility Currency)',
                             #'Cumulative Profit Payment/Interest Repayment (MYR) New',
                             #'Cumulative Profit Payment/Interest Repayment (MYR)',
                             'Curr']]

  appendfinal3['Cost/Principal Outstanding (Facility Currency)'].fillna(0,inplace=True)
  appendfinal3['Cost/Principal Outstanding (MYR)'].fillna(0,inplace=True)
  appendfinal3['Accrued Profit/Interest of the month (Facility Currency)'].fillna(0,inplace=True)
  appendfinal3['Accrued Profit/Interest of the month (MYR)'].fillna(0,inplace=True)
  appendfinal3['Modification of Loss (Facility Currency)'].fillna(0,inplace=True)
  appendfinal3['Modification of Loss (MYR)'].fillna(0,inplace=True)
  appendfinal3['Cumulative Accrued Profit/Interest (Facility Currency)'].fillna(0,inplace=True)
  appendfinal3['Cumulative Accrued Profit/Interest (MYR)'].fillna(0,inplace=True)
  appendfinal3['Income/Interest in Suspense (Facility Currency)'].fillna(0,inplace=True)
  appendfinal3['Income/Interest in Suspense (MYR)'].fillna(0,inplace=True)
  appendfinal3['Other Charges (Facility Currency)'].fillna(0,inplace=True)
  appendfinal3['Other Charges (MYR)'].fillna(0,inplace=True)
  appendfinal3["Ta`widh Payment/Penalty Repayment (Facility Currency)"].fillna(0,inplace=True)
  appendfinal3["Ta`widh Payment/Penalty Repayment (MYR)"].fillna(0,inplace=True)
  appendfinal3["Ta'widh (Compensation) (Facility Currency)"].fillna(0,inplace=True)
  appendfinal3["Ta'widh (Compensation) (MYR)"].fillna(0,inplace=True)
  appendfinal3['Total Loans Outstanding (Facility Currency)'].fillna(0,inplace=True)
  appendfinal3['Total Loans Outstanding (MYR)'].fillna(0,inplace=True)


  
  #---------------------------------------------Download-------------------------------------------------------------


  st.write("Row Column Checking: ")
  st.write(appendfinal3.shape)

  #st.write("-------------------------------------------------------------------------------")
  #st.write(f"Sum Cost/Principal (FC) : ${float(sum(appendfinal3['Cost/Principal Outstanding (Facility Currency)']))}")
  st.write(f"Sum Cost/Principal (MYR) : RM{float(sum(appendfinal3['Cost/Principal Outstanding (MYR)']))}")
  st.write("")
  #st.write(f"Sum Total Loans Outstanding (FC) : ${float(sum(appendfinal3['Accrued Profit/Interest of the month (Facility Currency)']))}")
  st.write(f"Sum Total Loans Outstanding (MYR) : RM{float(sum(appendfinal3['Accrued Profit/Interest of the month (MYR)']))}")
  st.write("")
  #st.write(f"Sum Mora (FC) : ${float(sum(appendfinal3['Modification of Loss (Facility Currency)']))}")
  st.write(f"Sum Mora (MYR) : RM{float(sum(appendfinal3['Modification of Loss (MYR)']))}")
  st.write("")
  #st.write(f"Sum Cumulative Accrued (FC) : ${float(sum(appendfinal3['Cumulative Accrued Profit/Interest (Facility Currency)']))}")
  st.write(f"Sum Cumulative Accrued (MYR) : RM{float(sum(appendfinal3['Cumulative Accrued Profit/Interest (MYR)']))}") 
  st.write("")
  #st.write(f"Sum IIS (FC) : ${float(sum(appendfinal3['Income/Interest in Suspense (Facility Currency)']))}")
  st.write(f"Sum IIS (MYR) : RM{float(sum(appendfinal3['Income/Interest in Suspense (MYR)']))}")
  st.write("")
  #st.write(f"Sum Other Charges (FC) : ${float(sum(appendfinal3['Other Charges (Facility Currency)']))}")
  st.write(f"Sum Other Charges (MYR) : RM{float(sum(appendfinal3['Other Charges (MYR)']))}")
  st.write("")
  #st.write(f"Sum Total Loans Outstanding (FC) : ${float(sum(appendfinal3['Total Loans Outstanding (Facility Currency)']))}")
  total_Penal = sum(appendfinal3["Ta`widh Payment/Penalty Repayment (MYR)"])
  st.write(f"Sum Tawidh Penalty (MYR) : RM{float(total_Penal)}")
  st.write("")
  #st.write(f"Sum Total Loans Outstanding (FC) : ${float(sum(appendfinal3['Total Loans Outstanding (Facility Currency)']))}")
  total_Penal_R = sum(appendfinal3["Ta'widh (Compensation) (MYR)"])
  st.write(f"Sum Tawidh Recovery (MYR) : RM{float(total_Penal_R)}")
  st.write("")
  #st.write(f"Sum Total Loans Outstanding (FC) : ${float(sum(appendfinal3['Total Loans Outstanding (Facility Currency)']))}")
  st.write(f"Sum Total Loans Outstanding (MYR) : RM{float(sum(appendfinal3['Total Loans Outstanding (MYR)']))}")
  st.write("")
     


  #st.write('Sum Total Loans Outstanding (MYR) : RM'+str(sum))

           
  #st.write("SAP Duplication Checking: ")
  #st.write(appendfinal3['Finance(SAP) Number'].value_counts())

  st.write(appendfinal3)
  
  st.write("")
  st.write("Download file: ")
  st.download_button("Download CSV",
                   appendfinal3.to_csv(index=False),
                   file_name='01. Debtor Listing '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')

  #st.write("Account duplication checking: ")
  #st.write(appendfinal3["EXIM Account No."].value_counts())

#chart  
#https://www.youtube.com/watch?app=desktop&v=DFMh6liDRtk

  #fig = px.scatter(df,
  #x = 'casual', #leh try repayment
  #y = 'windspeed', #leh try disbursement
  #color = 'season')

  #fig.update_layout(title="X vs Y",
  #width=1000,
  #height=500,
  #xaxis_title="casual x",
  #yaxus_title="y windspped",
  #template="simple_white")

  #fig.show()



  #fig = px.bar(bar_data, x="month", y="count")
  #fig.update_layout(bargap=0.0075,
  #title="bike by month",
  #width=1000,
  #height=500,
  #xaxis_title="month",
  #yaxis_title="bike",
  #template="simple_white",
  #hoverlabel=dict(bgcolor="white",font_size12,font_family="Arial"))

  #fig.update_traces(marker_color="#AAAAAA") #hex code for silver
  #fig.show()


# https://github.com/analyticswithadam/Python/blob/main/Introduction_to_Plotly_Express.ipynb
# Histogram 
# https://plotly.com/python/builtin-colorscales/

#average = df['cnt'].mean()
#fig = px.histogram(df, x = 'cnt',color='season', color_discrete_sequence=px.colors.qualitative.Dark24)

#fig.update_layout(
#    bargap = 0.005, 
#    title = 'Rentals',
#    width = 1000,
#    height = 500,
#    xaxis_title = 'Count of Bike Rentals',
#    yaxis_title = 'Count of Days',
#    template="simple_white")

#fig.add_shape(type="circle",
#    xref="x", yref="y",
#    fillcolor="PaleTurquoise",
#    x0=3500, y0=70, x1=5500, y1=90,
#    line_color="LightSeaGreen",
#)

#fig.add_annotation(x=4500, y=91,
#            text="Highest Frequency @ Approx 4500",
#            showarrow=True,
#            arrowhead=4)

#fig.show()



#avg = df['cnt'].mean()
#time = df['dteday'].min()

#fig = px.line(df, x = 'dteday',y='cnt')

#fig.update_layout(
#    title = 'Bike Rentals 2011 / 2012',
#    width = 1000,
#    height = 500,
#    xaxis_title = 'Count of Bike Rentals',
#    yaxis_title = 'Date',
#    template="simple_white")

#fig['data'][0]['line']['color']='#AAAAAA'

#fig.add_shape( # add a horizontal "target" line
#    type="line", line_color="black", line_width=3, opacity=1, line_dash="dot",
#    x0=0, x1=1, xref="paper", y0=avg, y1=avg, yref="y"
#)

#fig.add_annotation(x=time, y=avg,
#            text="Average Rentals",
#            showarrow=False,
#            arrowhead=4,
#            xshift = 70,
#            yshift = 10)


#fig.show()



#multiple line

#fig = px.line(df, x = 'dteday',y=['casual','registered'])

#fig['data'][0]['line']['color']="#F2CC8F"
#fig['data'][1]['line']['color']="#033F63"

#fig.update_layout(
#    title = 'Casual & Registered Bike Rentals 2011 / 2012',
#    width = 1000,
#    height = 500,
#    xaxis_title = 'Count of Bike Rentals',
#    yaxis_title = 'Date',
#    template="simple_white")
#fig.show()
     


 #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
#  query = st.text_input("Filter dataframe in lowercase")

#fill in the blank

#  if query:
#    mask = LDB2.applymap(lambda x: query in str(x).lower()).any(axis=1)
#    LDB2 = LDB2[mask]

#  st.data_editor(
#    LDB2,
#    hide_index=True, 
#    column_order=LDB2#("Customer Name","Status","Amount Approved / Facility Limit (MYR)")
#  ) 

 #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

 #drop down

  #filter = st.selectbox('Select Status', options=LDB2["Status"].unique())
  #filtered_df = LDB2[LDB2["Status"]==filter]
  #st.dataframe(filtered_df)