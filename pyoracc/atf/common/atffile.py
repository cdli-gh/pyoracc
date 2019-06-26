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
import json
from numbers import Number

from pyoracc.atf.cdli.atflex import AtfCDLILexer
from pyoracc.atf.cdli.atfyacc import AtfCDLIParser
from pyoracc.atf.common.atflex import AtfLexer
from pyoracc.atf.common.atfyacc import AtfParser
from pyoracc.atf.oracc.atflex import AtfOraccLexer
from pyoracc.atf.oracc.atfyacc import AtfOraccParser
from mako.template import Template
from pyoracc.tools.grammar_check import GrammarCheck

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
    def __init__(self, content, atftype='oracc', debug=False,skip=False,atf_id=0):
        g_check = GrammarCheck(content,atf_id)
        if content[-1] != '\n':
            content += "\n"
        if atftype == 'cdli':
            atfparser=AtfCDLIParser(debug=debug,skip=skip,log=log,g_check=g_check)
            
            atflexer=AtfCDLILexer(debug=debug, skip=skip,log=log,g_check=g_check)
        elif atftype == 'oracc':
            atfparser=AtfOraccParser(debug=debug, skip=skip,log=log,g_check=g_check) 
            atflexer=AtfOraccLexer(debug=debug, skip=skip,log=log,g_check=g_check)
        else:
            atfparser=AtfParser(debug=debug, skip=skip,log=log,g_check=g_check) 
            atflexer=AtfLexer(debug=debug, skip=skip,log=log,g_check=g_check)
        
        lexer = atflexer.lexer
        parser = atfparser.parser
        if debug:
            self.text = parser.parse(content, lexer=lexer, debug=log)
        else:
            self.text = parser.parse(content, lexer=lexer)
        g_check.check()
        self.errors = g_check.errors

    def __str__(self):
        return AtfFile.template.render_unicode(**vars(self))

    def serialize(self):
        return AtfFile.template.render_unicode(**vars(self))

    def to_json(self, skip_empty=True, **kwargs):
        '''Return a JSON representation of the parsed file.

        The optional skip_empty argument determines whether keys
        with empty values are included in the output. Set it to
        False to see all possible object members.

        Otherwise it accepts the same optional arguments as
        json.dumps().'''
        def _make_serializable(obj):
            '''Construct a dict representation of an object.

            This is necessary to handle our custom objects
            which json.JSONEncoder doesn't know how to
            serialize.'''

            return {k: v
                    for k, v in vars(obj).items()
                    if not str(k).startswith('_') and not (
                        skip_empty and not v and not isinstance(v, Number)
                    )}

        kwargs.setdefault('indent', 2)
        kwargs.setdefault('default', _make_serializable)
        return json.dumps(self.text, **kwargs)


def check_atf(infile, atftype, verbose=False,skip=False,atf_id=0):
    content = codecs.open(infile,encoding='utf-8-sig').read()
    atffile=AtfFile(content, atftype, verbose,skip,atf_id)
    # errors_lex=atffile.errors_lex
    # errors_yacc=atffile.errors_yacc
    return atffile.errors


if __name__ == "__main__":
    check_atf(infile=sys.argv[1], atftype=sys.argv[2],
              verbose=(sys.argv[3] == "True"))
