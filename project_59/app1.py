import streamlit as st
#pip install streamlit
#import PyPDF2

import spacy

import pandas as pd

from PIL import Image

#from pdfminer.high_level import extract_text

import sys 
import os
sys.path.append(os.path.abspath("H:/vrenv/project 59/main file"))
from ext import *


st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://i.pinimg.com/originals/92/4f/3d/924f3d13746d6621acfbf1ed9c563462.jpg")
    }
    """,
    unsafe_allow_html=True
)


st.write(""" # Feature Extraction From Medical Journals """)


docx_file = st.file_uploader("Upload Document",type=['pdf','txt'])


df=Nerdata_Final()
    
    

st.write(df)
    
    
