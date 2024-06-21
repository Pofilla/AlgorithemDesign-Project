import tkinter as tk
from tkinter import messagebox, ttk
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.vertices = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def _dfs(self, start, visited):
        stack = [start]
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                for neighbor in self.graph[v]:
                    if not visited[neighbor]:
                        stack.append(neighbor)

    def is_one_way(self):
        for u in range(self.vertices):
            for v in range(self.vertices):
                if u != v:
                    visited = [False] * self.vertices

                    # Check if u can reach v
                    self._dfs(u, visited)
                    if not visited[v]:
                        # Check if v can reach u
                        visited = [False] * self.vertices
                        self._dfs(v, visited)
                        if not visited[u]:
                            return False
        return True
    
    def get_graph(self):
        return self.graph

# Global variable to store the graph
current_graph = None

def check_graph():
    global current_graph
    try:
        vertices = int(entry_vertices.get())
        edges_text = entry_edges.get("1.0", tk.END).strip()
        edges = []

        for line in edges_text.splitlines():
            u, v = map(int, line.split())
            edges.append((u, v))

        # Create the graph
        graph = Graph(vertices)
        for u, v in edges:
            graph.add_edge(u, v)
        
        current_graph = graph

        # Check if the graph is one-way
        if graph.is_one_way():
            messagebox.showinfo("Result", "The graph is one-way connected.")
        else:
            messagebox.showinfo("Result", "The graph is NOT one-way connected.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid input.")

def display_graph():
    global current_graph
    if current_graph:
        graph_data = current_graph.get_graph()
        
        # Create a networkx graph
        G = nx.DiGraph()
        for u in graph_data:
            for v in graph_data[u]:
                G.add_edge(u, v)
        
        # Plot the graph
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', arrows=True)
        
        # Embed the plot into Tkinter window
        graph_window = tk.Toplevel(root)
        graph_window.title("Graph Representation")
        
        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        # Close button
        ttk.Button(graph_window, text="Close", command=graph_window.destroy).pack()

# Create the main window
root = tk.Tk()
root.title("Graph One-Way Connectivity Checker")

# Vertices input
tk.Label(root, text="Number of vertices:").grid(row=0, column=0)
entry_vertices = tk.Entry(root)
entry_vertices.grid(row=0, column=1)

# Edges input
tk.Label(root, text="Edges (one per line, format: u v):").grid(row=1, column=0)
entry_edges = tk.Text(root, height=10, width=30)
entry_edges.grid(row=1, column=1)

# Check button
check_button = tk.Button(root, text="Check One-Way", command=check_graph)
check_button.grid(row=2, columnspan=2, pady=10)

# Display graph button
display_button = tk.Button(root, text="Display Graph", command=display_graph)
display_button.grid(row=3, columnspan=2, pady=10)

# Run the application
root.mainloop()
