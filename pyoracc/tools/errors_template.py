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
            error_str = u"PyOracc Error at line {}: ID line (e.g. &P123456 = AB 78, 910)should be at the 2nd line of an ATF section.".format(oline+line[0])
        
        elif error_id == 1:
            line = error['line']
            error_str = u"PyOracc Error at line {}: Language Line (e.g. \# atf: lang) should be at the 2nd line of an ATF section. ".format(oline+line[0])

        elif error_id == 2:
            line = error['line']
            error_str = u"PyOracc Error at line {}: Artifact Type line (e.g. @tablet) should be at the 3rd line of an ATF section.".format(oline+line[0])

        elif error_id == 3:
            error_str = u"PyOracc Error: First line of a text should start with like \"&P123456 = AB 78, 910\""
        
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
            error_str += u": Brackets cannot be nested in transliteration line."

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
                error_str+=(u' '*5+u'at line '+str(oline+i[0])+'\n')
                for j in range(1,len(i)):
                    error_str += (u' '*8+u'column {}, char {}\n'.format(i[j][0],i[j][1]))

        elif error_id == 13:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Numerals in a transliteration line must be directly followed by the appropriate sign reading. e.g. 1(disz) or 2(gesz2)"


        elif error_id == 14:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": A transliteration must starts with a number which contains 1-4 digits followed by an optional \"\'\" plus a mandatory \".\" . e.g. 1'. or 133."

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
            error_str += u": Transliteration lines numbering under each surface must be sequential (increasing)"


        elif error_id == 17:
            line = error['line']
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": A line should start either by &, #, @, $, or number."


        error_str = error_str.encode('UTF-8') if _pyversion()==2 else error_str
        return error_str