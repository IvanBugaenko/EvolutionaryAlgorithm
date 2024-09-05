import streamlit as st
from src.algorithm.classes.Evolution import Evolution
from src.algorithm.functions.generate_field import generate_field
from src.algorithm.functions.draw import draw
from src.algorithm.functions.draw_fsm import draw_fsm

import numpy as np
import matplotlib.pyplot as plt


def ant_solve() -> None:
    N = 32
    F = 90

    field = generate_field(N, F)
    evolution = Evolution(field)

    n_state = st.number_input("Введите число состояний машины", min_value=2, value=7)
    epoch = st.number_input("Введите число эпох эволюции", min_value=1, value=100)
    population_size = st.number_input("Введите размер популяции", min_value=1, value=100)
    crossing_probability = st.number_input("Введите вероятность скрещивания", min_value=0., max_value=1., value=0.8)
    mutation_probability = st.number_input("Введите вероятность мутации", min_value=0., max_value=1., value=0.15)
    
    start = st.button("Начать вычисления")
    
    if start:
        fig, ax = plt.subplots()
        st.write('Исходное поле с едой')
        draw(field)
        st.pyplot(fig)

        best_fsm, history = evolution.get_answer(n_state, epoch, population_size, crossing_probability, mutation_probability)
        
        fig, ax = plt.subplots()
        st.write('Динамика изменения лучшей особи')
        plt.plot(history)
        st.pyplot(fig)

        fig, ax = plt.subplots()
        st.write('Траектория муравья')
        draw(best_fsm.env.field)
        st.pyplot(fig)

        st.write(f'Количество съеденной еды: {best_fsm.fitness}')

        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        st.write('Схема конечных автоматов')
        ax[0].set_title('Не видит еды')
        draw_fsm(best_fsm.fsm[:, :2], 'red', ax[0])
        ax[1].set_title('Видит еду')
        draw_fsm(best_fsm.fsm[:, 2:], 'blue', ax[1])
        st.pyplot(fig)

        st.balloons()
