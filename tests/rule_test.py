import os
import unittest
import ast

import networkx as nx
import numpy as np

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class RuleTest(unittest.TestCase):

    def _convert_to_matrix(self, filename, dtype=int):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
        content = content.replace('{{', '')
        content = content.replace('}}', '')
        content = content.replace('{', '')
        content = content.replace('},', ';')
        content = [[dtype(i) for i in x.split(',')] for x in content.split(';')]
        return np.array(content, dtype=np.int)

    def _convert_to_matrix2d(self, filename, dtype=int):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
            content = content.replace('{{{', '')
        content = content.replace('}}}', '')
        content = content.replace('{{', '')
        content = content.replace('{', '')
        content = [x.split('},') for x in content.split('}},')]
        content = [[h.split(',') for h in x] for x in content]
        content = [[[dtype(i) for i in h] for h in x] for x in content]
        return np.array(content, dtype=np.int)

    def _convert_to_list_of_lists(self, filename, strings=False, dtype=int):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
        content = content.replace('[[', '')
        content = content.replace(']]', '')
        content = content.replace('[', '')
        content = content.replace('],', ';')
        if strings:
            content = [[(None if i.strip() == "None" else i.strip()) for i in x.split(',')] for x in content.split(';')]
        else:
            content = [[dtype(i) for i in x.split(',')] for x in content.split(';')]
        return content

    def _convert_to_list_of_list_of_lists(self, filename, dtype=int):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
            content = content.replace('[[[', '')
        content = content.replace(']]]', '')
        content = content.replace('[[', '')
        content = content.replace('[', '')
        content = [x.split('],') for x in content.split(']],')]
        content = [[h.split(',') for h in x] for x in content]
        content = [[[dtype(i) for i in h] for h in x] for x in content]
        return content

    def _convert_from_literal(self, filename):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
            return ast.literal_eval(content)

    def _assert_networks_equal(self, g1, g2):
        def edge_match(e1, e2):
            self.assertEqual(e1, e2)
            return True

        def node_match(n1, n2):
            self.assertEqual(n1, n2)
            return True

        self.assertTrue(nx.is_isomorphic(g1, g2, edge_match=edge_match, node_match=node_match))
