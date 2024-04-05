import sys
import os
from pathlib import Path

if (dir := str(Path(os.getcwd()))) not in sys.path:
    sys.path.insert(0, dir)
    
    
import streamlit as st
from streamlit_option_menu import option_menu
from src.app.functions.algorithm_description.algorithm_description import algorithm_description
from src.app.functions.tsp_solve.tsp_solve import tsp_solve


IoC = {
    "app":
    {
        "Описание алгоритмов": algorithm_description,
        "Задача коммивояжера": tsp_solve,
    }
}

with st.sidebar:
    selected = option_menu("Меню", ["Описание алгоритмов", 'Задача коммивояжера'],
                           icons=['info-circle', 'buildings'], menu_icon="cast", default_index=0)


IoC["app"][selected]()
