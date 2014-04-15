import re

class StringScanner(object):
    def __init__(self, string=None):
        if string is not None and type(string) is not type(''): raise TypeError('Scanner works only on string')
        else:
            self.__string = string
            self.__pos = 0

    def __iadd__(self, string):
        if string is not None and type(string) is not type(''): raise TypeError('Scanner works only on string')
        self.__string += string
        return self

    def concat(self, string):
        try:
            self+=string
        except:
            raise

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, string):
        if string is not None and type(string) is not type(''): raise TypeError('Scanner works only on string')
        self.__string = string
        self.__pos = 0

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        self.__pos = pos
        
    def eos(self):
        return self.pos == len(self.string)

    @property
    def pre_match(self):
        return self.string[:self.pos-1]

    @property
    def post_match(self):
        return self.string[self.pos:]

    # __strscan_do_scan(self, re, 1,1,1)
    def scan(self, pattern, flags=0):
        if type(pattern) == type(''):
            pattern = re.compile(pattern, flags)
        match = pattern.match(self.string, self.pos)
        if match is not None:
            self.pos = match.end()
            return match.group(0)
        return None

    # __strscan_do_scan(self, re, 1,1,0)
    def scan_until(self, pattern, flags=0):
        if type(pattern) == type(''):
            pattern = re.compile(pattern, flags)
        match = pattern.search(self.string, self.pos)
        if match is not None:
            old = self.pos
            self.pos = match.end()
            return self.string[old:self.pos]
        return None

    # __strscan_do_scan(self, re, 1, 0, 1)
    def skip(self, pattern, flags=0):
        if type(pattern) == type(''):
            pattern = re.compile(pattern, flags)
        match = pattern.match(self.string, self.pos)
        if match is not None:
            old = self.pos
            self.pos = match.end()
            return self.pos - old
        return None

    # __strscan_do_scan(self, re, 1, 0, 0)
    def skip_until(self, pattern, flags=0):
        if type(pattern) == type(''):
            pattern = re.compile(pattern, flags)
        match = pattern.search(self.string, self.pos)
        if match is not None:
            old = self.pos
            self.pos = match.end()
            return self.pos - old
        return None

