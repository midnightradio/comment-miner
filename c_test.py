import unittest

from c import C

class TestC(unittest.TestCase):
    def setUp(self):
        self.c = C('dont care')

    def test_get_comment_definitions(self):
        self.assertItemsEqual(self.c.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'/*',
                    'endwith':r'*/',
                    'block':True},
                  { 'type':'comment',
                    'startwith':r'//',
                    'block':False} ])
        self.assertListEqual(self.c.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'/*',
                    'endwith':r'*/',
                    'block':True},
                  { 'type':'comment',
                    'startwith':r'//',
                    'block':False} ])

