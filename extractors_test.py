import unittest
from extractors import *
import sys

class TestExtractor(unittest.TestCase):
    class MixinExtractor(SlashStarExtractor, SlashSlashExtractor):
        ''' nested class for testing '''

    def test_constructor_should_raise_exception_when_string_is_not_given(self):
        class ConcreteExtractor(AbstractExtractor):
            def get_definitions(self):
                pass

        self.assertRaises(TypeError, ConcreteExtractor, 1)
        self.assertRaises(TypeError, ConcreteExtractor, file)
        try :
            _ = ConcreteExtractor(self.source)
        except:
            self.fail("Unexpected exception in normal construction")

    def test_subclasses_should_implement_abstractmethod(self):
        class ConcreteExtractor(AbstractExtractor):
            pass

        self.assertRaises(TypeError, ConcreteExtractor, self.source)

    def test_slashstar_extractor(self):
        self.assertItemsEqual(self.slashstar.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'/*',
                    'endwith':r'*/',
                    'block':True} ])
        self.assertListEqual(self.slashstar.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'/*',
                    'endwith':r'*/',
                    'block':True} ])

    def test_slashslash_extractor(self):
        self.assertItemsEqual(self.slashslash.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'//',
                    'block':False} ])
        self.assertListEqual(self.slashslash.get_comment_definitions(),
                [ { 'type':'comment',
                    'startwith':r'//',
                    'block':False} ])

    def test_mixin_subclass_extractor(self):
        self.assertItemsEqual(self.mixin.get_comment_definitions(), 
                [ { 'type':'comment',
                    'startwith':r'/*',
                    'endwith':r'*/',
                    'block':True},
                  { 'type':'comment',
                    'startwith':r'//',
                    'block':False} ])
        self.assertListEqual(self.mixin.get_comment_definitions(), 
                [ { 'type':'comment',
                    'startwith':r'/*',
                    'endwith':r'*/',
                    'block':True},
                  { 'type':'comment',
                    'startwith':r'//',
                    'block':False} ])

    def test_scan_block_comments(self):
        mixin = self.MixinExtractor(self.source)
        self.assertEquals(len(mixin.comments), 0)
        mixin.scan_block_comments()
        self.assertEquals(len(mixin.comments), 2)
        spos, epos = mixin.comments[0]
        self.assertEquals(self.source[spos:epos], '''\
/* A Hello World program

    Copyright Ty Coon
    // ...and Buckaroo Banzai
   "Yoyodyne"*/''')
        spos, epos = mixin.comments[1]
        self.assertEquals(self.source[spos:epos], '''\
/* This is not a real comment */''')

    def test_scan_line_comments(self):
        mixin = self.MixinExtractor(self.source)
        self.assertEquals(len(mixin.comments), 0)
        mixin.scan_line_comments()
        self.assertEquals(len(mixin.comments), 4)
        spos, epos = mixin.comments[0]
        self.assertEquals(self.source[spos:epos], '''\
// ...and Buckaroo Banzai''')
        spos, epos = mixin.comments[1]
        self.assertEquals(self.source[spos:epos], '''\
// Neither is this */");''')
        spos, epos = mixin.comments[2]
        self.assertEquals(self.source[spos:epos], '''\
// But this is''')
        spos, epos = mixin.comments[3]
        self.assertEquals(self.source[spos:epos], '''\
// Last comment''')

    def test_scan_quotes(self):
        pass


    def setUp(self):
        self.source = '''\
/* A Hello World program

    Copyright Ty Coon
    // ...and Buckaroo Banzai
   "Yoyodyne"*/

void main() {
    printf("Hello, World.\n");
    printf("/* This is not a real comment */");
    printf("// Neither is this */");
    // But this is
}

// Last comment
'''

        self.target = '''\
/* A Hello World program

    Copyright Ty Coon
    // ...and Buckaroo Banzai
   "Yoyodyne"*/





    // But this is


// Last comment
'''

        self.target_slashstar = '''\
/* A Hello World program

    Copyright Ty Coon
    // ...and Buckaroo Banzai
   "Yoyodyne"*/









'''
        self.target_slashslash = '''\










    // But this is


// Last comment
'''

        self.slashstar = SlashStarExtractor(self.source)
        self.slashslash = SlashSlashExtractor(self.source)
        self.mixin = self.MixinExtractor(self.source)
