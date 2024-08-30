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

## Select files:
# file_options = ["4000 english common words", "400.000 english common words", "Upload a CSV file"]
file_options = ["4000 english common words", "400.000 english common words"]
choice = st.sidebar.selectbox("Choose a file option:", file_options)
df = None
# Handle the file choice
if choice == "4000 english common words":
    file = 'data/4000-most-common-english-words-csv.csv'
    df = pd.read_csv(file, header=None, names=['word'])
elif choice == "400.000 english common words":
    file = 'data/words.csv'
    df = pd.read_csv(file, header=None, names=['word'])
    df = df.dropna()
    df['word'] = df['word'].str.strip('\"')  # Remove any surrounding quotes
    df = df[df['word'].str.isalpha()] # Filter out non-alphabetic words
# elif choice == "Upload a CSV file":
#     # Allow the user to upload a file
#     uploaded_file = st.file_uploader("Upload your file", type="csv")
#     if uploaded_file is not None:
#         # Read and display the uploaded file
#         df = pd.read_csv(uploaded_file)
#         # Ensure the 'word' column exists and process it
#         if 'word' in df.columns:
#             df['word'] = df['word'].str.strip('\"')  # Remove any surrounding quotes
#             df = df[df['word'].str.isalpha()]  # Filter out non-alphabetic words
#             df = df['word']  # Keep only the 'word' column
#             df.reset_index()
#         else:
#             st.error("The uploaded file does not contain a 'word' column.")


## Select dataset
st.sidebar.markdown("## Select Number of Words")
        # Add a slider to allow users to select a subset of words from the dataset
num_words = 0
def run_analysis():
    """Function to run the analysis and store metrics."""
    merged_metrics = {
            'Insertion Time (ms)': [],
            'Retrieval Time (ms)': [],
            'Total Nodes': [],
            'Nodes Traversed': []
        }
    
    tree_names = []

    for tree_key in selected_trees:
        tree_value = tree_options[tree_key]
        try:
            # Capture all the metrics from visualize function
            results, fig, nodes_traversed, total_nodes, insertion_time, retrieval_time = visualize(
                words=filtered_df.iloc[:, 0].tolist(), 
                tree_selection=tree_value, 
                prefix=prefix
            )
            tree_names.append(tree_key)
            merged_metrics['Insertion Time (ms)'].append(insertion_time)
            merged_metrics['Retrieval Time (ms)'].append(retrieval_time)
            merged_metrics['Total Nodes'].append(total_nodes)
            merged_metrics['Nodes Traversed'].append(nodes_traversed)

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

    with tab_metrics:
        st.markdown("### Tree Metrics")
        if merged_metrics:
            metrics_df = pd.DataFrame(merged_metrics, index=tree_names).T
            col1, col2 = st.columns(2)
            with col1:
                st.write(metrics_df)
            with col2:
                st.markdown("### Metrics Comparison")

                for metric_key in metrics_df.index:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(metrics_df.columns, metrics_df.loc[metric_key], marker='o', label=metric_key)
                    ax.set_xlabel('Trees')
                    ax.set_ylabel('Values')
                    ax.set_title(f'Comparison of {metric_key}')
                    ax.legend()
                    ax.grid(True)
                    st.pyplot(fig)
        else:
            st.markdown("No metrics collected yet. Please click the 'Run' button.")


if df is not None:
    st.write("Displaying File:")
    st.dataframe(df)
    num_words = st.sidebar.slider(
        "Number of words to visualize",
        min_value=100,
        max_value=len(df),
        value=1000,  # default value
        step=100
    )

    df.head()

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


    # Main screen
    tab_visualize, tab_metrics = st.tabs(["Visualize", "Metrics"])

    # Run button in the sidebar
    if st.sidebar.button(label='Run', key='run_analysis'):
        run_analysis()
  
