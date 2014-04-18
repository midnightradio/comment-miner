import unittest
from html import HTML

class TestHTML(unittest.TestCase):
    def setUp(self):
        self.html = HTML('dont care')

    def test_get_comment_definitions(self):
        self.assertItemsEqual(self.html.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'<!--',
                    'endwith':r'-->',
                    'block':True } ])
        self.assertListEqual(self.html.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'<!--',
                    'endwith':r'-->',
                    'block':True } ])

