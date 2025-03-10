# 🔍 Strongly Connected Components Finder  

## 📌 Project Overview  
This project implements an **interactive tool for finding strongly connected components (SCCs)** in a directed graph. It provides a **graphical user interface (GUI)** to create, modify, and visualize graphs while identifying their SCCs.  

## 🛠️ Features  
- **Add custom vertices and edges** to build a directed graph.  
- **Generate a default graph** for quick testing.  
- **Visualize the input graph** using **NetworkX** and **Matplotlib**.  
- **Compute and display SCCs** using depth-first search (DFS).  
- **Generate a meta-graph** to show relationships between SCCs.  

## 🔧 Technologies Used  
- **Python**  
- **NetworkX** for graph representation and visualization  
- **Matplotlib** for graphical output  
- **Tkinter & CustomTkinter** for GUI  

## 📊 How It Works  
1. **Graph Construction**  
   - Add vertices and edges manually via GUI  
   - Load a **predefined example graph**  

2. **Finding SCCs**  
   - **Reverse edges** of the graph  
   - Perform **DFS** on the reversed graph  
   - Sort nodes in **postorder** and perform **DFS again** on the original graph  

3. **Visualization**  
   - Display the **original graph**  
   - Compute **SCCs** and display them  
   - Generate and visualize the **meta-graph** of SCCs

## 🧑‍💻 Authors  
- [Amelia Posiadała](https://github.com/posiadalamelia)
- [Oliwia Strzelec](https://github.com/StrzelecO)
  
