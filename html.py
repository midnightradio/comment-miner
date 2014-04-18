from extractors import *

class HTML(AbstractExtractor):
    def get_definitions(self):
        return [ {  'type':'comment',
                    'startwith':r'<!--',
                    'endwith':r'-->',
                    'block':True }
                ] + super(HTML,self).get_definitions()

