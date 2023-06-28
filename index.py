import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import numpy as np
import cv2
import pandas as pd
import io 
from io import StringIO
import sys
import csv
import psycopg2
import subprocess
import time
import os
from os.path import exists
import pathlib
from pathlib import Path

# koneksi to database
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        return colnames, cur.fetchall()

## List Menu    
with st.sidebar:
    choose = option_menu("Main Menu", ["", "About", "Upload File", "Initial Process", "Report","post API"],
                         icons=['', 'house', 'cloud', 'chevron-double-right', 'newspaper',''],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "About":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Kelompok :</p>', unsafe_allow_html=True)
        st.write('')    
        st.subheader(f'\n \n Sukamto \n \n Arief Hidayat \n \n Dea Fesa \n \n Linda S. \n \n Fransiska A.W \n \n Emalia \n \n  Kristin Ross \n \n Nadia Putri \n')
    with col2:               # To display brand log
        st.write('')

## Menu untuk upload file data source
elif choose == "Upload File":
        # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Upload File</p>', unsafe_allow_html=True)
        st.write('')    

        ## clean Data
        #clean_data = st.button("Reset Data")
        #if clean_data:
        #    subprocess.run([f"{sys.executable}", "clean_data.py"])
        #    st.success(f'            >>>  Data Cleansing success.')

        # To display brand log
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            #st.write(bytes_data)
            
            dataframe = pd.read_csv(uploaded_file, encoding='latin-1')
            st.write(dataframe)
            btInput = st.button("upload file")
            if btInput:
                dt = pd.DataFrame(dataframe)
                dt.to_csv('D:\\dm\\data_input\\data_input.csv', index=True, encoding='latin-1')

                ## memanggil file insert_data.py
                subprocess.run([f"{sys.executable}", "insert_data.py"])
                st.success(f'            >>>  upload file success.')
                #conn.close()

## Menu proses
elif choose == "Initial Process":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Proses TextMining </p>', unsafe_allow_html=True)

    ## Menjalankan proses Text Mining
    showtable = st.button("Start Proceess")
    if showtable:
        ## Menjalankan file model_textmining
        subprocess.run([f"{sys.executable}", "model_textmining.py"])
        progress_text = "Operation in progress. Please wait."
        finish_text = "Operation progress."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1, text=finish_text)
        st.success('   Proses Selesai')

# Menu Data Report
elif choose == "Report":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Result Report</p>', unsafe_allow_html=True)
    st.subheader('-----------------------')

    dts = st.button("View DataSource")
    if dts:
   
    ##    names, rows = run_query("""
    ##        select * from public.tbl_dataset
    ##        """
    ##    )
    ##    st.write(pd.DataFrame(rows, columns=names))  
        try:
            dsource = pd.read_csv("D://dm//data_input//data_input.csv", encoding='latin-1')
            st.write(dsource) 
        except:
            st.error('maaf!!! data belum tersedia atau kesalahan format data')
        finally:
            st.write('')
    #Menampilkan data hasil proses Klasifikasi
    vkreport = st.button("view Klasifikasi Result")
    if vkreport:
        
    ##    st.write('Klasifikasi Result (1=ham, 0=spam)')
    ##    names, rows = run_query("""
    ##        select *
    ##            from tbl_klasifikasi_text 
    ##        """
    ##    )
    ##    st.write(pd.DataFrame(rows, columns=names))  
        try:
            klasi = pd.read_csv("D://dm//data_output//data_corpus.csv", encoding='latin-1')
            st.write(klasi) 
        except:
            st.error('maaf!!!.. data belum tersedia')
        finally:
            st.write('')
    #Menampilkan hasil model text Mining
    vReport = st.button("vReport Model")
    if vReport:
        try:
            data = pd.read_csv("D://dm//data_output//.akurasi_result.csv")
            data1 = pd.read_csv("D://dm//data_output//Gaus_rpt.csv")
            st.write(data)     
            st.write(data1)
        except:
            st.error('maaf!!!.. data belum tersedia')
        finally:
            st.write('')

# Menu Data Report
elif choose == "post API":
    try:
        subprocess.run([f"{sys.executable}", "api_ok.py"])
    except:
        st.write('terjadi kesalahan lainya')
    finally:
        st.write('')

conn.close()