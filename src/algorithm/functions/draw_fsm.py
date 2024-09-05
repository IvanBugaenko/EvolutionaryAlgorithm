import networkx as nx
import numpy as np


def draw_fsm(fsm: np.ndarray, font_color: str, ax) -> None:
    G = nx.MultiDiGraph(directed=True)
    G.add_nodes_from(np.arange(fsm.shape[0]))

    rule = dict()

    for i, (action, new_state) in enumerate(fsm):
        G.add_edge(i, new_state)
        rule[(i, new_state)] = action

    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, ax=ax)
    nx.draw_networkx_edge_labels(
        G, 
        pos,
        edge_labels=rule,
        font_color=font_color,
        ax=ax,
    )
