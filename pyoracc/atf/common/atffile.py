'''
Copyright 2015, 2016 University College London.

This file is part of PyORACC.

PyORACC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyORACC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyORACC. If not, see <http://www.gnu.org/licenses/>.
'''

import codecs
import sys
import logging

from pyoracc.atf.cdli.atflex import AtfCDLILexer
from pyoracc.atf.cdli.atfyacc import AtfCDLIParser
from pyoracc.atf.common.atflex import AtfLexer
from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.atf.oracc.atflex import AtfOraccLexer
from pyoracc.atf.oracc.atfyacc import AtfOraccParser
from mako.template import Template

logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

consoleHandler = logging.StreamHandler()
log.addHandler(consoleHandler)


class AtfFile(object):
    template = Template("${text.serialize()}")
    def __init__(self, content, atftype='oracc', debug=False,skip=False):
        if content[-1] != '\n':
            content += "\n"
        if atftype == 'cdli':
            atfparser=AtfCDLIParser(debug=debug, skip=skip,log=log,orig_input=content)
            atflexer=AtfCDLILexer(debug=debug, skip=skip,log=log,g_check=atfparser.g_check)
        elif atftype == 'oracc':
            atfparser=AtfOraccParser(debug=debug, skip=skip,log=log,orig_input=content) 
            atflexer=AtfOraccLexer(debug=debug, skip=skip,log=log,g_check=atfparser.g_check)
        else:
            atfparser=AtfParser(debug=debug, skip=skip,log=log,orig_input=content) 
            atflexer=AtfLexer(debug=debug, skip=skip,log=log,g_check=atfparser.g_check)
        lexer = atflexer.lexer
        parser = atfparser.parser
        self.errors_lex=atflexer.errors 
        self.errors_yacc=atfparser.errors
        if debug:
            self.text = parser.parse(content, lexer=lexer, debug=log)
        else:
            self.text = parser.parse(content, lexer=lexer)
        print(atfparser.g_check.print_test())

    def __str__(self):
        return AtfFile.template.render_unicode(**vars(self))

    def serialize(self):
        return AtfFile.template.render_unicode(**vars(self))


def check_atf(infile, atftype, verbose=False,skip=False):
    content = codecs.open(infile,
                          encoding='utf-8-sig').read()
    atffile=AtfFile(content, atftype, verbose,skip)
    errors_lex=atffile.errors_lex
    errors_yacc=atffile.errors_yacc
    return errors_lex,errors_yacc


if __name__ == "__main__":
    check_atf(infile=sys.argv[1], atftype=sys.argv[2],
              verbose=(sys.argv[3] == "True"))
