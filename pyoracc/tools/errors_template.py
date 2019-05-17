from pyoracc import _pyversion

class ErrorsTemplate(object):

    def error2str(self,error_id,oline,line,column,token):
        '''
        :params error_id: int, the error id
        :params oline:  int, original line before segementation
        :params line: list int, list of line number 
        :params column: list int, list of column number
        :params token: the token need to be displayed

        :return: str, a error message

        check different rules and append error message to self.error_str
        '''
        error_str=''
        if error_id == -1:
            error_str = u"PyOracc Error at line {}, column {}: Can't identify token '{}'.".format(oline+line[0],column[0],token)

        elif error_id == -2:
            error_str = u"PyOracc Error at line {}, column {}: Can't identify character '{}'.".format(oline+line[0],column[0],token)

        elif error_id == 0:
            error_str = u"PyOracc Error at line {}: ID line (e.g. &P123456 = AB 78, 910)should be at the 2nd line of an ATF section.".format(oline+line[0])
        
        elif error_id == 1:
            error_str = u"PyOracc Error at line {}: Language Line (e.g. \# atf: lang) should be at the 2nd line of an ATF section. ".format(oline+line[0])

        elif error_id == 2:
            error_str = u"PyOracc Error at line {}: Artifact Type line (e.g. @tablet) should be at the 3rd line of an ATF section.".format(oline+line[0])

        elif error_id == 3:
            error_str = u"PyOracc Error: First line of a text should start with like \"&P123456 = AB 78, 910\""
        
        elif error_id == 4:
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str += str(oline+line[i])
                error_str += ', ' if i<(len(line)-1) else ''
            error_str += u": Mutiple ID lines (e.g. &P123456 = AB 78, 910)"
        
        elif error_id == 5:
            error_str = u"PyOracc Error: Missing language line (e.g. #atf: lang akk)"
    
        elif error_id == 6:
            error_str = u"PyOracc Error at line " 
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''            
            error_str +=u": Mutiple languages lines (e.g. #atf: lang akk) "

        elif error_id == 7:
            error_str = u"PyOracc Error: Missing object line (e.g. @tablet)"

        elif error_id == 8:
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''
            error_str += u": Mutiple object lines (e.g. @tablet)"

        elif error_id == 9:
            error_str = u"PyOracc Error: at least 1 dollar comment line (e.g. $ blank space) or 1 surface line (e.g. @column 2) with 1 transliterration line (e.g. 1. dub-sar)"

        elif error_id == 10:
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Brackets cannot be nested in transliteration line."

        elif error_id == 11:
            error_str = u"PyOracc Error at line "
            for i in range(len(line)):
                error_str+=str(oline+line[i])
                error_str+=', ' if i<(len(line)-1) else ''      
            error_str += u": Incompleted brackets in the line."


        
        error_str = error_str.encode('UTF-8') if _pyversion()==2 else error_str
        return error_str