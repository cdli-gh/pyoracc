from pyoracc import _pyversion

class ErrorsTemplate(object):

    def error2str(self,oline,error):#error_id,line,column,token
        ''' 
        :params oline:  int, original line before segementation
        :params error: dict, {error_id:int, line:intlist, colmun:intlist, tocken:str} may be extend for further function

        :return: str, a error message

        check different rules and append error message to self.error_str
        '''
        error_id = error['err_id'] #int, the error id
         # list int, list of line number 

        error_str=''
        if error_id == -1:
            line = error['line']
            column = error['column']
            token = error['token']
            error_str = u"PyOracc Error at line {}, column {}: Can't identify token '{}'.".format(oline+line,column,token)

        elif error_id == -2:
            line = error['line']
            column = error['column']
            token = error['token']
            error_str = u"PyOracc Error at line {}, column {}: Can't identify character '{}'.".format(oline+line,column,token)

        elif error_id == 0:
            line = error['line']
            error_str = u"PyOracc Error at line {}: ID line (e.g. &P123456 = AB 78, 910)should be at the 1st line of an ATF section.".format(oline+line[0])
        
        elif error_id == 1:
            line = error['line']
            error_str = u"PyOracc Error at line {}: Except the #link, language Line (e.g. \# atf: lang) should be the 2nd components after ID line in an ATF section".format(oline+line[0])

        elif error_id == 2:
            line = error['line']
            error_str = u"PyOracc Error at line {}: Except the #link, Artifact Type line (e.g. @tablet) should be the 3rd components after ID line and language Line in an ATF section.".format(oline+line[0])

        elif error_id == 3:
            error_str = u"PyOracc Error: First line at {} of a text should start with like \"&P123456 = AB 78, 910\".".format(oline+1)
        
        elif error_id == 4:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str += str(oline+line[i])
                error_str += ', ' if i<(len(line)-1) else ''
            error_str += u": Mutiple ID lines (e.g. &P123456 = AB 78, 910)"
        
        elif error_id == 5:
            error_str = u"PyOracc Error: Missing language line (e.g. #atf: lang akk)"
    
        elif error_id == 6:
            line = error['line']
            error_str = u"PyOracc Error at line " 
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''            
            error_str +=u": Mutiple languages lines (e.g. #atf: lang akk) "

        elif error_id == 7:
            error_str = u"PyOracc Error: Missing object line (e.g. @tablet)"

        elif error_id == 8:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''
            error_str += u": Mutiple object lines (e.g. @tablet)"

        elif error_id == 9:
            error_str = u"PyOracc Error: at least 1 dollar comment line (e.g. $ blank space) or 1 surface line (e.g. @column 2) with 1 transliterration line (e.g. 1. dub-sar)"

        elif error_id == 10:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": No same type brackets can be nested in transliteration line."

        elif error_id == 11:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Incompleted brackets in the line."

        elif error_id == 12:
            #[org_line, (err_col,err_token)]
            lcpairs = error['lcpairs']
            error_str = u"PyOracc Error: Transliretation lines must contain only ASCII characters.\n"
            for i in lcpairs:
                error_str+=(u' '*5+u'at line '+str(oline+i[0])+' column ')
                for j in range(1,len(i)):
                    error_str += str(i[j][0])+', ' if (j<len(i)-1) else str(i[j][0])+'\n'

        elif error_id == 13:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Numerals in a transliteration line must be directly followed by the appropriate sign reading. e.g. 1(disz) or 1/2(gesz2)"


        elif error_id == 14:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": A transliteration must starts with a number which contains 1-4 digits followed by an optional \"\'\", \".\"or [a-z] plus a mandatory \".\" . e.g. 1'., 1a., or 133."

        elif error_id == 15:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": The starting number of transliteration line must contains at most 4 digits followed by an optional \"\'\" plus a mandatory \".\" . e.g. 1'. or 133."

        elif error_id == 16:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Transliteration lines numbering under each surface must be sequential (increasing), the numbering only takes two levels (i.e. 1.a.1 = 1.a)"


        elif error_id == 17:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": A line should start either by &, #, @, $, >>, or number(with optional singal digit [a-z] or \"'\")."

        elif error_id == 18:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Link line (starting from >>) should follow the trans line."

        elif error_id == 19:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": (...) is not allowed."

        elif error_id == 20:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": \"xxx\" is not allowed."

        elif error_id == 21:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": \"c\" is not allowed in trans line, use \"sz\" for shin"

        elif error_id == 22:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": @seal must be followed by a label (e.g. @seal 1)"

        elif error_id == 23:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": \"[\" brackets cannot be nested in \"{}\" or \"()\"."

        elif error_id == 24:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": no blank lines inside a text."

        elif error_id == 25:
            error_str = u"PyOracc Error: No ATF ID find in the ATF ID to period ID mapping catalogue."

        elif error_id == 26:
            error_str = u"PyOracc Error: ATF ID has not yet been specified in the period catalogue."

        elif error_id == 27:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Word \"{}\" should not be in the period {}.".format(error['word'],error['period'])

        elif error_id == 28:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str += str(oline+line[i])
                error_str += ', ' if i<(len(line)-1) else ''      
            error_str += u": Sign \"{}\" should not be in the period {}.".format(error['sign'],error['period'])

        elif error_id == 29:
            error_str = u"PyOracc Error: Corresponding PID {} is not in the current Sign List.".format(error['pid'])

        elif error_id == 30:
            error_str = u"PyOracc Error: Corresponding PID {} is not in the current Word List.".format(error['pid'])

        elif error_id == 31:
            error_str = u"PyOracc Error: This ATF text has not ATF ID at line {}.".format(oline+1)

        error_str = error_str.encode('UTF-8') if _pyversion()==2 else error_str
        return error_str