import unittest
from strscan import StringScanner

#http://ruby-doc.org/stdlib-1.9.2/libdoc/strscan/rdoc/StringScanner.html

class TestScanner(unittest.TestCase):
    def setUp(self):
        pass

    def test_construction(self):
        self.assertRaises(TypeError, StringScanner, 1)
        self.assertEquals(StringScanner('dont care').string, 'dont care')
        self.assertEquals(StringScanner().pos, 0)
        self.assertEquals(StringScanner().string, None)

        _ = StringScanner()
        self.assertRaises(TypeError, _.string, 1)
        _.string = 'dont care'
        self.assertEquals(_.string, 'dont care')
        self.assertEquals(_.pos, 0)

    def test_concat(self):
        source = "Fri Dec 12 1975 14:39"
        s = StringScanner(source)
        s.scan(r'Fri ')
        self.assertRaises(TypeError, s.concat, 1)
        #s += ' +1000 GMT'
        s.concat(' +1000 GMT')
        self.assertEquals(s.string, 'Fri Dec 12 1975 14:39 +1000 GMT')

    def test_skip(self):
        s = StringScanner('test string')
        self.assertEquals(s.skip(r'\w+'), 4)
        self.assertEquals(s.skip(r'\w+'), None)
        self.assertEquals(s.skip(r'\s+'), 1)
        self.assertEquals(s.skip(r'\w+'), 6)
        self.assertEquals(s.skip(r'.'), None)

    def test_skip_until(self):
        s = StringScanner("Fri Dec 12 1975 14:39")
        self.assertEquals(s.skip_until(r'12'), 10)

    def test_scan(self):
        source = 'This is an example string'
        s = StringScanner(source)
        self.assertFalse(s.eos())

        s.pos = len(source)
        self.assertTrue(s.eos())

        s.pos = 0
        self.assertEquals(s.scan(r'\w+'), 'This')
        self.assertIsNone(s.scan(r'\w+'))
        self.assertEquals(s.scan(r'\s+'), ' ')
        self.assertIsNone(s.scan(r'\s+'))
        self.assertEquals(s.scan(r'\w+'), 'is')
        self.assertFalse(s.eos())
        self.assertEquals(s.pos, 7)
        self.assertEquals(s.scan(r'\s+'), ' ')
        self.assertEquals(s.scan(r'\w+'), 'an')
        self.assertEquals(s.scan(r'\s+'), ' ')
        self.assertEquals(s.scan(r'\w+'), 'example')
        self.assertEquals(s.scan(r'\s+'), ' ')
        self.assertEquals(s.scan(r'\w+'), 'string')
        self.assertTrue(s.eos())
        self.assertIsNone(s.scan(r'\s+'))
        self.assertIsNone(s.scan(r'\w+'))

    def test_scan_until(self):
        s = StringScanner("Fri Dec 12 1975 14:39")
        self.assertEquals(s.scan_until(r'1'), "Fri Dec 1")
        self.assertEquals(s.pre_match, 'Fri Dec ')
        self.assertIsNone(s.scan_until(r'XYZ'))

    def test_pre_match_post_match_property(self):
        s = StringScanner('test string')
        self.assertEquals(s.scan(r'\w+'), 'test')
        self.assertEquals(s.scan(r'\s+'), ' ')
        self.assertEquals(s.pre_match, 'test')
        self.assertEquals(s.post_match, 'string')
