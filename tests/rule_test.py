import unittest
import numpy as np
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class RuleTest(unittest.TestCase):

    def _convert_to_matrix(self, filename):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
        content = content.replace('{{', '')
        content = content.replace('}}', '')
        content = content.replace('{', '')
        content = content.replace('},', ';')
        return np.matrix(content, dtype=np.int)

    def _convert_to_matrix2d(self, filename):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
            content = content.replace('{{{', '')
        content = content.replace('}}}', '')
        content = content.replace('{{', '')
        content = content.replace('{', '')
        content = [x.split('},') for x in content.split('}},')]
        content = [[h.split(',') for h in x] for x in content]
        content = [[[int(i) for i in h] for h in x] for x in content]
        return np.array(content, dtype=np.int)
