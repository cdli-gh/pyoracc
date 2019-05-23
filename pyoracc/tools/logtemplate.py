"""
This file serves as common error messages string for error report.
"""
from pyoracc import _pyversion
class LogTemplate(object):
     # common error message head

    def head_default(self,idx,ID,path):
        tmp_str = u"[{}] PyOracc Error: ATF_ID: {}, Path: {}"
        mesg = tmp_str.format(idx,ID,path)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg


    def yacc_default(self,value,line,pos,etype):
        tmp_str = u"Can't parse token '{}', (line {}, column {})"
        mesg = tmp_str.format(value,line, pos, etype)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg


    def lex_default(self,value,line,pos):
        tmp_str = u"Can't identify token '{}' starting (line {}, column {}) "
        mesg = tmp_str.format(value, line, pos)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def wrong_path(self,log_path):
        tmp_str = u"PyOracc Error: Wrong path to place the log file. {} "
        mesg = tmp_str.format(log_path)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def summary_num(self,e_num,pathname):
        tmp_str = u"PyOracc Summary: {} error(s) in {}."
        mesg = tmp_str.format(e_num,pathname)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def summary_end(self,pathname):
        tmp_str = u"PyOracc Info: Finished parsing {0}."
        mesg = tmp_str.format(pathname)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def raise_error(self,e,pathname):
        tmp_str = u"PyOracc failed with message: {0} in {1}"
        mesg = tmp_str.format(e, pathname)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg