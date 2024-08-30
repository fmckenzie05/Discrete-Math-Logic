import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from visualize import visualize
import concurrent.futures


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
def process_tree_visualization(tree_key, visualizations):
    if tree_key in visualizations:
        results, fig = visualizations[tree_key]
        return tree_key, results, fig
    return None
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

    # Initialize the metrics dictionary outside of any conditional blocks
    # Initialize dictionaries to store metrics and visualizations separately
    metrics = {}
    visualizations = {}


    # Main screen
    tab_visualize, tab_metrics = st.tabs(["Visualize", "Metrics"])

    # Run button in the sidebar
    if st.sidebar.button(label='Run', key='run_analysis'):
        run_analysis()

    with tab_visualize:
        if visualizations:
            st.markdown("### Visualization Results")

            # Run visualizations in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_tree_visualization, tree_key, visualizations) for tree_key in selected_trees]
                results_list = [future.result() for future in concurrent.futures.as_completed(futures)]

            # Display results
            for result in results_list:
                if result is not None:
                    tree_key, results, fig = result
                    col1, col2 = st.columns(2)
                    with st.container():
                        with col1:
                            st.markdown(f"## {tree_key} data structure")
                            st.plotly_chart(fig)
                        with col2:
                            st.markdown(f"## {tree_key} found words")
                            create_wordcloud(results)


    # Initialize the merged metrics dictionary
    merged_metrics = {
        'Insertion Time (ms)': [],
        'Retrieval Time (ms)': [],
        'Total Nodes': [],
        'Nodes Traversed': []
    }
    # Merge the values from the metrics dictionary
    tree_names = []
    for tree_key, metric in metrics.items():
        tree_names.append(tree_key)
        for key in merged_metrics.keys():
            merged_metrics[key].append(metric[key])


    with tab_metrics:
        st.markdown("### Tree Metrics")
        if metrics:
            col1, col2 = st.columns(2)
            with col1:
                for tree_key, metric in metrics.items():
                    st.markdown(f"#### {tree_key}")
                    st.write(pd.DataFrame.from_dict(metric, orient='index', columns=[tree_key]))
            with col2:
                st.markdown("### Metrics Comparison")

                for metric_key, values in merged_metrics.items():
                    fig, ax = plt.subplots(figsize=(10, 6))

                    ax.plot(tree_names, values, marker='o', label=metric_key)
                    ax.set_xlabel('Trees')

                    ax.set_ylabel('Values')
                    ax.set_title(f'Comparison of {metric_key}')
                    ax.legend()
                    ax.grid(True)


                    st.pyplot(fig)
        else:
            st.markdown("No metrics collected yet. Please click the 'Run' button.")
