from pyoracc.atf.common.atfyacc import AtfParser


class AtfOraccParser(AtfParser):

    tokens = AtfParser.tokens
    precedence = AtfParser.precedence

    def __init__(self,debug,skip,log,g_check):
        super(AtfOraccParser, self).__init__(debug,skip,log,g_check)
