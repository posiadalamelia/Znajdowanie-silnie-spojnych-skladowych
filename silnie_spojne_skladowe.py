import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

scc_result = None
class Graph:
    def __init__(self):
        self.graph = {}
        self.visited = {}
        self.prev = {}
        self.previst = {}
        self.postvisit = {}
        self.time = 0
        self.cc = 0
        self.ccnum = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.graph and vertex2 in self.graph:
            if vertex2 not in self.graph[vertex1]:
                self.graph[vertex1].append(vertex2)

    def create_default_graph(self):
        g.add_vertex('A')
        g.add_vertex('B')
        g.add_vertex('C')
        g.add_vertex('D')
        g.add_vertex('E')
        g.add_vertex('F')
        g.add_vertex('G')
        g.add_vertex('H')
        g.add_vertex('I')
        g.add_vertex('J')
        g.add_vertex('K')
        g.add_vertex('L')

        # dodawanie krawędzi
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        g.add_edge('B', 'D')
        g.add_edge('B', 'E')
        g.add_edge('C', 'F')
        g.add_edge('E', 'B')
        g.add_edge('E', 'F')
        g.add_edge('E', 'G')
        g.add_edge('F', 'C')
        g.add_edge('F', 'H')
        g.add_edge('G', 'H')
        g.add_edge('G', 'J')
        g.add_edge('H', 'K')
        g.add_edge('I', 'G')
        g.add_edge('J', 'I')
        g.add_edge('K', 'L')
        g.add_edge('L', 'J')

    def display_graph(self):
        for vertex in sorted(self.graph.keys()):
            print(f"{vertex}: {', '.join(sorted(self.graph[vertex]))}")

    def dfs(self, v_list=None):
        if v_list is None:
            v_list = self.graph
        for vertex in v_list:
            self.visited[vertex] = False
            self.prev[vertex] = None
            self.time = 1

        for vertex in v_list:
            if not self.visited[vertex]:
                self.dfs_visit(vertex)
                self.cc += 1

    def dfs_visit(self, vertex):
        self.visited[vertex] = True
        self.ccnum[vertex] = self.cc
        self.previst[vertex] = self.time
        self.time += 1
        for v in self.graph[vertex]:
            if not self.visited[v]:
                self.prev[v] = vertex
                self.dfs_visit(v)
                self.ccnum[v] = self.cc
        self.postvisit[vertex] = self.time
        self.time += 1

    def reverse_edges(self):
        reversed_graph = Graph()
        for vertex in self.graph.keys(): reversed_graph.add_vertex(vertex)
        for vertex in self.graph.keys():
            for neighbor in self.graph.get(vertex, []):
                reversed_graph.add_edge(neighbor, vertex)  # Odwrócenie kierunków krawędzi
        return reversed_graph

    def find_strongly_connected_components(self):
        reversed_graph = self.reverse_edges()
        reversed_graph.dfs()
        # print(reversed_graph.postvisit) -- tu jest dobrze
        verticles_in_postvisit_decreasing_order = {key: reversed_graph.postvisit[key] for key in reversed(reversed_graph.postvisit)}
        self.dfs(verticles_in_postvisit_decreasing_order)
        return self.display_scc2()
        #self.draw_graph()
        #self.draw_meta_graph()

    def display_scc(self):
        for key, value in self.ccnum.items():
            print(key, "należy do silnie spójnej składowej nr:", value)

    def display_scc2(self):
        # Tworzymy słownik, w którym kluczami są numery silnie spójnych składowych,
        # a wartościami listy wierzchołków należących do danej składowej
        scc_vertices = {}
        scc_result=""
        for vertex, cc_num in self.ccnum.items():
            if cc_num not in scc_vertices:
                scc_vertices[cc_num] = [vertex]
            else:
                scc_vertices[cc_num].append(vertex)

        # Wyświetlamy silnie spójne składowe i wierzchołki należące do każdej z nich
        for cc_num, vertices in scc_vertices.items():
            scc_result+=f"Silnie spójna składowa nr {cc_num + 1}: {vertices}\n"
        return scc_result

    def draw_graph(self):
        G = nx.DiGraph()

        for vertex in self.graph.keys():
            G.add_node(vertex)

        for vertex, neighbors in self.graph.items():
            for neighbor in neighbors:
                G.add_edge(vertex, neighbor)

        # Rysujemy graf
        plt.clf()
        pos = nx.circular_layout(G)  # Definiujemy układ wierzchołków
        ax = plt.gca()
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=10,
                font_weight='bold')  # Rysujemy graf
        ax.set_title('Graf wejściowy')  # Dodajemy tytuł
        plt.show()  # Wyświetlamy rysunek

    def draw_meta_graph(graph):
        meta_graph = nx.DiGraph()  # Inicjalizacja obiektu metagrafu

        # Dodajemy węzły metgrafu, które reprezentują silnie spójne składowe
        scc_vertices = {}
        for vertex, cc_num in graph.ccnum.items():
            if cc_num not in scc_vertices:
                scc_vertices[cc_num] = [vertex]
            else:
                scc_vertices[cc_num].append(vertex)

        # Dodajemy wierzchołki metagrafu
        for cc_num, vertices in scc_vertices.items():
            meta_graph.add_node(cc_num + 1)

        # Dodajemy krawędzie między węzłami metagrafu, reprezentujące krawędzie między składowymi w grafie pierwotnym
        for vertex, neighbors in graph.graph.items():
            for neighbor in neighbors:
                cc_num1 = graph.ccnum[vertex]
                cc_num2 = graph.ccnum[neighbor]
                if cc_num1 != cc_num2:
                    meta_graph.add_edge(cc_num1 + 1, cc_num2 + 1)

        # Rysujemy metagraf
        plt.clf()
        pos = nx.circular_layout(meta_graph)  # Definiujemy układ wierzchołków
        ax = plt.gca()
        nx.draw(meta_graph, pos, with_labels=True, node_color='lightgreen', node_size=800, font_size=10,
                font_weight='bold', arrowsize=20)  # Rysujemy metagraf
        ax.set_title('Metagraf')  # Dodajemy tytuł
        plt.show()  # Wyświetlamy rysunek

g = Graph()


def gui_add_vertex():
    top = tk.Toplevel(root)
    top.title("Dodaj wierzchołki")
    top.geometry("500x700")
    top.configure(bg='#2e2e2e')

    windowNumber = ctk.CTkEntry(master=top, placeholder_text="wprowadź liczbę wierzchołków", width=250, height=2)
    windowNumber.grid(row =0, column =1, padx=10, pady=10)

    def ok():
        input_value = windowNumber.get()

        if input_value.isdigit():
            number = int(input_value)

            if number>0:
                windowNumber.destroy()
                button_OK.destroy()
                windowVertices = []

                for i in range (number):
                    windowVertex = ctk.CTkEntry(master=top, placeholder_text="wprowadź wierzchołek", width=150, height=2)
                    windowVertex.grid(row =i, column =0, padx=10, pady=10)
                    windowVertices.append(windowVertex)

                def dodaj_wierzcholki():
                    all_filled = True
                    unique_vertices = set()

                    for entry in windowVertices:
                        vertex = entry.get()
                        if not vertex:
                            all_filled = False
                            break
                        if vertex in unique_vertices:
                            messagebox.showerror("Błąd", f"Próba podania istniejących już wierzchołków")
                            return
                        unique_vertices.add(vertex)

                    if all_filled:
                        for entry in windowVertices:
                            vertex = entry.get()
                            g.add_vertex(vertex)

                        top.destroy()
                        button1.configure(state=tk.DISABLED)
                        button2.configure(state=tk.NORMAL)

                    else:
                        messagebox.showerror("Błąd", "Proszę wypełnić wszystkie pola")

                button_dodaj_wierzcholki = tk.Button(top, text="Dodaj wierzchołki", command=dodaj_wierzcholki)
                button_dodaj_wierzcholki.grid(row =number, column =0, padx=10, pady=10)
            else:
                messagebox.showerror("Błąd", "Podana liczba musi być większa od zera")
        else:
            messagebox.showerror("Błąd", "Wprowadź liczbę całkowitą")


    button_OK = tk.Button(top, text="OK", command=ok)
    button_OK.grid(row =0, column =2, padx=10, pady=10)
    button0.configure(state=tk.DISABLED)

def gui_add_edge():
    top = tk.Toplevel(root)
    top.title("Dodaj krawędzie")
    top.geometry("700x700")
    top.configure(bg='#2e2e2e')

    windowNumber = ctk.CTkEntry(master=top, placeholder_text="wprowadź liczbę krawedzi", width=250,height=2)
    windowNumber.grid(row=0, column=1, padx=10, pady=10)

    def ok():
        input_value = windowNumber.get()

        if input_value.isdigit():
            number = int(input_value)

            if number>0:
                windowNumber.destroy()
                button_OK.destroy()
                windowEdges = []

                for i in range(number):
                        windowdInputVertex = ctk.CTkEntry(master=top, placeholder_text="z wierzchołka", width=150,height=2)
                        windowOutputVertex = ctk.CTkEntry(master=top, placeholder_text="do wierzchołka", width=150,height=2)
                        windowdInputVertex.grid(row=i, column=0, padx=10, pady=10)
                        windowOutputVertex.grid(row=i, column=1, padx=10, pady=10)
                        windowEdges.append(windowdInputVertex)
                        windowEdges.append(windowOutputVertex)

                def dodaj_krawedzie():
                    all_filled = True
                    unique_edges = set()

                    for i in range(0,len(windowEdges), 2):
                        if i+1<len(windowEdges):
                            Input = windowEdges[i].get()
                            Output = windowEdges[i+1].get()

                            if not Input or not Output:
                                all_filled = False
                                break

                            if Input not in g.graph or Output not in g.graph:
                                messagebox.showerror("Błąd", "Próba połączenia nieistniejących wierzchołków")
                                return

                            edge = (Input, Output)
                            if edge in unique_edges:
                                messagebox.showerror("Błąd", "Próba podania istniejących już krawędzi")
                                return
                            unique_edges.add(edge)

                    if all_filled:
                        for i in range(0, len(windowEdges), 2):
                            if i+1<len(windowEdges):
                                Input = windowEdges[i].get()
                                Output = windowEdges[i+1].get()
                                g.add_edge(Input, Output)
                        top.destroy()
                        button2.configure(state=tk.DISABLED)
                        button3.configure(state=tk.NORMAL)
                        button4.configure(state=tk.NORMAL)
                    else:
                        messagebox.showerror("Błąd", "Proszę wypełnić wszystkie pola")

                button_dodaj_krawedzie = tk.Button(top, text="Dodaj krawędzie", command=dodaj_krawedzie)
                button_dodaj_krawedzie.grid(row=i+1, column=0, padx=10, pady=10)
            else:
                messagebox.showerror("Błąd", "Podana liczba musi być większa od zera")

        else:
            messagebox.showerror("Błąd", "Wprowadź liczbę całkowitą")

    button_OK = tk.Button(top, text="OK", command=ok)
    button_OK.grid(row=0, column=2, padx=10, pady=10)

def gui_find_strongly_connected_components():
    global scc_result

    if scc_result is None:
        scc_result = g.find_strongly_connected_components()

    top = tk.Toplevel(root)
    top.title("Znajdź silnie spójne składowe")
    top.geometry("500x700")
    top.configure(bg='#2e2e2e')

    okno = tk.Text(top, height=300, width=1100, fg="#d1d1d1")
    okno.configure(bg='#2e2e2e')
    okno.pack()

    okno.insert(tk.END, scc_result)
    button5.configure(state=tk.NORMAL)

def gui_create_default_graph():
    g.create_default_graph()
    button1.configure(state=tk.DISABLED)
    button2.configure(state=tk.DISABLED)
    button3.configure(state=tk.NORMAL)
    button4.configure(state=tk.NORMAL)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("450x500")
root.title("Znajdowanie silnie spójnych składowych")

root.columnconfigure(0,weight=1)

button0 = ctk.CTkButton(root, text="Stwórz graf z domyślnych wartości", command=gui_create_default_graph)
button0.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

button1 = ctk.CTkButton(root, text="Dodaj wierzchołki grafu", command=gui_add_vertex)
button1.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

button2 = ctk.CTkButton(root, text="Dodaj krawędzie grafu", command=gui_add_edge)
button2.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
button2.configure(state=tk.DISABLED)

button3 = ctk.CTkButton(root, text="Wyświetl graf wejściowy", command=g.draw_graph)
button3.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
button3.configure(state=tk.DISABLED)

button4 = ctk.CTkButton(root, text="Znajdż silnie spójne składowe grafu", command=gui_find_strongly_connected_components)
button4.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
button4.configure(state=tk.DISABLED)

button5 = ctk.CTkButton(root, text="Wyświetl graf silnie spójnych składowych", command=g.draw_meta_graph)
button5.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
button5.configure(state=tk.DISABLED)

button6 = ctk.CTkButton(root, text="Zakończ", command=root.destroy)
button6.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="ew")


root.mainloop()