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
        return np.matrix(content, dtype=np.int).tolist()