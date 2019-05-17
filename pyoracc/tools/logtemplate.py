"""
This file serves as common error messages string for error report.
"""
from pyoracc import _pyversion
class LogTemplate(object):
     # common error message head
    
    def __init__(self):
        self.head_tmp_default= u"[{}] PyOracc Error: ATF_ID: {}, Path: {}"
        self.yacc_tmp_default= u"Can't parse token '{}', (line {}, column {})"
        self.lex_tmp_default= u"Can't identify token '{}' starting (line {}, column {}) "
        self.wrong_logpath_tmp= u"PyOracc Error: Wrong path to place the log file. {} "
        self.summary_num_tmp= u"PyOracc Summary: {} LEX error(s), {} YACC error(s) in {}."
        self.summary_end_tmp= u"PyOracc Info: Finished parsing {0}."
        self.raise_tmp= u"PyOracc failed with message: {0} in {1}"

    def head_default(self,idx,ID,path):
        mesg = self.head_tmp_default.format(idx,ID,path)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg


    def yacc_default(self,value,line,pos,etype):
        mesg = self.yacc_tmp_default.format(value,line, pos, etype)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg


    def lex_default(self,value,line,pos):
        mesg = self.lex_tmp_default.format(value, line, pos)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def wrong_path(self,log_path):
        mesg = self.wrong_logpath_tmp.format(log_path)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def summary_num(self,lex_num,yacc_num,pathname):
        mesg = self.summary_num_tmp.format(lex_num,yacc_num,pathname)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def summary_end(self,pathname):
        mesg = self.summary_end_tmp.format(pathname)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg

    def raise_error(self,e,pathname):
        mesg = self.raise_tmp.format(e, pathname)
        mesg = mesg.encode('UTF-8') if _pyversion()==2 else mesg
        return mesg