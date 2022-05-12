#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Set, Dict, NamedTuple
from enum import Enum
from typing import List
import networkx as nx


# Pomocnicza definicja podpowiedzi typu reprezentującego etykietę
# wierzchołka (liczba 1..n).
VertexID = int

# Pomocnicza definicja podpowiedzi typu reprezentującego listę sąsiedztwa.
AdjList = Dict[VertexID, List[VertexID]]

Distance = int
EdgeID = int


def neighbors(adjlist: AdjList, start_vertex_id: VertexID,
              max_distance: Distance) -> Set[VertexID]:

    return_set = list()
    color = dict()

    class NeighbourTuple(NamedTuple):
        vertex_id: VertexID
        distance: Distance

    class Color(Enum):
        BIALY = "BIALY"
        SZARY = "SZARY"
        CZARNY = "CZARNY"

    for u in adjlist:
        color[u] = Color.BIALY
        for v in adjlist[u]:
            color[v] = Color.BIALY
    color[start_vertex_id] = Color.SZARY
    Q = [NeighbourTuple(start_vertex_id, 0)]
    while Q:
        u = Q.pop(0)
        if u[1] > max_distance:
            break
        if u[0] != start_vertex_id:
            return_set.append(u[0])
        if u[0] != start_vertex_id:
            return_set.append(u[0])
        if u[0] in adjlist:
            for v in adjlist[u[0]]:
                if color[v] == Color.BIALY:
                    color[v] = Color.SZARY
                    Q.extend([NeighbourTuple(v, u[1]+1)])
            color[u[0]] = Color.CZARNY

    return {i for i in return_set}


# Nazwana krotka reprezentująca segment ścieżki.
class TrailSegmentEntry:
    def __init__(self, begining_vertex: VertexID, ending_vertex: VertexID, edge_id: EdgeID, egde_weight: float):
        self.begining_vertex = begining_vertex
        self.ending_vertex = ending_vertex
        self.edge_id = edge_id
        self.edge_weight = egde_weight


Trail = List[TrailSegmentEntry]


def load_multigraph_from_file(filepath: str) -> nx.MultiDiGraph:
    """Stwórz multigraf na podstawie danych o krawędziach wczytanych z pliku.

    :param filepath: względna ścieżka do pliku (wraz z rozszerzeniem)
    :return: multigraf
    """
    G = nx.MultiDiGraph()
    with open(filepath) as f:
        text = []
        for line in f:
            if line == '\n':
                continue
            new_line = str.strip(line)
            words = str.split(new_line, " ")
            text.extend(words)
    nodes_weights = []
    for i in range(len(text)):
        if not text[i]:
            continue
        if text[i].find(".") != -1:
            nodes_weights.append(float(text[i]))
        else:
            nodes_weights.append(int(text[i]))
    list_of_edges = []
    cursor = str()
    for i in nodes_weights:
        if type(i) != float:
            G.add_node(i)
            list_of_edges.append(i)
        else:
            a, *arg = list_of_edges
            G.add_edge(a, *arg, weight=i)
            list_of_edges.clear()
    return G


def find_min_trail(g: nx.MultiDiGraph, v_start: VertexID, v_end: VertexID) -> Trail:
    """Znajdź najkrótszą ścieżkę w grafie pomiędzy zadanymi wierzchołkami.

    :param g: graf
    :param v_start: wierzchołek początkowy
    :param v_end: wierzchołek końcowy
    :return: najkrótsza ścieżka
    """
    path = nx.dijkstra_path(g, source=v_start, target=v_end)
    trail_list = []
    for key_1, value_1 in g.adj.items():
        for key_2, value_2 in value_1.items():
            for key_3, value_3 in value_2.items():
                index_2: int = 0
                if key_1 in path and key_2 in path:
                    if len(trail_list) != 0:
                        if key_1 == trail_list[index_2 - 1].ending_vertex:
                            trail_list.append(TrailSegmentEntry(key_1, key_2, key_3, value_3['weight']))
                        elif key_1 == trail_list[index_2 - 1].begining_vertex and \
                                key_2 == trail_list[index_2 - 1].ending_vertex:
                            if value_3['weight'] < trail_list[index_2 - 1].edge_weight:
                                trail_list[index_2 - 1] = TrailSegmentEntry(key_1, key_2, key_3, value_3['weight'])
                    else:
                        trail_list.append(TrailSegmentEntry(key_1, key_2, key_3, value_3['weight']))
                    index_2 += 1
    return trail_list


def trail_to_str(trail: Trail) -> str:
    string = str()
    path_sum: float = 0.0
    for index in range(len(trail)):
        path_sum += trail[index].edge_weight
        if len(trail) == 1:
            string += f"{trail[index].begining_vertex} -[{trail[index].edge_id}:" \
                      f" {trail[index].edge_weight}]-> {trail[index - 1].ending_vertex}  (total = {path_sum})"
        else:
            if index < len(trail):
                string += f"{trail[index].begining_vertex} -[{trail[index].edge_id}:" \
                          f" {trail[index].edge_weight}]-> "
            if index == len(trail)-1:
                string += f"{trail[index].ending_vertex}  (total = " \
                          f"{path_sum})"
    return string
