from app.functions.algorithm_description import algorithm_description
from app.functions.tsp_solve import tsp_solve


IoC = {
    "app":
    {
        "Описание алгоритмов": algorithm_description,
        "Задача коммивояжера": tsp_solve,
    }
}
