import matplotlib.pyplot as plt
import numpy as np


def draw(field: np.ndarray) -> None:
    colors = {
        0: (255, 255, 255), # клетка поля
        1: (0, 255, 0), # несъеденная еда
        2: (127, 127, 127), # траектория муравья по полю
        3: (0, 0, 0), # траектория муравья по полю, где была съедена еда
    }

    h, w = field.shape
    image = np.zeros((h, w, 3))

    mask0 = field == 0
    image[mask0] = colors[0]

    mask1 = field == 1
    image[mask1] = colors[1]
    
    mask2 = field == 2
    image[mask2] = colors[2]
    
    mask3 = field == 3
    image[mask3] = colors[3]

    plt.imshow(image.astype(int))
    