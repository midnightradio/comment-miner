import io, re
from strscan import StringScanner
from abc import ABCMeta, abstractmethod

class SyntacticError(Exception): pass

class AbstractExtractor(object):
    __metaclass__ = ABCMeta
    __definitions = []

    def __init__(self, source):
        if type(source) is not type(''):
            raise TypeError('Type %s is not supported'%type(source))
        self.__source = source
        self.__formats = None
        self.__scanner = StringScanner(source)
        self.__comments = []
        self.__ignores = []

    #@classmethod
    @abstractmethod
    def get_definitions(cls):
        return cls.__definitions
    
    def get_comment_definitions(self):
        return filter(lambda x:x['type']=='comment', self.get_definitions())
        #return self.__definitions['comments']

    @property
    def comments(self):
        return sorted(set(self.__comments), key=lambda comment:comment[0])

    @property
    def ignores(self):
        return sorted(set(self.__ignores), key=lambda comment:comment[0])

    def extract(self):
        pass

    def scan_block_comments(self):
        for block_comment in [definition for definition in self.get_definitions() if definition['block']]:
            self.__comments += self.scan(block_comment['startwith'], block_comment['endwith'], block_comment['block'])

    def scan_line_comments(self):
        for line_comment in [definition for definition in self.get_definitions() if definition['block'] is False]:
            self.__comments += self.scan(line_comment['startwith'], None, line_comment['block'])


    def scan_comments(self):
        scan_block_comments()
        scan_line_comments()

    def scan_ignore(self):
        pass

    def scan(self, startwith, endwith, block):
        result = list()
        while not self.__scanner.eos():
            if self.__scanner.skip_until(re.escape(startwith)) is None:
                self.__scanner.skip('.*$', re.S)
                continue
            spos = self.__scanner.pos - len(startwith)

            if block is True: # block comment
                if self.__scanner.skip_until(re.escape(endwith)) is None:
                    raise SyntacticError
                    self.__scanner.skip('.*$', re.S)
                    continue
            else: # line comment
                self.__scanner.skip_until(r'.*$', re.M)
                
            epos = self.__scanner.pos
            result.append((spos, epos))
            print '>>>> %d:%d'%(spos, epos)
            print self.__scanner.string[spos:epos]
            print '<<<<'
        return result
        
class SlashStarExtractor(AbstractExtractor):
    def get_definitions(self):
        return [ {  'type':'comment',
                    'startwith':r'/*',
                    'endwith':r'*/',
                    'block':True }
                ] + super(SlashStarExtractor, self).get_definitions()

class SlashSlashExtractor(AbstractExtractor):
    def get_definitions(self):
        return [ { 'type':'comment',
                    'startwith':r'//',
                    'block':False}
                ] + super(SlashSlashExtractor, self).get_definitions()

class SingleQuoteExtractor(AbstractExtractor):
    pass

class DoubleQuoteExtractor(AbstractExtractor):
    pass
