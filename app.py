# https://github.com/jkanner/streamlit-dataview/blob/master/app.py
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from visualize import visualize

def create_wordcloud(words):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(words))
    fig, ax = plt.subplots()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)

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
if file_event == '4000 most common English words':
    file = 'data/4000-most-common-english-words-csv.csv'
elif file_event == 'Custom upload':
    file = st.file_uploader("Upload your CSV file", type="csv")
    if file is None:
        st.sidebar.markdown("""File does not exist""")

st.sidebar.markdown("## Select Tree data structure")
#-- Set tree
# tree_event = st.sidebar.selectbox('Which tree do you want to test?',
#                                     ['Trie', 'Ternary', 'Radix'])   
# if tree_event == 'Trie':
#     tree_option = 1
# elif tree_event == 'Ternary':
#     tree_option = 2
# else:
#     tree_option = 3


#-- Set prefix
st.sidebar.markdown("## Select a prefix")
st.sidebar.markdown("""Choose a prefix. Leave blank if you want to list all possible words""")
prefix = st.sidebar.text_input(label='Prefix', value='') 

if st.sidebar.button(label='Autocomplete and graph'):
    
    try:
        st.markdown("## Trie data structure")
        trie_results, trie_fig = visualize(csv_file_path=file, tree_selection=1, prefix=prefix)
        st.plotly_chart(trie_fig)
        create_wordcloud(trie_results)
    except:
        st.markdown("""Trie error""")
    
    try:
        st.markdown("## Ternary data structure")
        ternary_results, ternary_fig = visualize(csv_file_path=file, tree_selection=2, prefix=prefix)
        st.plotly_chart(ternary_fig)
        create_wordcloud(ternary_results)

    except:
        st.markdown("""Ternary error""")

    try:
        st.markdown("## Trie data structure")
        radix_results, radix_fig = visualize(csv_file_path=file, tree_selection=3, prefix=prefix)
        st.plotly_chart(radix_fig)
        create_wordcloud(radix_results)
    except:
        st.markdown("""Radix error""")





