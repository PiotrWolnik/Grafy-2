#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import graphs_2
from graphs_2 import *


class TestMinRoute(unittest.TestCase):
    def test_find_min_trail(self):
        g = load_multigraph_from_file('graphs.dat')
        trail_list = find_min_trail(g, 1, 3)
        weight = 0
        for i in range(len(trail_list)):
            weight += trail_list[i].edge_weight
        self.assertEqual(weight, nx.dijkstra_path_length(g, source=1, target=3))


if __name__ == '__main__':
    unittest.main()
