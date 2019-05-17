from pyoracc.atf.common.atflex import AtfLexer
class AtfCDLILexer(AtfLexer):

    def __init__(self, skip, debug, log,g_check):
        super(AtfCDLILexer, self).__init__(skip, debug, log,g_check)
