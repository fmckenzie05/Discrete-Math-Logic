import streamlit as st
import pandas as pd
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

st.title('Tree nodes visualizer')

# Sidebar
st.sidebar.markdown("## Select Number of Words")
# Load the dataset
file = 'data/words.csv'
df = pd.read_csv(file, header=None, names=['word'])

# Drop any rows with NaN values
df = df.dropna()

df['word'] = df['word'].str.strip('\"')  # Remove any surrounding quotes
df = df[df['word'].str.isalpha()] # Filter out non-alphabetic words

# Add a slider to allow users to select a subset of words from the dataset
num_words = st.sidebar.slider(
    "Number of words to visualize",
    min_value=100,
    max_value=len(df),
    value=1000,  # default value
    step=100
)

# Subset and shuffle the dataframe based on the slider
filtered_df = df.sample(frac=1, random_state=42).head(num_words)

st.sidebar.markdown(f"Selected {num_words} words from the dataset.")

st.sidebar.markdown("## Select Tree data structure")
tree_options = {
    'Trie': 1,
    'Ternary': 2,
    'Radix': 3
}
selected_trees = [tree for tree in tree_options if st.sidebar.checkbox(tree, value=False)]

st.sidebar.markdown("## Select a prefix")
st.sidebar.markdown("""Choose a prefix. Leave blank if you want to list all possible words""")
prefix = st.sidebar.text_input(label='Prefix', value='')

# Initialize the metrics dictionary outside of any conditional blocks
# Initialize dictionaries to store metrics and visualizations separately
metrics = {}
visualizations = {}

def run_analysis():
    """Function to run the analysis and store metrics."""
    for tree_key in selected_trees:
        tree_value = tree_options[tree_key]
        try:
            # Capture all the metrics from visualize function
            results, fig, nodes_traversed, total_nodes, insertion_time, retrieval_time = visualize(
                words=filtered_df.iloc[:, 0].tolist(), 
                tree_selection=tree_value, 
                prefix=prefix
            )

            # Store the metrics for this tree
            metrics[tree_key] = {
                'Insertion Time (ms)': insertion_time,
                'Retrieval Time (ms)': retrieval_time,
                'Total Nodes': total_nodes,
                'Nodes Traversed': nodes_traversed
            }

            # Display visualizations in the Visualize tab
            with tab_visualize:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"## {tree_key} data structure")
                    st.plotly_chart(fig)
                with col2:
                    st.markdown(f"## {tree_key} found words")
                    wordcloud_fig = create_wordcloud(results)

        except Exception as e:
            st.markdown(f"**Error with {tree_key}**: {str(e)}")



# Main screen
tab_visualize, tab_metrics = st.tabs(["Visualize", "Metrics"])

# Run button in the sidebar
if st.sidebar.button(label='Run', key='run_analysis'):
    run_analysis()

with tab_visualize:
    if visualizations:
        st.markdown("### Visualization Results")
        for tree_key in selected_trees:
            if tree_key in visualizations:
                results, fig = visualizations[tree_key]
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"## {tree_key} data structure")
                    st.plotly_chart(fig)
                with col2:
                    st.markdown(f"## {tree_key} found words")
                    create_wordcloud(results)

with tab_metrics:
    st.markdown("### Tree Metrics")
    if metrics:
        for tree_key, metric in metrics.items():
            st.markdown(f"#### {tree_key}")
            st.write(pd.DataFrame.from_dict(metric, orient='index', columns=[tree_key]))
    else:
        st.markdown("No metrics collected yet. Please click the 'Run' button.")
