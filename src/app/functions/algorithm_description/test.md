# Алгоритмы эволюционной оптимизации

## Решение задачи коммивояжера при помощи алгоритма светлячков

![](../../assets/firefly.png)

Решение задачи коммивояжера является одной из классических задач комбинаторной оптимизации. Она заключается в поиске оптимального пути, проходящего через все заданные города, с минимальной суммарной длиной.

Один из алгоритмов, используемых для решения этой задачи, называется алгоритмом светлячков. Он основан на моделировании поведения светлячков в природе и их способности усваивать свет, который производят особи.

Алгоритм светлячков является эвристическим методом и может давать приближенное решение задачи коммивояжера. Его эффективность зависит от выбора параметров и настройки алгоритма.

Для данной задачи было использовано порядковое представление Гамильтонова цикла. В качестве функции скрещивания было взято одноточечное. Мутация особи производится путем оценки допустимого изменения гена (которое не противоречит порядковому представлению).

Поскольку задача коммивояжера - задача дискретной комбинаторной оптимизации, а светлячковый алгоритм первоначально был создан для решения непрерывных задач оптимизации, были внесены модификации, чтобы применить его к данной задачи.

Вместо шага используется скрещивание, что позволяет обмениваться информацией о маршрутах, также применяется мутация, чтобы не оставаться в локальном оптимуме. 

На вход алгоритм принимает следующие параметры:

1. $N$ - число городов (число вершин графа);
2. *adjacency_matrix* - матрица весов (матрица смежности с весами);
3. $\gamma \in (0, 1)$ - уровень значимости привлекательности света для светлячков (если $\gamma \rightarrow 0$, то светлячки со схожей яркостью не будут обращать друг на друга внимание, если $\gamma \rightarrow 1$, то светлячки со схожей яркостью будут всегда обращать друг на друга внимание). Это дискретный аналог коэффициента рассеивания света в среде из непрерывного определения алгоритма;
4. *population_size* - размер популяции светлячков;
5. *mutation_probability* $\in [0, 1]$ - вероятность мутации лучшей особи в паре;
6. *k_max* - максимальное число итераций алгоритма (эпох).