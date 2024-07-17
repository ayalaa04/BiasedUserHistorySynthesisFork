import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Define the MovielensInteractionGraph class
class MovielensInteractionGraph:
    def __init__(self, user_data, item_data, edges):
        self.user_data = user_data
        self.item_data = item_data
        self.edges = edges
        self.all_edges = set(edges)

# Function to visualize the interaction graph
def visualize_interaction_graph(igraph):
    G = nx.Graph()

    # Add edges from the interaction graph
    for edge in igraph.all_edges:
        user_id, item_id = edge
        G.add_edge(f"user_{user_id}", f"item_{item_id}")

    # Draw the graph
    pos = nx.spring_layout(G)  # Positioning the nodes using Fruchterman-Reingold force-directed algorithm
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=8, font_weight='bold')
    plt.title("User-Item Interaction Graph")
    plt.show()

# Load the data (replace these file paths with the actual paths to your data)
users_file_path = 'DATASET/ml-1m/users.dat'
ratings_file_path = 'DATASET/ml-1m/ratings.dat'
movies_file_path = 'DATASET/ml-1m/movies.dat'

# Read the data into DataFrames with the correct encoding
users_df = pd.read_csv(users_file_path, sep='::', engine='python', names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], encoding='ISO-8859-1')
ratings_df = pd.read_csv(ratings_file_path, sep='::', engine='python', names=['UserID', 'MovieID', 'Rating', 'Timestamp'], encoding='ISO-8859-1')
movies_df = pd.read_csv(movies_file_path, sep='::', engine='python', names=['MovieID', 'Title', 'Genres'], encoding='ISO-8859-1')

# Convert DataFrames to the required format
user_data = users_df.set_index('UserID').to_dict('index')
item_data = movies_df.set_index('MovieID').to_dict('index')
edges = [tuple(x) for x in ratings_df[['UserID', 'MovieID']].to_numpy()]

# Create the interaction graph
igraph = MovielensInteractionGraph(user_data, item_data, edges)

# Visualize the graph
visualize_interaction_graph(igraph)