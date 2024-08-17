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
st.set_page_config(page_title=apptitle, page_icon=":evergreen_tree:", layout="wide")

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

tree_options = {
    'Trie': 1,
    'Ternary': 2,
    'Radix': 3
}
selected_trees = [tree for tree in tree_options if st.sidebar.checkbox(tree, value=False)]
# tree_selections = [tree_options[tree] for tree in selected_trees]


#-- Set prefix
st.sidebar.markdown("## Select a prefix")
st.sidebar.markdown("""Choose a prefix. Leave blank if you want to list all possible words""")
prefix = st.sidebar.text_input(label='Prefix', value='') 


# Main screen
tab_visualize, tab_metrics = st.tabs(["Visualize", "Metrics"])

# Store tree metrics
tree_metrics = {}
with tab_visualize:
    if st.sidebar.button(label='Autocomplete and graph'):
        col1, col2 = st.columns(2)
        for tree_key in selected_trees:
            tree_value = tree_options[tree_key]
            try:
                results, fig = visualize(csv_file_path=file, tree_selection=tree_value, prefix=prefix)

                with col1:
                    st.markdown(f"## {tree_key} data structure")
                    st.plotly_chart(fig)
                with col2:
                    # Explicitly pass the figure objects
                    st.markdown(f"## {tree_key} found words")
                    wordcloud_fig = create_wordcloud(results)

            except Exception as e:
                st.markdown(f"**Error with {tree_key}**: {str(e)}")

# Show tree metrics
with tab_metrics:
    st.markdown("Hihi")






