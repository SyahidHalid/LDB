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
    <h1>Non-Trade Ageing</h1>
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

D1 = form.text_input("Input Ageing Islamic Sheet ")

df1 = form.file_uploader(label= "Upload Latest Non Trade Islamic - Ageing:")
if df1:
  T1 = pd.read_excel(df1, sheet_name=D1, header=11)

D2 = form.text_input("Input Ageing OPF Sheet ")

df2 = form.file_uploader(label= "Upload Latest Non Trade OPF - Ageing:")
if df2:
  T2 = pd.read_excel(df2, sheet_name=D2, header=10)
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
  T1_1 = T1.iloc[np.where(~(T1['ACCOUNT NO:'].isna())&(T1['ACCOUNT NO:']!="ACCOUNT NO:"))].drop(["NO","Unnamed: 0","SIPP"],axis=1)
  T2_1 = T2.iloc[np.where(~(T2['ACCOUNT NO:'].isna())&(T2['ACCOUNT NO:']!="ACCOUNT NO:"))].drop(["NO","Unnamed: 0"],axis=1)

  T1_2 = T1_1.merge(T1[["ACCOUNT NO:","SIPP"]],on="ACCOUNT NO:",how="left")
  T2_1["SIPP"] = "NO"

  T1_2["File"] = "ISLAMIC"
  T2_1["File"] = "OPF"

  T1_2.columns=T2_1.columns

  COMBINE = pd.concat([T1_2,T2_1])
  st.write(COMBINE)
  
  #---------------------------------Download-------------------------------------------------------------

  #st.write("")
  #st.write("Row Column Checking: ")
  #st.write(T1_2.shape)
  
  #st.write("")
  #st.write(T2_1.shape)

  st.write("")
  st.write(COMBINE.shape)
    
  st.write("")
  st.write("Download file: ")
  st.download_button("Download CSV",
                   COMBINE.to_csv(index=False),
                   file_name='10. Ageing Non-Trade '+str(year)+"-"+str(month)+'.csv',
                   mime='text/csv')