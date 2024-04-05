import streamlit as st
from src.algorithm.classes.Environment import Environment
from src.algorithm.functions.get_graph import get_graph
from io import StringIO
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import plotly.express as px
import plotly.figure_factory as ff


def get_answer(N: int, adjacency_matrix: np.ndarray) -> None:
    gamma = st.number_input("Введите уровень значимости привлекательности света $\gamma$", min_value=0., max_value=1., value=0.8)
    population_size = st.number_input("Введите размер популяции", min_value=10, value=100)
    mutation_probability = gamma = st.number_input("Введите вероятность мутации особи", min_value=0., max_value=1., value=0.1)
    k_max = st.number_input("Введите число итераций алгоритма", min_value=10, value=100)
    
    env = Environment(N, adjacency_matrix, gamma)
    
    start = st.button("Начать вычисления")
    
    if start:
        best_fitness, best_route, history = env.get_answer(population_size, mutation_probability, k_max)
        st.write(f'Лучший вес маршрута: {best_fitness}')
        st.write(f'Лучший маршрут: {" → ".join(list(map(lambda x: str(x + 1), best_route)))}')
        
        G = nx.Graph()
        edges = []
        for i, j in combinations(range(N), 2):
            edges.append([i + 1, j + 1, adjacency_matrix[i][j]])
        
        G.add_weighted_edges_from(edges)
        
        way = nx.Graph()
        way_edge = [
            [best_route[i] + 1, best_route[i + 1] + 1] for i in range(len(best_route) - 1)
        ] + [[best_route[-1] + 1, best_route[0] + 1]]

        way.add_edges_from(way_edge)
        
        fig, ax = plt.subplots()
        
        nx.draw_circular(G, with_labels=True)
        nx.draw(way, with_labels=True, pos=nx.circular_layout(G), edge_color="red")
        st.pyplot(fig)
        
        st.write('График изменения веса маршрута')
        fig, ax = plt.subplots()
        plt.plot(list(map(lambda x: x[0], history)))
        st.pyplot(fig)
        
        st.balloons()
    
def upload_solve() -> None:
    uploaded_file = st.file_uploader("Выберите файл .txt (сначала идет число городов, затем указываются без разделителей ребра между вершинами и их вес):")

    if uploaded_file:
        string_io = StringIO(uploaded_file.getvalue().decode("utf-8"))
        N, adjacency_matrix = get_graph(list(string_io))
        st.write(f'Количество городов: {N}')
        
        get_answer(N, adjacency_matrix)
    
def input_solve() -> None:
    ...

def tsp_solve() -> None:
    tab1, tab2 = st.tabs(["Загрузка данных через файл", "Самостоятельный ввод данных"])

    with tab1:
        upload_solve()

    with tab2:
        input_solve()