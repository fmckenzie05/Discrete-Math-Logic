# https://github.com/jkanner/streamlit-dataview/blob/master/app.py
import streamlit as st
import requests, os, tempfile
from visualize import visualize

# -- Set page config
apptitle = 'Tree visualizer'

st.set_page_config(page_title=apptitle, page_icon=":evergreen_tree:")

# -- Default detector list
detectorlist = ['H1','L1', 'V1']

st.title('Tree nodes visualizer')

# Main screen
# st.markdown("""
# """)


# Side bar
st.sidebar.markdown("## Select Data File")
#-- Set data file
file_event = st.sidebar.selectbox('Which data file do you want to test?',
                                    ['4000 most common English words', 'Custom upload'])
file = 'data/4000-most-common-english-words-csv.csv'
if file_event == '4000 most common English words':
    # -- Set the prefix:        
    

    st.sidebar.markdown("""Leave blank if you want to list all possible words""")
elif file_event == 'Custom upload':
    file = st.file_uploader("Upload your CSV file", type="csv")
    if file is None:
        st.sidebar.markdown("""File does not exist""")

st.sidebar.markdown("## Select Tree data structure")
#-- Set tree
tree_event = st.sidebar.selectbox('Which tree do you want to test?',
                                    ['Trie', 'Ternary', 'Radix'])   
if tree_event == 'Trie':
    tree_option = 1
elif tree_event == 'Ternary':
    tree_option = 2
else:
    tree_option = 1  


#-- Set prefix
prefix = st.sidebar.text_input('Choose a prefix', '')    


